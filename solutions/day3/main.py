from dataclasses import dataclass
import re
from sys import argv
from typing import List


@dataclass
class Multiplication:
    left: int
    right: int

    def evaluate(self) -> int:
        return self.left * self.right


class MultiplicationParser:
    input: str
    input_length: int
    position: int

    def __init__(self, input: str):
        self.input = input
        self.input_length = len(input)
        self.position = 0

    def parse(self) -> List[Multiplication]:
        multiplications: List[Multiplication] = []

        while not self.is_at_end():
            next_token = self.peek_token()

            if next_token == "m":
                multiplication = self.try_parse_multiplication()
                if multiplication is not None:
                    multiplications.append(multiplication)
            else:
                self.advance()

        return multiplications
    
    def parse_with_conditionals(self) -> List[Multiplication]:
        multiplication_enabled = True
        multiplications: List[Multiplication] = []

        while not self.is_at_end():
            next_token = self.peek_token()

            if next_token == "m":
                multiplication = self.try_parse_multiplication()
                if multiplication is not None and multiplication_enabled:
                    multiplications.append(multiplication)
            elif next_token == "d":
                conditional = self.try_parse_conditional()
                if conditional is not None:
                    multiplication_enabled = conditional
            else:
                self.advance()

        return multiplications

    def try_parse_multiplication(self) -> Multiplication | None:
        if not self.consume_tokens("mul("):
            return None

        first_number = self.try_parse_number()
        if first_number is None:
            return None
        
        if not self.consume_token(","):
            return None
        
        second_number = self.try_parse_number()
        if second_number is None:
            return None
        
        if not self.consume_token(")"):
            return None
        
        return Multiplication(first_number, second_number)
    
    def try_parse_number(self) -> int | None:
        number: int | None = None

        while True:
            token = self.peek_token()
            if token is None or not token.isdigit():
                break

            if number is None:
                number = int(token)
            else:
                number = (number * 10) + int(token)

            self.advance()

        return number
    
    def try_parse_conditional(self) -> bool | None:
        if not self.consume_tokens("do"):
            return None

        next_token = self.peek_token()

        if next_token == "(" and self.consume_tokens("()"):
            return True
        elif next_token == "n" and self.consume_tokens("n't()"):
            return False
        
        return None

    def consume_token(self, expected_token: str) -> bool:
        actual_token = self.peek_token()

        if actual_token == expected_token:
            self.advance()
            return True
        
        return False
    
    def consume_tokens(self, tokens: str) -> bool:
        for token in tokens:
            if not self.consume_token(token):
                return False
        
        return True
    
    def peek_token(self) -> str | None:
        if self.is_at_end():
            return None
        
        return self.input[self.position]
    
    def advance(self):
        self.position += 1

    def is_at_end(self) -> bool:
        return self.position >= self.input_length
    

def parse_conditional_multiplications_with_regex(memory: str) -> List[Multiplication]:

    multiplication_enabled = True
    multiplications: List[Multiplication] = []

    for match in re.finditer("mul\((\d+),(\d+)\)|do(?!n't)|don't", memory):

        instruction = match.group(0)

        if instruction == "do":
            multiplication_enabled = True
        elif instruction == "don't":
            multiplication_enabled = False
        elif multiplication_enabled:
            first_number = int(match.group(1))
            second_number = int(match.group(2))

            multiplications.append(
                Multiplication(first_number, second_number)
            )

    return multiplications


def calculate_total(memory: str) -> int:
    multiplications = MultiplicationParser(memory).parse()

    return sum_multiplications(multiplications)


def calculate_conditional_total(memory: str, validate_with_regex = False) -> int:

    conditional_multiplications = MultiplicationParser(memory).parse_with_conditionals()
    conditional_total = sum_multiplications(conditional_multiplications)

    if validate_with_regex:
        conditional_multiplications_regex = parse_conditional_multiplications_with_regex(memory)
        conditional_total_regex = sum_multiplications(conditional_multiplications_regex)

        assert conditional_total == conditional_total_regex, "Conditional total from MultiplicationParser does not match total from regex"

    return conditional_total


def sum_multiplications(multiplications: List[Multiplication]) -> int:
    total = 0
    for multiplication in multiplications:
        total += multiplication.evaluate()
    
    return total


def get_memory(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read().strip().replace("\n", "")
    

if __name__ == "__main__":
    input_file_path = argv[1]
    memory = get_memory(input_file_path)

    total = calculate_total(memory)
    print(f"Part 1: {total}")

    conditional_total = calculate_conditional_total(memory, validate_with_regex=True)
    print(f"Part 2: {conditional_total}")
