#!/bin/bash
# add.sh - Import a full or monthly update file
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

case "$1" in
"") echo "Import a full or monthly update file. Usage: ${0##*/} <new.csv>"; exit 1;;
esac

# Check if the script is being run as root, and exit if true
if [ "$UID" -eq "0" ] ; then
  echo ">>>>>>>>>>>>>>>>>>>> You can't be root! - quitting..."
  exit 1
fi

input_file="$1"
input_file="${input_file#./}"
register_file="register.csv"

# Archive the existing register file with a timestamp if it exists
if [ -e "$register_file" ]; then
    echo "$register_file has been archived with these counts:"
    tail -n +2 "$register_file" | cut -d',' -f4 | sort | uniq -c
    cp "$register_file" $(date -d "today" +"%Y%m%d%H%M").retired."$register_file"
fi

# Detect the delimiter in the input file
if head -n 1 "$input_file" | grep -q $'\t'; then
    delimiter=$'\t'
elif head -n 1 "$input_file" | grep -q ','; then
    delimiter=','
else
    echo "Unable to automatically detect the delimiter in the input file."
    echo "Please specify the delimiter manually using the --delimiter option."
    exit 1
fi

# Check for mixed delimiters in the input file
if grep -q $'\t' "$input_file" && grep -q ',' "$input_file"; then
    echo "Error: Mixed delimiters detected in the input file."
    echo "Please ensure the file consistently uses a single delimiter."
    echo "Sending fail notice to the supplier."
    # Add code here to generate a fail notice to the supplier
    exit 1
fi

echo -n "Input file: $input_file"
echo -n ", Output file: $register_file"
echo ", Delimiter: $delimiter"

# Run the Python scripts to remap with the detected delimiter and standardize the column names and content
python ../xmap.py -i "$input_file" -o "mapped_$input_file" --delimiter="$delimiter"
python ../transform.py -i "mapped_$input_file" -o "transformed_$input_file"

# Update the register file if it exists, otherwise create a new one
if [ -e "$register_file" ]; then
    echo "$register_file had these counts:"
    tail -n +2 "$register_file" | cut -d',' -f4 | sort | uniq -c
    python ../merge-update.py -u "transformed_$input_file" -r "$register_file" -o "$register_file"
    echo "$register_file now has these counts:"
    tail -n +2 "$register_file" | cut -d',' -f4 | sort | uniq -c
else
    mv "transformed_$input_file" "$register_file"
    echo "$register_file has been created with these counts:"
    tail -n +2 "$register_file" | cut -d',' -f4 | sort | uniq -c
fi

# Clean up temporary files
rm "mapped_$input_file"

# This script is part of The Common People project, designed and coded by jh.
# The script imports a full or monthly update file, detects the delimiter,
# checks for mixed delimiters, and runs Python scripts to remap and transform
# the input file. It then updates an existing register file or creates a new one.
#
# The script is released under the GNU General Public License (GPL) version 3 or later.
# This means that you are free to use, modify, and distribute this script, as long as
# you follow the terms and conditions of the GPL license.
#
# For more information about the GPL license, please visit:
# https://www.gnu.org/licenses/gpl-3.0.en.html
