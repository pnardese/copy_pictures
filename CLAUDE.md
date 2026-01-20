# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python CLI utility for copying pictures from a camera card to a local disk, organizing them into date-based folders using EXIF metadata.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the script
python copy_pictures.py <source_folder> <destination_folder> [--folder-name "Description"]
```

## Architecture

Single-file script (`copy_pictures.py`) with two main functions:
- `get_date_taken(image_path)`: Extracts date from EXIF metadata (DateTimeOriginal or DateTime tags)
- `copy_pictures(source_folder, destination_folder, folder_name=None)`: Iterates files, creates date-based folders, copies with progress output

Files are organized into folders named by date (YYYY-MM-DD) or optionally with a suffix (e.g., "2024-01-15 - Vacation").

## Dependencies

- `exifread`: For reading EXIF metadata from image files
