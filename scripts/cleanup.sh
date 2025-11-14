#!/bin/bash

# This script finds and deletes redundant files.
# A file is considered redundant if it has a number in its name (e.g., "file 2.txt")
# and its content is identical to the original file (e.g., "file.txt").

find . -regex ".* [2-9]\..*" -o -regex ".* [1-9][0-9]\..*" | while read -r file; do
    # Extract the base name and the number
    base_name=$(echo "$file" | sed -E 's/ (([0-9]+))\././')
    
    # Check if the original file exists
    if [ -f "$base_name" ]; then
        # Compare the two files
        if diff -q "$file" "$base_name" >/dev/null; then
            # If they are the same, delete the numbered file
            echo "Deleting redundant file: $file"
            rm "$file"
        else
            echo "Files are different, not deleting: $file"
        fi
    else
        echo "Original file not found for: $file"
    fi
done
