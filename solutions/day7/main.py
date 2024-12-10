from enum import Enum
from sys import argv
from typing import Dict, List


class Operation(Enum):
    ADD = "Add"
    MULTIPLY = "Multiply" 
    CONCATENATION = "Concatenation"

    def evaluate(self, operand_one: int, operand_two: int) -> int:
        if self == Operation.ADD:
            return operand_one + operand_two
        elif self == Operation.MULTIPLY:
            return operand_one * operand_two
        elif self == Operation.CONCATENATION:
            return (operand_one * (10 ** get_digit_count(operand_two))) + operand_two
        else:
            raise NotImplementedError("Operation {self.value} is not implemented")


def get_digit_count(number: int) -> int:
    count = 1

    while number >= 10:
        number = number // 10
        count += 1

    return count


def get_calibrations(file_path: str) -> Dict[int, List[int]]:
    with open(file_path, "r") as file:

        calibrations: Dict[int, List[int]] = {}

        for line in file.readlines():
            components = line.strip().split(":")

            result = int(components[0])
            values = [int(x) for x in components[1].strip().split(" ")]

            calibrations[result] = values

        return calibrations
    

def is_valid_calibration_equation(
    result: int, 
    values: List[int],
    operations: List[Operation]) -> bool:

    def validate(total: int, index: int) -> bool:
        if index == len(values):
            return result == total

        value = values[index]

        for operation in operations:
            updated_total = operation.evaluate(total, value)

            if validate(updated_total, index + 1):
                return True
            
        return False

    return validate(values[0], 1)


if __name__ == "__main__":
    input_file_path = argv[1]

    calibrations = get_calibrations(input_file_path)

    part_one_operations = [Operation.ADD, Operation.MULTIPLY]
    total = 0
    for result, values in calibrations.items():
        if is_valid_calibration_equation(result, values, part_one_operations):
            total += result
    print(f"Part 1: {total}")

    part_two_operations =  [Operation.ADD, Operation.MULTIPLY, Operation.CONCATENATION]
    total_with_concatentation = 0
    for result, values in calibrations.items():
        if is_valid_calibration_equation(result, values, part_two_operations):
            total_with_concatentation += result
    print(f"Part 2: {total_with_concatentation}")