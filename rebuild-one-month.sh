#!/bin/bash
# rebuild-one-month.sh - Process a specific file in subdirectories
#
# Copyright (C) 2024 The Common People
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Function to process each file
process_file() {
    local file="$1"
    local directory=$(dirname "$file")
    echo "processing $1 in $file"
    # Invoke the existing script with the file name as an argument - when all LADs, change ../ to ./
    ../add.sh "$file"
}

# Check if the file name is provided as a command-line argument
if [ $# -eq 0 ]; then
    echo "Please provide the file name as a command-line argument."
    exit 1
fi
echo "started one month with $1"
search_file="$1"

# Find all files with the specified name in subdirectories and process each file
echo "calling process_file"
export -f process_file
find . -type f -name "$search_file" -exec bash -c 'process_file "$0"' {} \;

# This script is part of The Common People project, designed and coded by jh.
# The script processes a specific file in subdirectories by invoking the add.sh
# script for each occurrence of the file. It takes the file name as a command-line
# argument and searches for files with that name in subdirectories.
#
# The script is released under the GNU General Public License (GPL) version 3 or later.
# This means that you are free to use, modify, and distribute this script, as long as
# you follow the terms and conditions of the GPL license.
#
# For more information about the GPL license, please visit:
# https://www.gnu.org/licenses/gpl-3.0.en.html
