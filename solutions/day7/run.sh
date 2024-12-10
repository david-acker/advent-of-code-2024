#! /bin/bash

input_file_path=$1

script_directory=$(dirname "$(realpath "$0")")
script_file_path="${script_directory}/main.py"

echo "--- Day 7: Bridge Repair ---"
python3 $script_file_path $input_file_path