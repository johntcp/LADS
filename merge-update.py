#!/usr/bin/python
# merge_update.py - Merge a standardized transformed update file with an existing register
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
#
# required input:
#    register.csv carrying LAD, E, 0, PD, Constituency and the elector detail
#    update.csv with this month's changes
# will output next month's register.csv
# 13/03/2024 invented inline code insertion to break the equivalent fieldname table to a python import sourcefile
# 15/03/2004
# How we deal with updates
# ========================
# There are two supplier formats to deal with initially, PD and Idox Xpress.
# PD has AMD flags, Idox Xpress has month codes for when the record was last created, modified and deleted
# In both cases M is handled as D, followed by A unless M and D months are present and identical
# A generates a transient electors record to filter through monthly.sh onto the register with the usual transforms.
#
#    Usage: python merge_update.py -u UPDATEFILE -r REGISTERFILE -o OUTPUTFILE
#

import csv
import argparse
import os
import shutil
from datetime import datetime

def merge_update(update_file, register_file, output_file):
    added_count = 0
    modified_count = 0
    deleted_count = 0

    # Read the existing register into a dictionary
    register_data = {}
    with open(register_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            register_data[row['Elector ID']] = row

    # Process the update file and merge the changes into the register
    with open(update_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            elector_id = row['Elector ID']
            created_month = row['ElectorCreatedMonth']
            modified_month = row['ElectorChangedMonth']
            deleted_month = row['ElectorDeletedMonth']



            if deleted_month > "0" and not (created_month == deleted_month):
                if deleted_month == "3" and created_month == "3":
                    print("delete",elector_id,register_data[elector_id]) 
                deleted_count += 1
                register_data.pop(elector_id, None)
            elif created_month > "0" and not (deleted_month > "0"):
                if deleted_month == "3" and created_month == "3":
                    print("add",elector_id,register_data[elector_id]) 
                added_count += 1
                register_data[elector_id] = row
            elif modified_month > "0" and not (deleted_month > "0"):
                if deleted_month == "3" and created_month == "3":
                    print("modify",elector_id,register_data[elector_id]) 
                modified_count += 1
                register_data[elector_id].update(row)
            else:
                print(f"Warning: add and delete in same month!: Legal - no action taken for elector {elector_id}")

    # Write the updated register to the output file
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(register_data.values())

    print(f"Merged update file '{update_file}' with register file '{register_file}' and saved the updated register as '{output_file}'.")
    print(f"The process added {added_count}, modified {modified_count}, and deleted {deleted_count} elector records, resulting in a net change of {added_count - deleted_count}.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge a standardized transformed update file with an existing register.')
    parser.add_argument('-u', '--update', default='update.csv', help='Update file (default: update.csv)')
    parser.add_argument('-r', '--register', default='register.csv', help='Register file (default: register.csv)')
    parser.add_argument('-o', '--output', default='register.csv', help='Output file (default: register.csv)')
    args = parser.parse_args()

    # Backup the input files with a timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    shutil.copy2(args.update, f"{os.path.splitext(args.update)[0]}_{timestamp}.csv")
    shutil.copy2(args.register, f"{os.path.splitext(args.register)[0]}_{timestamp}.csv")

    merge_update(args.update, args.register, args.output)

# This script is part of The Common People project, designed and coded by jh.
# The script merges a standardized transformed update file with an existing register.
# It processes the update file and applies the changes to the register based on the
# creation, modification, and deletion flags in the update file.
#
# The script is released under the GNU General Public License (GPL) version 3 or later.
# This means that you are free to use, modify, and distribute this script, as long as
# you follow the terms and conditions of the GPL license.
#
# For more information about the GPL license, please visit:
# https://www.gnu.org/licenses/gpl-3.0.en.html
