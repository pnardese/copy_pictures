import os
import sys
import shutil
import exifread
import argparse

# Supported media file extensions
SUPPORTED_EXTENSIONS = {
    # Image formats
    '.jpg', '.jpeg', '.png', '.gif', '.tiff', '.tif', '.bmp', '.webp',
    '.heic', '.heif', '.ico', '.svg',
    # RAW formats
    '.raw', '.cr2', '.cr3', '.nef', '.arw', '.dng', '.orf', '.rw2',
    '.pef', '.srw', '.raf', '.3fr', '.kdc', '.dcr', '.mrw', '.rwl',
    # Photoshop / Adobe formats
    '.psd', '.psb', '.ai', '.eps',
    # Video formats
    '.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.m4v',
    '.mpg', '.mpeg', '.3gp', '.mts', '.m2ts', '.vob', '.ogv',
    # VFX / CGI formats
    '.exr', '.hdr', '.dpx', '.cin',
}

def is_supported_file(filename):
    """Check if file has a supported media extension."""
    ext = os.path.splitext(filename)[1].lower()
    return ext in SUPPORTED_EXTENSIONS

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

def copy_pictures(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Collect all supported media files recursively
    media_files = []
    skipped_files = 0
    for root, dirs, files in os.walk(source_folder):
        for filename in files:
            if is_supported_file(filename):
                media_files.append(os.path.join(root, filename))
            else:
                skipped_files += 1

    if skipped_files > 0:
        print(f"Skipped {skipped_files} non-media files")

    total_files = len(media_files)
    copied_files = 0
    nodate_files = 0
    already_copied = 0

    for file_path in media_files:
        filename = os.path.basename(file_path)
        year, date = get_date_taken(file_path)

        if year is None:
            target_folder = os.path.join(destination_folder, "nodate")
            nodate_files += 1
        else:
            target_folder = os.path.join(destination_folder, year, date)

        destination_path = os.path.join(target_folder, filename)

        # Skip if file already exists at destination
        if os.path.exists(destination_path):
            already_copied += 1
            print(f"Skipping (already exists): {filename}")
            continue

        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        try:
            shutil.copy2(file_path, target_folder)
            copied_files += 1
            print(f"Copying {copied_files}/{total_files - already_copied}: {filename}")
        except Exception as e:
            print(f"Error copying {filename}: {e}")

    print(f"Copy complete. {copied_files} files copied, {already_copied} skipped (already exist), {nodate_files} without date info.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy pictures from a camera card to a disk, organizing by year and date.")
    parser.add_argument("source_folder", help="Source folder with pictures (scans subfolders recursively)")
    parser.add_argument("destination_folder", help="Destination folder on disk")

    args = parser.parse_args()

    if not os.path.exists(args.source_folder):
        print(f"Source folder does not exist: {args.source_folder}")
        sys.exit(1)

    copy_pictures(args.source_folder, args.destination_folder)
