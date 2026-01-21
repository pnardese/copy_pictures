# Copy Pictures

A Python CLI utility for copying pictures and media files from a camera card to a local disk, organizing them into date-based folders using EXIF metadata.

## Features

- Extracts date from EXIF metadata (DateTimeOriginal or DateTime tags)
- Organizes media into `year/date` folder structure (e.g., `2024/2024-01-15/`)
- Recursively scans source folders including subfolders
- Automatically copies files without date metadata to a `nodate` folder
- Skips files that already exist at the destination (duplicate detection)
- Skips non-media files (like `.DS_Store`, system files, etc.)
- Progress output during copy operation

## Supported File Formats

| Category | Extensions |
|----------|------------|
| Images | jpg, jpeg, png, gif, tiff, tif, bmp, webp, heic, heif, ico, svg |
| RAW | raw, cr2, cr3, nef, arw, dng, orf, rw2, pef, srw, raf, 3fr, kdc, dcr, mrw, rwl |
| Photoshop/Adobe | psd, psb, ai, eps |
| Video | mp4, mov, avi, mkv, wmv, flv, webm, m4v, mpg, mpeg, 3gp, mts, m2ts, vob, ogv |
| VFX/CGI | exr, hdr, dpx, cin |

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python copy_pictures.py <source_folder> <destination_folder>
```

### Arguments

| Argument | Description |
|----------|-------------|
| `source_folder` | Source folder with pictures (scans subfolders recursively) |
| `destination_folder` | Destination folder on disk |

### Example

Copy all media from camera card to Pictures folder:
```bash
python copy_pictures.py /Volumes/CAMERA/DCIM ~/Pictures/imported
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
  nodate/
    file_without_exif.png
    video_clip.mp4
```
