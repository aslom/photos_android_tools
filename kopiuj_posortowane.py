#!/usr/bin/env python3
import os
import shutil
from datetime import datetime
import re
import threading
import time




# Define source and destination directories
source_directory = 'F:\\FOTOMAYA\\PIXEL6\\Camera'
destination_directory = 'F:\\FOTOMAYA\\POSORTOWANE'
source_directory = 'photos_dir'
destination_directory = 'sorted_dir'

def extract_year_month_from_filename(filename):
    # Use regex to find year and month in the filename from ANDROID DCIM files
    # ^PXL_\d{8}_\d{6}(\.\w+)?$
    match_pxl = re.search(r'PXL_(\d{4})(\d{2})', filename)
    if match_pxl:
        year = match_pxl.group(1)
        month = match_pxl.group(2)
        return year, month
    match = re.search(r'IMG(\d{4})(\d{2})', filename)
    if match:
        year = match.group(1)
        month = match.group(2)
        return year, month
    return None, None


print(f"Starting to copy photo files from {source_directory} to {destination_directory} sorted by year and month...")

total_files = len([f for f in os.listdir(source_directory) if os.path.isfile(os.path.join(source_directory, f))])
processed_files = 0
last_print_time = time.time()
print(f"Total files to process: {total_files} in {source_directory}")

# Iterate through each file in the source directory
for filename in os.listdir(source_directory):
    source_file_path = os.path.join(source_directory, filename)

    # Ensure it's a file
    if os.path.isfile(source_file_path):
        processed_files += 1
        if processed_files % 100 == 0:  # Print progress every 100 files
            # Print progress of number of processed_files out of total_files every 5 seconds
            current_time = time.time()
            if current_time - last_print_time >= 5:
                print(f"Processed {processed_files} out of {total_files} files.")
                last_print_time = current_time

        # Get creation time and format it
        #creation_time = os.path.getmtime(source_file_path)
        #creation_date = datetime.fromtimestamp(creation_time)
        #year_month_dir = os.path.join(destination_directory, f"{creation_date.year}-{creation_date.month:02}")
        year, month = extract_year_month_from_filename(source_file_path)
        year_month_dir = os.path.join(destination_directory, f"{year}-{month}")
		
        # Create year-month directory if it doesn't exist
        os.makedirs(year_month_dir, exist_ok=True)

        # Define destination file path
        destination_file_path = os.path.join(year_month_dir, filename)

        # Check if the file exists in destination and compare modification times
        if not os.path.exists(destination_file_path) or \
           os.path.getmtime(source_file_path) > os.path.getmtime(destination_file_path):
            shutil.copy2(source_file_path, destination_file_path)  # Use copy2 to preserve metadata
            print(f"Copied {source_file_path} to {destination_file_path}")

print("Files copied successfully.")
