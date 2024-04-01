#!/bin/bash
# rebuild-all-months.sh - Rebuild register.csv files for all months
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

#find . -type f -name "register.csv" -exec rm {} \;
#and remove ../ for ./
rm register.csv
../rebuild-one-month.sh electors.csv
../rebuild-one-month.sh update-jan.csv
../rebuild-one-month.sh update-feb.csv
../rebuild-one-month.sh update-mar.csv
../rebuild-one-month.sh update-apr.csv
../rebuild-one-month.sh update-may.csv
../rebuild-one-month.sh update-jun.csv
../rebuild-one-month.sh update-jul.csv
../rebuild-one-month.sh update-aug.csv
../rebuild-one-month.sh update-sep.csv
../rebuild-one-month.sh update-oct.csv
../rebuild-one-month.sh update-nov.csv

# This script is part of The Common People project, designed and coded by jh.
# The script rebuilds the register.csv files for all months by removing the
# existing register.csv files and invoking the rebuild-one-month.sh script
# for each month's update file.
#
# The script is released under the GNU General Public License (GPL) version 3 or later.
# This means that you are free to use, modify, and distribute this script, as long as
# you follow the terms and conditions of the GPL license.
#
# For more information about the GPL license, please visit:
# https://www.gnu.org/licenses/gpl-3.0.en.html
