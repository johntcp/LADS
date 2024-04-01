#!/bin/bash
# progress.sh - List subdirectories that are not empty
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

if [ -d "$1" ] && [ -n "$(ls -A "$1")" ]; then
    echo "$1"
fi

# This script is part of The Common People project, designed and coded by jh.
# The script checks if a given directory exists and is not empty. If the
# directory meets these conditions, its name is printed to the console.
# This script is typically used in conjunction with the empty.sh script to
# identify active LAD directories.
#
# The script is released under the GNU General Public License (GPL) version 3 or later.
# This means that you are free to use, modify, and distribute this script, as long as
# you follow the terms and conditions of the GPL license.
#
# For more information about the GPL license, please visit:
# https://www.gnu.org/licenses/gpl-3.0.en.html
