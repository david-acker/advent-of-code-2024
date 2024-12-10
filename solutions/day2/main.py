import sys
from typing import List, Set


def check_report_safety(values: List[int]) -> bool:
    is_increasing: bool | None = None

    for i in range(len(values) - 1):
        start = values[i]
        end = values[i + 1]

        difference = start - end

        if is_increasing is None:
            is_increasing = difference > 0
        else:
            if (difference < 0 and is_increasing) or difference > 0 and not is_increasing:
                return False

        absolute_difference = abs(difference)

        if absolute_difference == 0 or absolute_difference > 3:
            return False
    
    return True


def check_report_safety_with_problem_dampener(values: List[int]) -> bool:
    ascending_invalid_indices = get_invalid_indices(values, ascending=True)
    descending_invalid_indices = get_invalid_indices(values, ascending=False)

    invalid_indices = ascending_invalid_indices.union(descending_invalid_indices)

    for index in invalid_indices:
        value = values.pop(index)

        if check_report_safety(values):
            return True
        
        values.insert(index, value)

    return False


def get_invalid_indices(values: List[int], ascending: bool) -> Set[int]:
    invalid_indices: Set[int] = set()

    for i in range(len(values) - 1):
        start = values[i]
        end = values[i + 1]

        difference = start - end

        if (((difference < 0 and ascending) or 
            (difference > 0 and not ascending)) or
            (difference == 0 or abs(difference) > 3)):
            invalid_indices.add(i)
            if (i > 0):
                invalid_indices.add(i - 1)
            invalid_indices.add(i + 1)

    return invalid_indices


def get_reports(file_path: str) -> List[List[int]]:
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    return [parse_report(line) for line in lines]


def parse_report(line: str) -> List[int]:
    values = line.strip().split(" ")
    return [int(x) for x in values]


if __name__ == "__main__":
    input_file_path = sys.argv[1]

    reports = get_reports(input_file_path)

    safe_report_count = 0
    for report in reports:
        if check_report_safety(report):
            safe_report_count += 1
    print(f"Part 1: {safe_report_count}")

    dampened_safe_report_count = 0
    for report in reports:
        if check_report_safety_with_problem_dampener(report):
            dampened_safe_report_count += 1
    print(f"Part 2: {dampened_safe_report_count}")
