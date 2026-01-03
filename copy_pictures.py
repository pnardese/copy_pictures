import os
import shutil
import exifread
import argparse

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

def copy_pictures(source_folder, destination_folder, folder_name=None):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    image_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    total_files = len(image_files)
    copied_files = 0

    for filename in image_files:
        file_path = os.path.join(source_folder, filename)
        date_taken = get_date_taken(file_path)
        if date_taken is None:
            print(f"Could not determine date for {filename}, skipping.")
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

    args = parser.parse_args()

    if not os.path.exists(args.source_folder):
        print(f"Source folder does not exist: {args.source_folder}")
        sys.exit(1)

    copy_pictures(args.source_folder, args.destination_folder, args.folder_name)
