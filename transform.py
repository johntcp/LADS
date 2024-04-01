#!/usr/bin/python
# transform.py - Apply transformations and cleaning to the mapped LAD data
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
# script to apply transformations and cleaning to the mapped LAD data

import csv
import re
import argparse
import unicodedata

def clean_text(text):
    # Remove soft hyphens (0xAD)
    text = text.replace('\xad', '')

    # Remove other control characters
    text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C')
    text = text.replace('\xc3', '')
    text = text.replace('\xad', '')
    text = text.replace('\x82', '')
    text = text.replace('\xc2', '')

    # Replace non-breaking spaces with regular spaces
    text = text.replace('\xa0', ' ')

    # Remove leading and trailing whitespace
    text = text.strip()

    return text

def shuffle_address_lines(row):
    address_fields = ['Address1', 'Address2', 'Address3', 'Address4', 'Address5', 'Address6']

    # Shuffle address lines 2-6 towards the right
    if row['Address2']:
        while row['Address6'] == "" and any(row[field] for field in address_fields[2:]):
            row['Address6'] = row['Address5']
            row['Address5'] = row['Address4']
            row['Address4'] = row['Address3']
            row['Address3'] = ""
            if row['Address2']:
                if not row['Address2'][0].isnumeric():
                    row['Address3'] = row['Address2']
                    row['Address2'] = ""

    return row

def capitalize_mc_mac(name):
    return re.sub(r'\b(Mc|Mac)(\w)', lambda x: x.group(1) + x.group(2).upper(), name)

def transform_data(input_file, output_file, pd_file):
    # Read the pd.csv file and create a lookup dictionary
    pd_lookup = {}
    with open(pd_file, 'r') as pd_csv:
        reader = csv.reader(pd_csv)
        for row in reader:
            lad, e_code, o_code, pdcode, constituency = row
            pd_lookup[pdcode] = (lad, e_code, o_code, constituency)

    process_month=1
    reported_missing_pdcodes = set()
    reported_pdcodes = set()

    with open(input_file, 'r', encoding='latin1') as csv_file:
        reader = csv.DictReader(csv_file)

        with open(output_file, 'w', newline='', encoding='utf-8') as transformed_file:
            fieldnames = reader.fieldnames
            if 'LAD' not in fieldnames:
                fieldnames = ['LAD', 'E-code', 'O-code', 'Constituency'] + reader.fieldnames
            writer = csv.DictWriter(transformed_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                # Apply text cleaning to all fields
                transformed_row = {key: clean_text(value) for key, value in row.items()}

                # Remove postcodes from address fields
                for i in range(1, 10):
                    address_field = f'Address{i}'
                    if address_field in transformed_row:
                        transformed_row[address_field] = transformed_row[address_field].replace(",", "")
                        if transformed_row[address_field] == transformed_row['PostCode']:
                            transformed_row[address_field] = ''  # Set the address field to an empty string if it matches>
#                        transformed_row[address_field] = re.sub(r'\b[a-z]{1,2}\d{1,2}[ ][a-z]?\s*\d[a-z]{2}\b', '', >

                        transformed_row[address_field] = re.sub(r'\b[a-z]{1,2}\d{1,2}[a-z]?\s*\d[a-z]{2}\b', '', transformed_row[address_field])

                # Convert fields to title case, bar exceptions
                transformed_row = {key: value.title() if key not in ['PDCode', 'PostCode', 'Elector Number Prefix', 'Elector Number', 'Register Code' ] else value.upper() for key, value in transformed_row.items()}

                # Standardize breathing marks and apostrophes in personal names
                for field in ['Elector Name First', 'Elector Name Middle', 'Elector Name Last'], 'Elector Name':
                    if field in transformed_row:
                        transformed_row[field] = re.sub(r'[\x80-\xFF]', "'", transformed_row[field])
                        transformed_row[field] = transformed_row[field].replace('`', "'")
                        transformed_row[field] = transformed_row[field].replace(",", "")
                        transformed_row[field] = transformed_row[field].strip()
                        transformed_row[field] = transformed_row[field].title()
                        transformed_row[field] = capitalize_mc_mac(transformed_row[field])

                # Shuffle address lines
                transformed_row = shuffle_address_lines(transformed_row)

                # Standardize update command if this is an Xpress update file
                # Standardize update command if this uses Status flags
                if transformed_row['Status'] == "A":
                    transformed_row['ElectorCreatedMonth'] = process_month
                    transformed_row['ElectorChangedMonth'] =  "0"
                    transformed_row['ElectorDeletedMonth'] =  "0"
                elif transformed_row['Status'] == "M":
                    transformed_row['ElectorChangedMonth'] = process_month
                    transformed_row['ElectorCreatedMonth'] =  "0"
                    transformed_row['ElectorDeletedMonth'] =  "0"
                elif transformed_row['Status'] == "D":
                    transformed_row['ElectorDeletedMonth'] = process_month
                    transformed_row['ElectorCreatedMonth'] =  "0"
                    transformed_row['ElectorChangedMonth'] =  "0"

                shape = transformed_row['Elector Number'].split("-")
                if len(shape) > 1:
                    transformed_row['PDCode'] = shape[0]
                    transformed_row['Elector Number Prefix'] = shape[0]
                    transformed_row['Elector Number'] = shape[1]

                pdcode = transformed_row['Elector Number Prefix']

               # Lookup LAD, E-code, O-code, and Constituency from pd.csv based on PDCode
                if pdcode in pd_lookup:
                    lad, e_code, o_code, constituency = pd_lookup[pdcode]
                    transformed_row['LAD'] = lad
                    transformed_row['E-code'] = e_code
                    transformed_row['O-code'] = o_code
                    transformed_row['Constituency'] = constituency
                    if pdcode not in reported_pdcodes:
                        reported_pdcodes.add(pdcode)  # Add the pdcode to the known good pdcodes
                    else:
                        pass
                elif pdcode not in reported_missing_pdcodes:
                    print(f"No PD entry in pd.csv for {pdcode}")
                    reported_missing_pdcodes.add(pdcode)  # Add the pdcode to the set to avoid repeating the message

                if transformed_row['Elector Number'].endswith("/"):
                    transformed_row['Elector Number'] = transformed_row['Elector Number'][:-1]
                if "/" in transformed_row['Elector Number']:
                    transformed_row['Elector ID'] = transformed_row['Elector Number Prefix'] + "-" + transformed_row['Elector Number']
                elif transformed_row['Elector Number Suffix'] in [""]:
                    transformed_row['Elector ID'] = transformed_row['Elector Number Prefix'] + "-" + transformed_row['Elector Number'] + "/0"
                else:
                    transformed_row['Elector ID'] = transformed_row['Elector Number Prefix'] + "-" + transformed_row['Elector Number'] + "/" + transformed_row['Elector Number Suffix']
                writer.writerow(transformed_row)

    #for pdcode in reported_pdcodes:
    #    pdcode_data = pd_lookup.get(pdcode, ('', '', '', '', ''))
    #    print(f'used polling code',pdcode,'in',pdcode_data[3])
    #print("register.csv has been successfully created.")
    print(f"Transformed and cleaned data saved as '{output_file}'.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Apply transformations and cleaning to mapped LAD data.')
    parser.add_argument('-i', '--input', default='mapped.csv', help='Input mapped file (default: mapped.csv)')
    parser.add_argument('-o', '--output', default='transformed.csv', help='Output transformed file (default: transformed.csv)')
    parser.add_argument('-p', '--pd_file', default='pd.csv', help='Path to pd.csv file (default: pd.csv)')
    args = parser.parse_args()

    transform_data(args.input, args.output, args.pd_file)

# This script is part of The Common People project, designed and coded by jh.
# The script applies transformations and cleaning to the mapped LAD data.
# It processes the input file, performs various data cleaning and transformation
# operations, and saves the transformed data to the output file. The script also
# utilizes a pd.csv file for lookup purposes.
#
# The script is released under the GNU General Public License (GPL) version 3 or later.
# This means that you are free to use, modify, and distribute this script, as long as
# you follow the terms and conditions of the GPL license.
#
# For more information about the GPL license, please visit:
# https://www.gnu.org/licenses/gpl-3.0.en.html
