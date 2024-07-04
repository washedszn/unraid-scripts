#!/bin/bash

# Define an associative array with groups as keys and profiles as values
declare -A media_types
media_types=(
    ["Bluray-1080p"]="Bluray-1080p Bluray-1080p Remux"
    ["WEB-1080p"]="WEB-1080p WEBRip-1080p HDTV-1080p"
    ["Bluray-720p"]="Bluray-720p"
    ["WEB-720p"]="WEB-720p WEBRip-720p HDTV-720p"
    ["Bluray-480p"]="Bluray-480p"
    ["WEB-480p"]="WEB-480p WEBRip-480p"
    ["DVD"]="DVD"
    ["SDTV"]="SDTV"
)

# Root directory of your media files
root_dir="/mnt/user/data/media"

# Check if the root directory exists
if [ ! -d "$root_dir" ]; then
    echo "Root directory $root_dir does not exist."
    exit 1
fi

# Loop through each media type group and calculate total size for each profile
for group in "${!media_types[@]}"
do
    total_size=0
    for profile in ${media_types[$group]}
    do
        size=$(find "$root_dir" -type f -name "*$profile*" -exec du -b {} + 2>/dev/null | awk '{total += $1} END {print total}')
        if [ -z "$size" ]; then
            size=0
        fi
        total_size=$(awk "BEGIN {print $total_size + $size}")
    done
    total_size_gb=$(awk "BEGIN {print $total_size / 1024 / 1024 / 1024}")
    echo "Total size for $group files: $total_size_gb GB"
done
