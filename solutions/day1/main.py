import sys
from typing import Dict, List, Tuple


def calculate_total_distance(left_list: List[int], right_list: List[int]) -> int:
    left_list.sort()
    right_list.sort()

    total_distance = 0

    for i in range(len(left_list)):
        total_distance += abs(left_list[i] - right_list[i])

    return total_distance 


def calculate_similarity_score(left_list: List[int], right_list: List[int]) -> int:
    right_list_number_count: Dict[int, int] = {}
    for x in right_list:
        right_list_number_count[x] = right_list_number_count.get(x, 0) + 1

    similarity_score = 0   
    for x in left_list:
        similarity_score += x * right_list_number_count.get(x, 0)

    return similarity_score 


def get_input_lists(file_path: str) -> Tuple[List[int], List[int]]:
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    number_pairs: List[Tuple[int, int]] = [parse_line(line) for line in lines]
    lists = [list(x) for x in zip(*number_pairs)]

    return (lists[0], lists[1])


def parse_line(line: str) -> Tuple[int, int]:
    values = line.strip().split(" " * 3)
    return int(values[0]), int(values[1])


if __name__ == "__main__":
    input_file_path = sys.argv[1]

    (left_list, right_list) = get_input_lists(input_file_path)
    total_distance = calculate_total_distance(left_list, right_list)
    print(f"Part 1: {total_distance}")

    similarity_score = calculate_similarity_score(left_list, right_list)
    print(f"Part 2: {similarity_score}")
