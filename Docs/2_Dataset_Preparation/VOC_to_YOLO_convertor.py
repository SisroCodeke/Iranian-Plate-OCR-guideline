"""
Pascal VOC to YOLO Format Label Converter (Parallel Version)

This script converts Pascal VOC format XML labels to YOLO format TXT files.
It processes all XML files in the input directory and its subdirectories in parallel,
converts the bounding box annotations to YOLO format (normalized x_center, y_center, width, height),
and saves them to the output directory while preserving the original folder structure.

The class labels are converted according to the provided OCR_CHARACTERS_NAME list.
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
import psutil
import time
from tqdm import tqdm
from PIL import Image

# ========== CONFIGURATION CONSTANTS ==========

# Path to the directory containing Pascal VOC format XML labels (including subdirectories)
PASCAL_FORMAT_LABEL_PATH = "PATH_TO_MIXED_DATASET_DIRETORY"

# Path to the directory where YOLO format TXT labels will be saved
YOLO_FORMAT_LABEL_PATH = "PATH_TO_MIXED_DATASET_OUTPUT_DIRECOTRY"

# Parallel processing configuration
PARALLEL = True  # Set to False to disable parallel processing
NUM_CORES = 8    # Maximum CPU cores to use (None = all available)

# Class list in order (index will be used as class ID in YOLO format)
OCR_CHARACTERS_NAME = ["PUT","YOUR","FOUNDED","CLASSES","HERE"]

# ========== HELPER FUNCTIONS ==========

def get_class_id(class_name):
    """
    Get the YOLO class ID for a given class name.
    
    Args:
        class_name (str): The class name to look up
        
    Returns:
        int: The class ID/index in the OCR_CHARACTERS_NAME list
        
    Raises:
        ValueError: If the class name is not found in the list
    """
    try:
        return OCR_CHARACTERS_NAME.index(class_name)
    except ValueError:
        raise ValueError(f"Class '{class_name}' not found in OCR_CHARACTERS_NAME list")

def convert_pascal_to_yolo(size, box):
    """
    Convert Pascal VOC bounding box coordinates to YOLO format.
    
    Args:
        size (tuple): (width, height) of the image
        box (tuple): (xmin, ymin, xmax, ymax) Pascal VOC bounding box coordinates
        
    Returns:
        tuple: (x_center, y_center, width, height) in normalized YOLO format
    """
    dw = 1. / size[0]
    dh = 1. / size[1]
    
    # Calculate center coordinates and dimensions
    x = (box[0] + box[2]) / 2.0
    y = (box[1] + box[3]) / 2.0
    w = box[2] - box[0]
    h = box[3] - box[1]
    
    # Normalize coordinates
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    
    return (x, y, w, h)

def get_image_size(xml_path):
    """
    Get image size either from XML or from corresponding image file.
    
    Args:
        xml_path (str): Path to the XML file
        
    Returns:
        tuple: (width, height) of the image
    """
    # First try to get size from XML
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    size = root.find('size')
    if size is not None:
        width = int(size.find('width').text)
        height = int(size.find('height').text)
        return (width, height)
    
    # If not in XML, look for image file
    xml_dir = os.path.dirname(xml_path)
    xml_basename = os.path.splitext(os.path.basename(xml_path))[0]
    
    # Try common image extensions
    for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
        image_path = os.path.join(xml_dir, xml_basename + ext)
        if os.path.exists(image_path):
            try:
                with Image.open(image_path) as img:
                    return img.size
            except Exception as e:
                raise ValueError(f"Could not read image dimensions from {image_path}: {str(e)}")
    
    # If still not found, try getting filename from XML (some XMLs might have different naming)
    filename = root.find('filename')
    if filename is not None and filename.text:
        image_path = os.path.join(xml_dir, filename.text)
        if os.path.exists(image_path):
            try:
                with Image.open(image_path) as img:
                    return img.size
            except Exception as e:
                raise ValueError(f"Could not read image dimensions from {image_path}: {str(e)}")
    
    raise ValueError(f"Could not find corresponding image file for {xml_path}. Tried: {xml_basename}.jpg/.jpeg/.png/.bmp")


def process_xml_file(xml_path):
    """
    Process a single Pascal VOC XML file and convert it to YOLO format.
    
    Args:
        xml_path (tuple): (input_path, output_dir) paths
        
    Returns:
        tuple: (success, xml_path, message)
    """
    xml_path, output_dir = xml_path
    try:
        # Parse the XML file
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Get image dimensions
        try:
            width, height = get_image_size(xml_path)
        except ValueError as e:
            return (False, xml_path, str(e))
        
        # Prepare output file path
        relative_path = os.path.relpath(xml_path, PASCAL_FORMAT_LABEL_PATH)
        yolo_path = os.path.join(output_dir, relative_path)
        yolo_path = os.path.splitext(yolo_path)[0] + '.txt'
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(yolo_path), exist_ok=True)
        
        # Process each object in the XML file
        with open(yolo_path, 'w') as f:
            for obj in root.iter('object'):
                # Get class name
                class_name = obj.find('name').text
                
                # Skip if class name is not in our list
                if class_name not in OCR_CHARACTERS_NAME:
                    continue
                
                # Get bounding box coordinates
                bndbox = obj.find('bndbox')
                if bndbox is None:
                    continue
                    
                xmin = float(bndbox.find('xmin').text)
                ymin = float(bndbox.find('ymin').text)
                xmax = float(bndbox.find('xmax').text)
                ymax = float(bndbox.find('ymax').text)
                
                # Convert to YOLO format
                yolo_box = convert_pascal_to_yolo((width, height), (xmin, ymin, xmax, ymax))
                
                # Get class ID
                class_id = get_class_id(class_name)
                
                # Write to output file
                f.write(f"{class_id} {yolo_box[0]} {yolo_box[1]} {yolo_box[2]} {yolo_box[3]}\n")
        
        return (True, xml_path, "Success")
    
    except Exception as e:
        return (False, xml_path, str(e))

def monitor_resources():
    """Return current system resource usage statistics."""
    cpu_percent = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    return {
        'cpu': cpu_percent,
        'memory': mem.percent,
        'used_mem_gb': mem.used / (1024 ** 3),
        'total_mem_gb': mem.total / (1024 ** 3)
    }

def print_resource_stats(stats):
    """Print formatted resource statistics."""
    print(f"CPU: {stats['cpu']:.1f}% | "
          f"Memory: {stats['memory']:.1f}% ({stats['used_mem_gb']:.1f}/{stats['total_mem_gb']:.1f} GB)")

# ========== MAIN PROCESSING ==========

def main():
    """
    Main function that processes all XML files in the input directory and its subdirectories.
    """
    # Convert input and output paths to absolute paths
    pascal_path = os.path.abspath(PASCAL_FORMAT_LABEL_PATH)
    yolo_path = os.path.abspath(YOLO_FORMAT_LABEL_PATH)
    
    print(f"Starting conversion from Pascal VOC to YOLO format")
    print(f"Input directory: {pascal_path}")
    print(f"Output directory: {yolo_path}")
    print(f"Parallel processing: {'Enabled' if PARALLEL else 'Disabled'}")
    if PARALLEL:
        print(f"Using {NUM_CORES} CPU cores")
    
    # Collect all XML files to process
    xml_files = []
    for root, dirs, files in os.walk(pascal_path):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))
    
    total_files = len(xml_files)
    if total_files == 0:
        print("No XML files found in the input directory.")
        return
    
    print(f"\nFound {total_files} XML files to process")
    
    # Prepare task list (input_path, output_dir)
    tasks = [(xml_file, yolo_path) for xml_file in xml_files]
    
    successful_conversions = 0
    failed_conversions = 0
    error_messages = {}
    
    start_time = time.time()
    
    if PARALLEL:
        # Parallel processing with ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=NUM_CORES) as executor:
            futures = [executor.submit(process_xml_file, task) for task in tasks]
            
            # Create progress bar
            with tqdm(total=total_files, desc="Processing files", unit="file") as pbar:
                last_resource_update = 0
                
                for future in as_completed(futures):
                    result = future.result()
                    success, file_path, message = result
                    
                    if success:
                        successful_conversions += 1
                    else:
                        failed_conversions += 1
                        error_messages[file_path] = message
                    
                    # Update progress bar
                    pbar.update(1)
                    
                    # Periodically update resource stats (every 0.5 seconds)
                    current_time = time.time()
                    if current_time - last_resource_update > 0.5:
                        stats = monitor_resources()
                        pbar.set_postfix({
                            'CPU': f"{stats['cpu']:.1f}%",
                            'Mem': f"{stats['memory']:.1f}%",
                            'Success': successful_conversions,
                            'Failed': failed_conversions
                        })
                        last_resource_update = current_time
    else:
        # Sequential processing (for debugging or small datasets)
        with tqdm(total=total_files, desc="Processing files", unit="file") as pbar:
            last_resource_update = 0
            
            for task in tasks:
                result = process_xml_file(task)
                success, file_path, message = result
                
                if success:
                    successful_conversions += 1
                else:
                    failed_conversions += 1
                    error_messages[file_path] = message
                
                pbar.update(1)
                
                # Periodically update resource stats
                current_time = time.time()
                if current_time - last_resource_update > 0.5:
                    stats = monitor_resources()
                    pbar.set_postfix({
                        'CPU': f"{stats['cpu']:.1f}%",
                        'Mem': f"{stats['memory']:.1f}%",
                        'Success': successful_conversions,
                        'Failed': failed_conversions
                    })
                    last_resource_update = current_time
    
    # Print final summary
    elapsed_time = time.time() - start_time
    print("\nConversion complete")
    print(f"Total processing time: {elapsed_time:.2f} seconds")
    print(f"Files processed per second: {total_files / elapsed_time:.2f}")
    print(f"Total XML files processed: {total_files}")
    print(f"Successfully converted: {successful_conversions}")
    print(f"Failed conversions: {failed_conversions}")
    
    if failed_conversions > 0:
        print("\nError summary (first 10 errors):")
        for i, (file_path, error) in enumerate(list(error_messages.items())[:10]):
            print(f"{i+1}. {file_path}: {error}")
        if len(error_messages) > 10:
            print(f"... and {len(error_messages) - 10} more errors")

if __name__ == "__main__":
    # Set up multiprocessing correctly on Windows
    multiprocessing.freeze_support()
    main()
