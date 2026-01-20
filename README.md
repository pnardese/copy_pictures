# Copy Pictures

A Python CLI utility for copying pictures from a camera card to a local disk, organizing them into date-based folders using EXIF metadata.

## Features

- Extracts date from EXIF metadata (DateTimeOriginal or DateTime tags)
- Organizes photos into `year/date` folder structure (e.g., `2024/2024-01-15/`)
- Recursively scans source folders including subfolders
- Option to copy files without date metadata to a separate `nodate` folder
- Progress output during copy operation

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python copy_pictures.py <source_folder> <destination_folder> [--nodate]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `source_folder` | Source folder with pictures (scans subfolders recursively) |
| `destination_folder` | Destination folder on disk |
| `--nodate` | Copy only files without date metadata to a 'nodate' folder |

### Examples

Copy all photos from camera card to Pictures folder:
```bash
python copy_pictures.py /Volumes/CAMERA/DCIM ~/Pictures/imported
```

Copy only files that have no EXIF date:
```bash
python copy_pictures.py /Volumes/CAMERA/DCIM ~/Pictures/imported --nodate
```

## Output Structure

```
destination_folder/
  2024/
    2024-01-15/
      IMG_001.jpg
      IMG_002.jpg
    2024-01-16/
      IMG_003.jpg
  2023/
    2023-12-25/
      IMG_100.jpg
```

With `--nodate` flag:
```
destination_folder/
  nodate/
    file_without_exif.jpg
```
