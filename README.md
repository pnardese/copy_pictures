Copy pictures from a camera card to a folder on a local HD and organizes files in folders with a date name. Optional tag to add a description to folder name, e.g. "2025-12-31 - Vacation"
Using the --date tag allows to choose specific dates to be copied.

Use:

## Normal usage (copies all pictures)
```
python copy_pictures.py /media/camera /home/user/photos --folder-name "Vacation"
```

## Interactive date selection
```
python copy_pictures.py /media/camera /home/user/photos --date
```

## With both date selection and folder name
```
python copy_pictures.py /media/camera /home/user/photos --date --folder-name "Vacation"
```
```
**When you run with `--date`, you'll see:**

Scanning 150 files...

Available dates:
----------------------------------------
1. 2024-01-15 (45 pictures)
2. 2024-01-16 (62 pictures)
3. 2024-01-17 (43 pictures)
----------------------------------------

Enter the numbers of dates to copy (e.g., 1,3,5 or 1-3 or 'all'):
>
```
