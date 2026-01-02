import os
import sys
import shutil
import exifread

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

def copy_pictures(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Get list of image files
    image_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    total_files = len(image_files)
    copied_files = 0

    for filename in image_files:
        file_path = os.path.join(source_folder, filename)
        date_taken = get_date_taken(file_path)
        if date_taken is None:
            print(f"Could not determine date for {filename}, skipping.")
            continue

        target_folder = os.path.join(destination_folder, date_taken)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        shutil.copy2(file_path, target_folder)
        copied_files += 1
        print(f"Copying {filename} in {target_folder} --- {copied_files}/{total_files}")

    print(f"Copy complete. {copied_files}/{total_files} pictures copied.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <source_folder> <destination_folder>")
        sys.exit(1)

    source_folder = sys.argv[1]
    destination_folder = sys.argv[2]

    if not os.path.exists(source_folder):
        print(f"Source folder does not exist: {source_folder}")
        sys.exit(1)

    copy_pictures(source_folder, destination_folder)
