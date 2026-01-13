import os
import shutil
import exifread
import argparse
import sys
from collections import defaultdict

def get_date_taken(image_path):
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            date_tag = tags.get('EXIF DateTimeOriginal') or tags.get('EXIF DateTime')
            if date_tag:
                date_str = str(date_tag)
                return date_str.split(' ')[0].replace(':', '-')
    except Exception as e:
        print(f"Error reading metadata from {image_path}: {e}")
    return None

def get_all_image_files(source_folder):
    """Recursively get all image files from source folder and subfolders."""
    image_files = []
    for root, dirs, files in os.walk(source_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            image_files.append(file_path)
    return image_files

def scan_dates(source_folder):
    """Scan all images and return a dictionary of dates with file counts."""
    dates_dict = defaultdict(list)
    image_files = get_all_image_files(source_folder)
    
    print(f"Scanning {len(image_files)} files...")
    for file_path in image_files:
        date_taken = get_date_taken(file_path)
        if date_taken:
            dates_dict[date_taken].append(file_path)
    
    return dates_dict

def display_and_select_dates(dates_dict):
    """Display available dates and let user select which ones to copy."""
    if not dates_dict:
        print("No pictures with valid dates found.")
        return []
    
    sorted_dates = sorted(dates_dict.keys())
    
    print("\nAvailable dates:")
    print("-" * 40)
    for i, date in enumerate(sorted_dates, 1):
        print(f"{i}. {date} ({len(dates_dict[date])} pictures)")
    print("-" * 40)
    
    print("\nEnter the numbers of dates to copy (e.g., 1,3,5 or 1-3 or 'all'):")
    selection = input("> ").strip()
    
    if selection.lower() == 'all':
        return sorted_dates
    
    selected_dates = []
    try:
        parts = selection.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                # Handle range (e.g., 1-3)
                start, end = map(int, part.split('-'))
                for i in range(start, end + 1):
                    if 1 <= i <= len(sorted_dates):
                        selected_dates.append(sorted_dates[i - 1])
            else:
                # Handle single number
                i = int(part)
                if 1 <= i <= len(sorted_dates):
                    selected_dates.append(sorted_dates[i - 1])
    except ValueError:
        print("Invalid input. Please try again.")
        return display_and_select_dates(dates_dict)
    
    return selected_dates

def copy_pictures(source_folder, destination_folder, folder_name=None, selected_dates=None):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    image_files = get_all_image_files(source_folder)
    
    # Calculate total files to copy based on selected dates
    if selected_dates:
        total_files = 0
        for file_path in image_files:
            date_taken = get_date_taken(file_path)
            if date_taken and date_taken in selected_dates:
                total_files += 1
    else:
        total_files = len(image_files)
    
    copied_files = 0

    for file_path in image_files:
        filename = os.path.basename(file_path)
        date_taken = get_date_taken(file_path)
        if date_taken is None:
            print(f"Could not determine date for {filename}, skipping.")
            continue

        # Skip if date filtering is active and this date isn't selected
        if selected_dates and date_taken not in selected_dates:
            continue

        # Create folder name with optional custom name
        if folder_name:
            target_folder_name = f"{date_taken} - {folder_name}"
        else:
            target_folder_name = date_taken

        target_folder = os.path.join(destination_folder, target_folder_name)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        try:
            shutil.copy2(file_path, target_folder)
            copied_files += 1
            print(f"Copying {copied_files}/{total_files}: {filename}")
        except Exception as e:
            print(f"Error copying {filename}: {e}")

    print(f"Copy complete. {copied_files}/{total_files} pictures copied.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy pictures from a camera card to a disk, organizing by date.")
    parser.add_argument("source_folder", help="Folder on the camera card with pictures")
    parser.add_argument("destination_folder", help="Destination folder on disk")
    parser.add_argument("--folder-name", help="Optional name to add to the date-based folder")
    parser.add_argument("--date", action="store_true", help="Show all dates and interactively select which to copy")

    args = parser.parse_args()

    if not os.path.exists(args.source_folder):
        print(f"Source folder does not exist: {args.source_folder}")
        sys.exit(1)

    selected_dates = None
    if args.date:
        dates_dict = scan_dates(args.source_folder)
        selected_dates = display_and_select_dates(dates_dict)
        if not selected_dates:
            print("No dates selected. Exiting.")
            sys.exit(0)
        print(f"\nSelected dates: {', '.join(selected_dates)}")
        print()

    copy_pictures(args.source_folder, args.destination_folder, args.folder_name, selected_dates)