"""Historical Claude v2 summation demonstration with bounded input."""

import math
from collections.abc import Iterable

Number = int | float
MAX_INPUT_COUNT = 100


def get_number(prompt: str, allow_float: bool = True) -> Number | None:
    """Read one finite number, or return ``None`` when input is closed."""
    while True:
        try:
            user_input = input(prompt)
        except EOFError:
            print("Input closed. Exiting this demo.")
            return None

        try:
            number: Number = float(user_input) if allow_float else int(user_input)
            if allow_float and not math.isfinite(number):
                raise ValueError("numbers must be finite")
            return number
        except ValueError as exc:
            number_type = "finite number" if allow_float else "whole number"
            print(f"Invalid input ({exc}). Please enter a valid {number_type}.")


def get_multiple_numbers(
    count: int, allow_float: bool = True
) -> list[Number] | None:
    """Read between one and ``MAX_INPUT_COUNT`` numbers from the user."""
    if not 1 <= count <= MAX_INPUT_COUNT:
        print(f"Please enter a count from 1 to {MAX_INPUT_COUNT}.")
        return None

    numbers: list[Number] = []
    for index in range(count):
        number = get_number(f"Enter number {index + 1}: ", allow_float)
        if number is None:
            return None
        numbers.append(number)
    return numbers


def custom_sum(numbers: Iterable[Number]) -> Number:
    """Sum values manually without using Python's built-in ``sum``."""
    total: Number = 0
    for number in numbers:
        total += number
    return total


def demonstrate_sum_methods() -> None:
    """Demonstrate different approaches to summing numbers."""
    print("=== Method 1: Sum two integers ===")
    first_integer = get_number("Enter first number: ", allow_float=False)
    second_integer = get_number("Enter second number: ", allow_float=False)
    if first_integer is None or second_integer is None:
        return
    print(f"Sum: {first_integer} + {second_integer} = {first_integer + second_integer}\n")

    print("=== Method 2: Sum two floats ===")
    first_float = get_number("Enter first number: ")
    second_float = get_number("Enter second number: ")
    if first_float is None or second_float is None:
        return
    print(f"Sum: {first_float} + {second_float} = {first_float + second_float}\n")

    print("=== Method 3: Sum multiple numbers ===")
    count = get_number("How many numbers do you want to sum? ", allow_float=False)
    if count is None:
        return
    numbers = get_multiple_numbers(count)
    if numbers is None:
        return
    print(f"Sum: {' + '.join(str(number) for number in numbers)} = {sum(numbers)}\n")

    print("=== Method 4: Custom summation function ===")
    more_numbers = get_multiple_numbers(3)
    if more_numbers is None:
        return
    print(
        f"Sum: {' + '.join(str(number) for number in more_numbers)}"
        f" = {custom_sum(more_numbers)}\n"
    )


if __name__ == "__main__":
    print("Python Number Summation Examples\n")
    demonstrate_sum_methods()
