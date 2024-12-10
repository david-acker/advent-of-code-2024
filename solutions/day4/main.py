from enum import Enum
from sys import argv
from typing import List


class Direction(Enum):
    UP = (0, 1)
    UP_RIGHT = (1, 1)
    RIGHT = (1, 0)
    DOWN_RIGHT = (1, -1)
    DOWN = (0, -1)
    DOWN_LEFT = (-1, -1)
    LEFT = (-1, 0)
    UP_LEFT = (-1, 1)


def matches_string(
    grid: List[List[int]],
    row: int,
    col: int,
    direction: Direction,
    string: str) -> bool:

    width = len(grid)
    height = len(grid[0])

    (row_offset, col_offset) = direction.value

    for letter in string:
        row += row_offset
        col += col_offset

        if (row < 0 or 
            row >= width or 
            col < 0 or 
            col >= height or 
            grid[row][col] != letter):
            return False   

    return True


def word_search(grid: List[List[int]], word: str) -> int:
    match_count = 0
    
    width = len(grid)
    height = len(grid[1])

    first_letter = word[0]
    rest_of_word = word[1:]

    for row in range(width):
        for col in range(height):

            if grid[row][col] != first_letter:
                continue
                
            match_count += sum([
                matches_string(
                    grid,
                    row,
                    col,
                    direction,
                    rest_of_word) for direction in Direction   
            ])

    return match_count


def cross_word_search(grid: List[List[int]]) -> int:
    match_count = 0
    
    width = len(grid)
    height = len(grid[1])

    for row in range(width):
        for col in range(height):

            if grid[row][col] != "A":
                continue

            if not check_diagonals(grid, row, col, [Direction.UP_RIGHT, Direction.DOWN_LEFT], "MS"):
                continue

            if not check_diagonals(grid, row, col, [Direction.UP_LEFT, Direction.DOWN_RIGHT], "MS"):
                continue

            match_count += 1

    return match_count


def check_diagonals(
    grid: List[List[int]],
    row: int,
    col: int,
    directions: List[Direction],
    letters: str) -> bool:
    return (check_diagonal(grid, row, col, directions, letters) 
        or check_diagonal(grid, row, col, directions[::-1], letters))


def check_diagonal(
    grid: List[List[int]],
    row: int,
    col: int,
    directions: List[Direction],
    letters: str) -> bool:

    for (direction, letter) in zip(directions, letters):
        if not matches_string(grid, row, col, direction, letter):
            return False
        
    return True
        

def get_grid(file_path: str) -> List[List[int]]:
    with open(file_path, "r") as file:
        lines = file.read().strip().split("\n")
        return [[*line] for line in lines]


if __name__ == "__main__":
    input_file_path = argv[1]
    grid = get_grid(input_file_path)

    match_count = word_search(grid, "XMAS")
    print(f"Part 1: {match_count}")

    x_match_count = cross_word_search(grid)
    print(f"Part 2: {x_match_count}")
