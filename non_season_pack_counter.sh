#!/bin/bash

total_leaf_dirs=0
multi_release_dirs=0
debug_mode=0

# Check for command line argument for debugging
if [ "$1" == "-d" ] || [ "$1" == "--debug" ]; then
    debug_mode=1
fi

# Set the starting directory
start_dir="/mnt/user/data/media/tv-anime"

[ $debug_mode -eq 1 ] && echo "Starting directory scan in $start_dir..."

# Find all directories and process them
while read dir; do
    [ $debug_mode -eq 1 ] && echo "Processing directory: $dir"

    # Check if the directory contains any subdirectories
    if [ $(find "$dir" -mindepth 1 -maxdepth 1 -type d | wc -l) -eq 0 ]; then
        [ $debug_mode -eq 1 ] && echo "No subdirectories found, processing files..."
        # Increment the total count of leaf directories
        ((total_leaf_dirs++))

        # Extract everything after the last ']' and before the file extension
        releases=$(find "$dir" -type f \( -iname "*.mkv" -o -iname "*.mp4" \) -exec basename {} \; | sed -n 's/.*\]\(.*\)\.\(mkv\|mp4\)$/\1/p' | sort -u)

        [ $debug_mode -eq 1 ] && echo "Extracted releases:" && echo "$releases"

        # Count unique release tags
        count=$(echo "$releases" | wc -l)
        [ $debug_mode -eq 1 ] && echo "Found $count unique release tags."

        # If more than one unique release tag, print the directory and increment the count
        if [ "$count" -gt 1 ]; then
            echo "$dir"
            [ $debug_mode -eq 1 ] && echo "Multiple releases found in $dir"
            ((multi_release_dirs++))
        fi
    fi
done < <(find "$start_dir" -type d)

# Calculate and display statistics
echo "Total leaf directories: $total_leaf_dirs"
echo "Directories with multiple releases: $multi_release_dirs"
if [ $total_leaf_dirs -gt 0 ]; then
    percentage=$(echo "scale=2; $multi_release_dirs * 100 / $total_leaf_dirs" | bc)
    echo "Percentage of directories with multiple releases: $percentage%"
else
    echo "No leaf directories found."
fi
