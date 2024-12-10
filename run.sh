#! /bin/bash

for arg in "$@"; do
    [[ "$arg" == "--test" ]] && use_test_inputs=true
done

solutions_directory="$(pwd)/solutions/"
inputs_directory="$(pwd)/inputs/"

run_solution() {
    day_number=$1

    solution_script_path="${solutions_directory}day${day_number}/run.sh"

    if [[ "$use_test_inputs" == true ]]; then
        input_file_name="input_test.txt"
    else
        input_file_name="input.txt"
    fi

    input_file_path="${inputs_directory}day${day_number}/${input_file_name}"

    if [ -f $solution_script_path ] && [ -f $input_file_path ]; then
        "${solution_script_path}" $input_file_path
        echo
    fi 
}

# Ensure all solution scripts are executable
find . -mindepth 2 -type f -name "run.sh" | xargs chmod +x

if [[ "$use_test_inputs" == true ]]; then
    echo "Advent of Code 2024 (Test Results)"
else
    echo "Advent of Code 2024"
fi
echo

for day_number in {1..25}; do
    run_solution $day_number
done