from enum import Enum
from sys import argv
from typing import List, Set, Tuple


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


def get_next_direction(direction: Direction) -> Direction:
    if direction == Direction.UP:
        return Direction.RIGHT
    elif direction == Direction.RIGHT:
        return Direction.DOWN
    elif direction == Direction.DOWN:
        return Direction.LEFT
    else:
        return Direction.UP
    

def get_next_position(row: int, col: int, direction: Direction) -> Tuple[int, int]:
    (row_offset, col_offset) = direction.value
    return (row + row_offset, col + col_offset)


def get_visited_position_count(
    width: int,
    height: int,
    start_position: Tuple[int, int],
    obstacles: Set[Tuple[int, int]]) -> int:

    (row, col) = start_position
    direction = Direction.UP

    visited: Set[Tuple[int, int, Direction]] = set()

    def within_bounds(r: int, c: int) -> bool:
        return r >= 0 and r < width and c >= 0 and c < height
    
    def has_obstacle(r: int, c: int) -> bool:
        return (r, c) in obstacles 

    while within_bounds(row, col) and (row, col, direction) not in visited:
        visited.add((row, col, direction))

        (new_row, new_col) = get_next_position(row, col, direction)

        while has_obstacle(new_row, new_col):
            direction = get_next_direction(direction)
            (new_row, new_col) = get_next_position(row, col, direction)

        if not within_bounds(new_row, new_col):
            break

        row = new_row
        col = new_col

    return len({ (row, col) for (row, col, _) in visited })


def get_map(file_path: str) -> List[List[str]]:
    with open(file_path, "r") as file:
        return [[*line.strip()] for line in file.readlines()]
    
    
def get_coordinates(map: List[List[str]]) -> Tuple[Tuple[int, int], Set[Tuple[int, int]]]:
    start_position: Tuple[int, int] = (-1, -1)
    obstacles: Set[Tuple[int, int]] = set()

    width = len(map)
    height = len(map[0])

    for row in range(width):
        for col in range(height):
            position = map[row][col]

            if position == "#":
                obstacles.add((row, col))
            elif position == "^":
                start_position = (row, col)

    assert start_position != (-1, -1), "No start position found"
    
    return (start_position, obstacles)
    

if __name__ == "__main__":
    input_file_path = argv[1]

    map = get_map(input_file_path)

    width = len(map)
    height = len(map[0])

    (start_position, obstacles) = get_coordinates(map)

    visited_position_count = get_visited_position_count(width, height, start_position, obstacles)
    print(f"Part 1: {visited_position_count}")
