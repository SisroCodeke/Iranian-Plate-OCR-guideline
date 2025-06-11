"""
Pascal VOC Class Extractor
This script processes Pascal VOC XML annotation files to extract and count all unique object classes.
Features:
- Parallel processing for large datasets
- Real-time system monitoring
- Progress tracking with resource usage
- Output saved as Python list
"""

import os
import xml.etree.ElementTree as ET
from collections import defaultdict
import multiprocessing
from tqdm import tqdm  # Progress bar library
import psutil  # System monitoring library
import time

# ================= CONFIGURATION SECTION =================
# Hardcoded paths and settings (modify these as needed)
XML_FOLDER_PATH = "PATH_TO_VOC_DATASET_DIRECTORY"  # Path to directory containing Pascal VOC XML files
OUTPUT_FILE_PATH = "voc_classes.txt"        # Output file path for class list
USE_PARALLEL = True                         # Enable/disable parallel processing
MAX_CORES = 8                               # Maximum CPU cores to use (None = all available)
SHOW_LIVE_USAGE = True                      # Show live CPU/memory in progress bar
# =========================================================

def process_xml_file(file_path):
    """
    Process a single XML file to extract object classes.
    
    Args:
        file_path (str): Path to the XML file to process
        
    Returns:
        set: Set of unique class names found in the file
    """
    classes = set()  # Using set to automatically handle duplicates within a file
    
    try:
        # Parse the XML file using ElementTree
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Find all object elements in the XML
        for obj in root.findall('object'):
            # Get the class name from the 'name' tag
            class_name = obj.find('name').text
            classes.add(class_name)  # Add to set (automatically handles duplicates)
            
    except ET.ParseError as e:
        # Handle XML parsing errors
        print(f"\nXML Parsing Error in {os.path.basename(file_path)}: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"\nError processing {os.path.basename(file_path)}: {e}")
    
    return classes

def get_system_stats():
    """
    Get current system resource usage statistics.
    
    Returns:
        dict: Dictionary containing CPU and memory usage information
    """
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    return {
        'cpu': cpu_percent,
        'memory_used': memory.used / (1024 ** 3),  # Convert to GB
        'memory_total': memory.total / (1024 ** 3),  # Convert to GB
        'memory_percent': memory.percent
    }

def format_stats(stats):
    """
    Format system statistics for display in progress bar.
    
    Args:
        stats (dict): System statistics from get_system_stats()
        
    Returns:
        str: Formatted string with CPU and memory info
    """
    return (f"CPU: {stats['cpu']:.1f}% | "
            f"MEM: {stats['memory_used']:.1f}/{stats['memory_total']:.1f}GB "
            f"({stats['memory_percent']:.1f}%)")

def process_files_parallel(file_list, num_workers):
    """
    Process XML files in parallel using multiprocessing.
    
    Args:
        file_list (list): List of XML file paths to process
        num_workers (int): Number of parallel workers to use
        
    Returns:
        list: List of sets containing classes from each file
    """
    # Create multiprocessing pool
    with multiprocessing.Pool(processes=num_workers) as pool:
        # Initialize progress bar with custom formatting
        with tqdm(total=len(file_list), 
                 desc="Processing", 
                 unit="file",
                 postfix={'sys': ''}) as pbar:
            
            results = []
            # Process files in parallel with imap_unordered for better performance
            for i, class_set in enumerate(pool.imap_unordered(process_xml_file, file_list)):
                results.append(class_set)
                
                # Update progress bar
                if SHOW_LIVE_USAGE and i % 10 == 0:  # Update stats every 10 files
                    stats = get_system_stats()
                    pbar.set_postfix(sys=format_stats(stats))
                pbar.update(1)
                
    return results

def process_files_sequential(file_list):
    """
    Process XML files sequentially (single-threaded).
    
    Args:
        file_list (list): List of XML file paths to process
        
    Returns:
        list: List of sets containing classes from each file
    """
    results = []
    # Initialize progress bar with custom formatting
    with tqdm(file_list, desc="Processing", unit="file", postfix={'sys': ''}) as pbar:
        for i, file_path in enumerate(pbar):
            results.append(process_xml_file(file_path))
            
            # Update progress bar with system stats
            if SHOW_LIVE_USAGE and i % 5 == 0:  # Update stats every 5 files
                stats = get_system_stats()
                pbar.set_postfix(sys=format_stats(stats))
                
    return results

def list_and_save_voc_classes():
    """
    Main function to coordinate the processing of XML files,
    counting classes, and saving results.
    """
    # Record start time for performance measurement
    start_time = time.time()
    
    # Verify the input directory exists
    if not os.path.isdir(XML_FOLDER_PATH):
        print(f"Error: Directory not found - {XML_FOLDER_PATH}")
        return
    
    # Get list of all XML files in the directory
    xml_files = [os.path.join(XML_FOLDER_PATH, f) 
                for f in os.listdir(XML_FOLDER_PATH) 
                if f.endswith('.xml')]
    
    if not xml_files:
        print("No XML files found in the specified directory.")
        return
    
    # Print initial information
    initial_stats = get_system_stats()
    print(f"\n{' Pascal VOC Class Extractor ':=^50}")
    print(f"• Found {len(xml_files)} XML files to process")
    print(f"• Initial System Status: {format_stats(initial_stats)}")
    
    # Determine processing mode (parallel or sequential)
    if USE_PARALLEL:
        available_cores = multiprocessing.cpu_count()
        num_workers = min(MAX_CORES, available_cores) if MAX_CORES else available_cores
        print(f"• Processing Mode: Parallel ({num_workers} workers)")
        results = process_files_parallel(xml_files, num_workers)
    else:
        print("• Processing Mode: Sequential (1 worker)")
        results = process_files_sequential(xml_files)
    
    # Combine results from all files
    class_counts = defaultdict(int)
    for class_set in results:
        for class_name in class_set:
            class_counts[class_name] += 1
    
    # Sort classes alphabetically
    unique_classes = sorted(class_counts.keys())
    
    # Save the class list to file
    with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(str(unique_classes))
    
    # Calculate processing time
    duration = time.time() - start_time
    final_stats = get_system_stats()
    
    # Print summary report
    print(f"\n{' Processing Complete ':=^50}")
    print(f"• Time elapsed: {duration:.2f} seconds")
    print(f"• Files processed: {len(xml_files)}")
    print(f"• Unique classes found: {len(unique_classes)}")
    print(f"• Final System Status: {format_stats(final_stats)}")
    print(f"• Results saved to: {OUTPUT_FILE_PATH}")
    
    # Print class distribution (top 20 most frequent)
    print(f"\n{' Class Distribution (Top 20) ':-^50}")
    sorted_classes = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    max_len = max(len(name) for name, _ in sorted_classes)
    
    for class_name, count in sorted_classes:
        print(f"{class_name.ljust(max_len)} : {count:>6} occurrences")

if __name__ == "__main__":
    # Set multiprocessing start method (important for Windows compatibility)
    multiprocessing.set_start_method('spawn', force=True)
    
    # Run the main function
    list_and_save_voc_classes()
