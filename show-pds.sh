#!/bin/bash
# show-pds.sh - Create a pd.csv from scratch
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
# required:
#    elector.csv with full LAD file
# creates:
#    pd.csv carrying LAD, E, 0, PD, Constituency
#    and a BACKUP of the old pd.csv if it exists
# NB: It is eventually necessary to hand-edit the resulting pd.csv with the constituency of each district! 
# The system accepts an unedited pd.csv but there is no contituency breakdown of elector distribution

runtime=$(date "+%Y.%m.%d-%H.%M.%S") # this won't change for the duration of the script, unlike direct invocation
if [ -f pd.csv ]; then
    cp pd.csv BACK-PD.$runtime.csv
fi
# Get the current directory's name
dir_name=$(basename "$(pwd)")
# Set IFS to '-' and read the parts into variables
IFS='-' read -r t2 t3 t4 <<< "$dir_name"
tail -n +2 "${1:-electors.csv}" | cut -d',' -f1 |
sort | uniq | sed "s/^/$t2,$t3,$t4,/" |
sed "s/$/,$t4/" | sed 's/"//g' | tee pd.csv

# This script is part of The Common People project, designed and coded by jh.
# The script creates a pd.csv file from scratch using an elector.csv file.
# It extracts the necessary information from the elector.csv file and formats
# it into the required pd.csv structure. If a previous pd.csv file exists, it
# creates a backup before generating the new one.
#
# The script is released under the GNU General Public License (GPL) version 3 or later.
# This means that you are free to use, modify, and distribute this script, as long as
# you follow the terms and conditions of the GPL license.
#
# For more information about the GPL license, please visit:
# https://www.gnu.org/licenses/gpl-3.0.en.html
