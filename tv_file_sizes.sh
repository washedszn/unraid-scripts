#!/bin/bash

# Hardcoded directory
search_dir="/mnt/user/data/media/tv-anime"

# Function to convert bytes to human-readable format
to_human_readable() {
    local bytes=$1
    if [ $bytes -lt 1024 ]; then
        echo "${bytes} B"
    elif [ $bytes -lt 1048576 ]; then
        echo "$(echo "scale=2; $bytes/1024" | bc) KB"
    elif [ $bytes -lt 1073741824 ]; then
        echo "$(echo "scale=2; $bytes/1048576" | bc) MB"
    else
        echo "$(echo "scale=2; $bytes/1073741824" | bc) GB"
    fi
}

# Find all mkv and mp4 files recursively and handle spaces and special characters properly
mapfile -t file_list < <(find "$search_dir" -type f \( -iname "*.mkv" -o -iname "*.mp4" \))

# Check if files were found
if [ ${#file_list[@]} -eq 0 ]; then
    echo "No .mkv or .mp4 files found in the directory."
    exit 1
fi

# Collect all file sizes into an array
sizes=()
for file in "${file_list[@]}"; do
    sizes+=($(stat -c %s "$file"))
done

# Calculate number of files
count=${#sizes[@]}

# Check if there are files to process
if [ $count -eq 0 ]; then
    echo "No files to process."
    exit 1
fi

# Sort sizes to calculate statistics
IFS=$'\n' sorted_sizes=($(sort -n <<<"${sizes[*]}"))
unset IFS

# Calculations
total_size=0
for size in "${sorted_sizes[@]}"; do
    total_size=$(($total_size + $size))
done

min_size=$(to_human_readable ${sorted_sizes[0]})
max_size=$(to_human_readable ${sorted_sizes[-1]})
average_size=$(to_human_readable $(echo "$total_size / $count" | bc))

# Calculate percentiles
percentile_25=$(to_human_readable $(echo "${sorted_sizes[$((count * 25 / 100))]}" | bc))
percentile_50=$(to_human_readable $(echo "${sorted_sizes[$((count * 50 / 100))]}" | bc)) # Median
percentile_75=$(to_human_readable $(echo "${sorted_sizes[$((count * 75 / 100))]}" | bc))

# Output the results
echo "Total size of files: $(to_human_readable $total_size)"
echo "Total number of files: $count"
echo "Minimum file size: $min_size"
echo "Maximum file size: $max_size"
echo "Average file size: $average_size"
echo "25th percentile (file size): $percentile_25"
echo "50th percentile (Median file size): $percentile_50"
echo "75th percentile (file size): $percentile_75"