#! /bin/bash

input_file_path=$1

script_directory=$(dirname "$(realpath "$0")")
script_file_path="${script_directory}/main.py"

echo "--- Day 5: Print Queue ---"
python3 $script_file_path $input_file_path