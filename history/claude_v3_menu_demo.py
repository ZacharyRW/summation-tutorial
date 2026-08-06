"""Historical Claude v3 menu-driven summation demonstration."""

import math
from collections.abc import Iterable
from typing import Union

Number = Union[int, float]
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
            print(
                f"Invalid input ({exc}). Please enter a valid {number_type} "
                "(negative numbers allowed)."
            )


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


def analyze_numbers(numbers: Iterable[Number]) -> dict[str, object]:
    """Return sign and summary statistics for finite numeric values.

    Values must be built-in ``int`` values or finite ``float`` values. The input
    is materialized once, so generators are supported and the returned
    sign-based lists preserve the original values and order. ``total`` and the
    sign-specific sums use Python's built-in ``sum`` and consequently retain
    normal Python ``int``/``float`` arithmetic rather than adding a
    high-precision policy to this historical demonstration.

    For non-empty input, ``mean`` is ``total / count``, ``median`` is the
    middle sorted value (or the arithmetic mean of the two middle values), and
    ``minimum`` and ``maximum`` are input values. For empty input, all four
    summary statistics are ``None``. Non-numeric values raise ``TypeError``;
    non-finite floats raise ``ValueError``.
    """
    values = list(numbers)
    for number in values:
        if isinstance(number, bool) or not isinstance(number, (int, float)):
            raise TypeError("numbers must contain int or float values")
        if isinstance(number, float) and not math.isfinite(number):
            raise ValueError("numbers must contain only finite float values")

    positive_numbers = [number for number in values if number > 0]
    negative_numbers = [number for number in values if number < 0]
    zero_numbers = [number for number in values if number == 0]
    total = sum(values)

    if values:
        sorted_values = sorted(values)
        middle_index = len(sorted_values) // 2
        if len(sorted_values) % 2:
            median: Number | None = sorted_values[middle_index]
        else:
            lower_middle = sorted_values[middle_index - 1]
            upper_middle = sorted_values[middle_index]
            median = (lower_middle + upper_middle) / 2
        mean: Number | None = total / len(values)
        minimum: Number | None = sorted_values[0]
        maximum: Number | None = sorted_values[-1]
    else:
        mean = median = minimum = maximum = None

    return {
        "total": total,
        "positive": positive_numbers,
        "negative": negative_numbers,
        "zeros": zero_numbers,
        "positive_sum": sum(positive_numbers),
        "negative_sum": sum(negative_numbers),
        "positive_count": len(positive_numbers),
        "negative_count": len(negative_numbers),
        "zero_count": len(zero_numbers),
        "mean": mean,
        "median": median,
        "minimum": minimum,
        "maximum": maximum,
    }


def method_two_integers() -> None:
    """Sum two integers."""
    print("\n=== Sum Two Integers ===")
    first = get_number("Enter first number: ", allow_float=False)
    second = get_number("Enter second number: ", allow_float=False)
    if first is None or second is None:
        return
    print(f"Sum: {first} + {second} = {first + second}")


def method_two_floats() -> None:
    """Sum two finite floating-point numbers."""
    print("\n=== Sum Two Floats ===")
    first = get_number("Enter first number: ")
    second = get_number("Enter second number: ")
    if first is None or second is None:
        return
    print(f"Sum: {first} + {second} = {first + second}")


def _read_count(prompt: str) -> int | None:
    count = get_number(prompt, allow_float=False)
    if count is None:
        return None
    return count


def method_multiple_numbers() -> None:
    """Sum a bounded number of values."""
    print("\n=== Sum Multiple Numbers ===")
    count = _read_count("How many numbers do you want to sum? ")
    if count is None:
        return
    numbers = get_multiple_numbers(count)
    if numbers is None:
        return
    print(f"Sum: {' + '.join(str(number) for number in numbers)} = {sum(numbers)}")


def method_custom_sum() -> None:
    """Demonstrate the extracted custom summation function."""
    print("\n=== Custom Summation Function ===")
    count = _read_count("How many numbers? ")
    if count is None:
        return
    numbers = get_multiple_numbers(count)
    if numbers is None:
        return
    print(
        f"Sum: {' + '.join(str(number) for number in numbers)}"
        f" = {custom_sum(numbers)}"
    )


def method_positive_negative_demo() -> None:
    """Demonstrate a sign-based breakdown of finite numbers."""
    print("\n=== Positive and Negative Numbers Demo ===")
    print("Enter a mix of positive and negative numbers")
    count = _read_count("How many numbers? ")
    if count is None:
        return
    numbers = get_multiple_numbers(count)
    if numbers is None:
        return

    analysis = analyze_numbers(numbers)
    print(f"\nSum: {' + '.join(str(number) for number in numbers)} = {analysis['total']}")
    print("\nBreakdown:")
    print(f"  Positive numbers: {analysis['positive']} (sum: {analysis['positive_sum']})")
    print(f"  Negative numbers: {analysis['negative']} (sum: {analysis['negative_sum']})")
    if analysis["zero_count"]:
        print(f"  Zeros: {analysis['zero_count']}")
    print("\nSummary statistics:")
    print(f"  Mean: {analysis['mean']}")
    print(f"  Median: {analysis['median']}")
    print(f"  Minimum: {analysis['minimum']}")
    print(f"  Maximum: {analysis['maximum']}")


def display_menu() -> None:
    """Display the main menu."""
    print("\n" + "=" * 50)
    print("Python Number Summation Examples")
    print("=" * 50)
    print("1. Sum two integers")
    print("2. Sum two floats")
    print("3. Sum multiple numbers")
    print("4. Custom summation function")
    print("5. Positive/Negative numbers demo")
    print("6. Run all examples")
    print("0. Exit")
    print("=" * 50)


def _wait_for_enter(prompt: str) -> bool:
    try:
        input(prompt)
    except EOFError:
        print("Input closed. Exiting this demo.")
        return False
    return True


def run_all_examples() -> None:
    """Run all example methods until input closes."""
    method_two_integers()
    if not _wait_for_enter("\nPress Enter to continue..."):
        return
    method_two_floats()
    if not _wait_for_enter("\nPress Enter to continue..."):
        return
    method_multiple_numbers()
    if not _wait_for_enter("\nPress Enter to continue..."):
        return
    method_custom_sum()
    if not _wait_for_enter("\nPress Enter to continue..."):
        return
    method_positive_negative_demo()


def main() -> None:
    """Run the menu until the user exits or input closes."""
    while True:
        display_menu()
        try:
            choice = input("\nEnter your choice (0-6): ")
        except EOFError:
            print("Input closed. Exiting this demo.")
            return

        if choice == "1":
            method_two_integers()
        elif choice == "2":
            method_two_floats()
        elif choice == "3":
            method_multiple_numbers()
        elif choice == "4":
            method_custom_sum()
        elif choice == "5":
            method_positive_negative_demo()
        elif choice == "6":
            run_all_examples()
        elif choice == "0":
            print("\nThank you for using the summation examples!")
            return
        else:
            print("\nInvalid choice. Please enter a number between 0 and 6.")

        if choice in {"1", "2", "3", "4", "5"} and not _wait_for_enter(
            "\nPress Enter to return to menu..."
        ):
            return


if __name__ == "__main__":
    main()
