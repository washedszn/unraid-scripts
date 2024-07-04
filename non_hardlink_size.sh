#!/bin/bash

# Define the directory
dir="/mnt/user/data/torrents"

# Check if directory exists
if [ ! -d "$dir" ]; then
  echo "Directory $dir does not exist."
  exit 1
fi

# Calculate the total size of non-hardlinked files across all subdirectories
total_size=$(find "$dir" -type f -links 1 -exec du -k {} + | awk '{sum += $1} END {print sum}')

# If total_size is empty, set it to 0
total_size=${total_size:-0}

# Convert size from kilobytes to human-readable format and display it
echo "Total size of non-hardlinked files: $(numfmt --to=iec --from-unit=1024 --suffix=B $total_size)"