#!/usr/bin/python
# xmap.py - Map LAD files to internal format using the synonyms dictionary
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

# The Common People
# script to map LAD files to our internal format using the synonyms dictionary

import sys
import csv
import argparse
from pprint import pprint
from cp3_fieldnames import synonyms

def map_headers(header, synonyms):
    mapped_headers = {}
    for field in header:
        for key, synonyms_list in synonyms.items():
            if any(synonym.lower() == field.lower() for synonym in synonyms_list):
                mapped_headers[field] = key
                break
        else:
            print(f"Error: No synonym found for column name '{field}'. Please update the synonyms dictionary.")
            sys.exit(1)
    return mapped_headers

def map_lad_file(input_file, output_file, delimiter, synonyms):
    with open(input_file, 'r', encoding='latin-1') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=delimiter)
        mapped_headers = map_headers(reader.fieldnames, synonyms)

        with open(output_file, 'w', newline='', encoding='latin-1') as mapped_file:
            writer = csv.DictWriter(mapped_file, fieldnames=list(synonyms.keys()), quoting=csv.QUOTE_ALL, quotechar='"')
            writer.writeheader()

            for row in reader:
                mapped_row = {mapped_headers[key]: value for key, value in row.items()}
                writer.writerow(mapped_row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Map LAD files to internal format.')
    parser.add_argument('-i', '--input', default='electors.csv', help='Input LAD file (default: electors.csv)')
    parser.add_argument('-o', '--output', default='mapped.csv', help='Output mapped file (default: mapped.csv)')
    parser.add_argument('-d', '--delimiter', default=',', help='The delimiter used in the input file (default: comma).')
    args = parser.parse_args()

    map_lad_file(args.input, args.output, args.delimiter, synonyms)

# This script is part of The Common People project, designed and coded by jh.
# The script maps LAD files to an internal format using a synonyms dictionary.
# It reads the input LAD file, maps the column headers to the internal format
# using the synonyms dictionary, and writes the mapped data to the output file.
#
# The script is released under the GNU General Public License (GPL) version 3 or later.
# This means that you are free to use, modify, and distribute this script, as long as
# you follow the terms and conditions of the GPL license.
#
# For more information about the GPL license, please visit:
# https://www.gnu.org/licenses/gpl-3.0.en.html
