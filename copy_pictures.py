import os
import sys
import shutil
import exifread
import argparse

def get_date_taken(image_path):
    """Returns (year, date) tuple, e.g. ('2024', '2024-01-15') or (None, None)."""
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            date_tag = tags.get('EXIF DateTimeOriginal') or tags.get('EXIF DateTime')
            if date_tag:
                date_str = str(date_tag)
                date_part = date_str.split(' ')[0].replace(':', '-')
                year = date_part.split('-')[0]
                return year, date_part
    except Exception as e:
        print(f"Error reading metadata from {image_path}: {e}")
    return None, None

def copy_pictures(source_folder, destination_folder, nodate=False):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Collect all files recursively
    image_files = []
    for root, dirs, files in os.walk(source_folder):
        for filename in files:
            image_files.append(os.path.join(root, filename))

    total_files = len(image_files)
    copied_files = 0

    for file_path in image_files:
        filename = os.path.basename(file_path)
        year, date = get_date_taken(file_path)

        if nodate:
            if year is not None:
                continue
            target_folder = os.path.join(destination_folder, "nodate")
        else:
            if year is None:
                print(f"Could not determine date for {filename}, skipping.")
                continue
            target_folder = os.path.join(destination_folder, year, date)

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
    parser = argparse.ArgumentParser(description="Copy pictures from a camera card to a disk, organizing by year and date.")
    parser.add_argument("source_folder", help="Source folder with pictures (scans subfolders recursively)")
    parser.add_argument("destination_folder", help="Destination folder on disk")
    parser.add_argument("--nodate", action="store_true", help="Copy only files without date metadata to a 'nodate' folder")

    args = parser.parse_args()

    if not os.path.exists(args.source_folder):
        print(f"Source folder does not exist: {args.source_folder}")
        sys.exit(1)

    copy_pictures(args.source_folder, args.destination_folder, nodate=args.nodate)
