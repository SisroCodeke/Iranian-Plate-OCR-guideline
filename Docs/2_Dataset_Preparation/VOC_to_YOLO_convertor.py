"""
Pascal VOC to YOLO Format Label Converter

This script converts Pascal VOC format XML labels to YOLO format TXT files.
It processes all XML files in the input directory and its subdirectories,
converts the bounding box annotations to YOLO format (normalized x_center, y_center, width, height),
and saves them to the output directory while preserving the original folder structure.

The class labels are converted according to the provided OCR_CHARACTERS_NAME list.
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path

# ========== CONFIGURATION CONSTANTS ==========

# Path to the directory containing Pascal VOC format XML labels (including subdirectories)
PASCAL_FORMAT_LABEL_PATH = "/path/to/pascal/labels"

# Path to the directory where YOLO format TXT labels will be saved
YOLO_FORMAT_LABEL_PATH = "/path/to/yolo/labels"

# Class list in order (index will be used as class ID in YOLO format)
OCR_CHARACTERS_NAME = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "ت", "و", "ق", "د", "ب", "ی", "ج", "پ", "ه‍", "ل",
    "ص", "م", "ط", "س", "ن", "ع", "گ", "ف", "ژ", "الف",
    "ک", "ث", "S", "D", "تشریفات", "ز", "ش", "ظ"
]

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

def process_xml_file(xml_path, output_dir):
    """
    Process a single Pascal VOC XML file and convert it to YOLO format.
    
    Args:
        xml_path (str): Path to the input XML file
        output_dir (str): Base directory for saving YOLO format files
        
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    try:
        # Parse the XML file
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Get image dimensions
        size = root.find('size')
        if size is None:
            print(f"Warning: No size element in {xml_path}, skipping")
            return False
            
        width = int(size.find('width').text)
        height = int(size.find('height').text)
        
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
                    print(f"Warning: Unknown class '{class_name}' in {xml_path}, skipping")
                    continue
                
                # Get bounding box coordinates
                bndbox = obj.find('bndbox')
                if bndbox is None:
                    print(f"Warning: No bounding box for object in {xml_path}, skipping")
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
        
        return True
    
    except Exception as e:
        print(f"Error processing {xml_path}: {str(e)}")
        return False

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
    
    # Counters for statistics
    total_files = 0
    successful_conversions = 0
    
    # Walk through all files in the input directory
    for root, dirs, files in os.walk(pascal_path):
        for file in files:
            if file.endswith('.xml'):
                total_files += 1
                xml_file_path = os.path.join(root, file)
                
                if process_xml_file(xml_file_path, yolo_path):
                    successful_conversions += 1
    
    # Print summary
    print(f"\nConversion complete")
    print(f"Total XML files found: {total_files}")
    print(f"Successfully converted: {successful_conversions}")
    if total_files > 0:
        print(f"Failed conversions: {total_files - successful_conversions}")

if __name__ == "__main__":
    main()
