"""Canonical reusable lesson demonstrating several Python summation methods."""

from __future__ import annotations

import argparse
import math
import operator
import sys
from collections.abc import Iterable, Sequence
from functools import reduce

Number = int | float
PRECISION_EXAMPLE = (1e16, 1.0, 1.0, 1.0, -1e16)


def parse_numbers(prompt: str, allow_float: bool = False) -> list[Number] | None:
    """
    Read a space-separated line of finite numbers.

    Integer mode returns exact ``int`` values. Float mode accepts only finite
    ``float`` values. Returns ``None`` after an EOF so callers can exit cleanly.
    """
    while True:
        try:
            raw = input(prompt).strip()
        except EOFError:
            print("Input closed. Exiting this demo.")
            return None

        if not raw:
            print("Please enter one or more numbers separated by spaces.")
            continue

        parts = raw.split()
        try:
            if allow_float:
                numbers = [float(part) for part in parts]
                if not all(math.isfinite(number) for number in numbers):
                    raise ValueError("numbers must be finite")
                return numbers
            return [int(part) for part in parts]
        except ValueError as exc:
            print(f"Invalid input ({exc}). Try again.")


# --- Two-number sum variants -------------------------------------------------


def add_plus(a: Number, b: Number) -> Number:
    """Direct addition with +."""
    return a + b


def add_sum(a: Number, b: Number) -> Number:
    """Built-in sum over a fixed-size tuple."""
    return sum((a, b))


def add_operator(a: Number, b: Number) -> Number:
    """operator.add function."""
    return operator.add(a, b)


# --- N-number sum variants ---------------------------------------------------


def sum_builtin(nums: Iterable[Number]) -> Number:
    """Built-in sum; fast for numeric lists."""
    return sum(nums)


def sum_reduce(nums: Iterable[Number]) -> Number:
    """reduce + operator.add; educational."""
    return reduce(operator.add, nums, 0)


def sum_fsum(nums: Iterable[Number]) -> float:
    """math.fsum; better numeric stability for floats."""
    return math.fsum(nums)


def precision_example_results() -> tuple[float, float, float]:
    """Compare the three N-number methods on a rounding-sensitive example."""
    numbers = PRECISION_EXAMPLE
    return sum_builtin(numbers), sum_reduce(numbers), sum_fsum(numbers)


def parse_cli_numbers(
    raw_numbers: Sequence[str], allow_float: bool = False
) -> list[Number]:
    """Parse command-line numbers using the lesson's numeric contract."""
    numbers: list[Number] = []
    number_type = "finite number" if allow_float else "whole number"
    for raw_number in raw_numbers:
        try:
            number: Number = float(raw_number) if allow_float else int(raw_number)
        except ValueError as exc:
            raise ValueError(f"{raw_number!r} is not a valid {number_type}.") from exc
        if allow_float and not math.isfinite(number):
            raise ValueError(f"{raw_number!r} is not a valid finite number.")
        numbers.append(number)
    return numbers


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the optional one-shot command-line interface."""
    parser = argparse.ArgumentParser(
        description="Sum numbers without starting the interactive lesson."
    )
    parser.add_argument(
        "--numbers",
        metavar="NUMBER",
        nargs=argparse.REMAINDER,
        help="one or more numbers to sum; defaults to exact whole numbers",
    )
    parser.add_argument(
        "--float",
        dest="allow_float",
        action="store_true",
        help="parse --numbers as finite floating-point values",
    )
    return parser


def show_two_number_demo() -> bool:
    """Show the two-number lesson and report whether input remained open."""
    while True:
        numbers = parse_numbers(
            "Enter exactly two integers (e.g., 3 5): ", allow_float=False
        )
        if numbers is None:
            return False
        if len(numbers) == 2:
            a, b = numbers
            break
        print("Please enter exactly two integers separated by spaces.")

    print("\nTwo-number methods:")
    print(f"  a + b               -> {add_plus(a, b)}")
    print(f"  sum((a, b))         -> {add_sum(a, b)}")
    print(f"  operator.add(a, b)  -> {add_operator(a, b)}")
    return True


def show_many_number_demo() -> bool:
    """Show the many-number lesson and report whether input remained open."""
    nums = parse_numbers("Enter one or more numbers (floats ok): ", allow_float=True)
    if nums is None:
        return False
    print("\nMany-number methods:")
    print(f"  sum(nums)           -> {sum_builtin(nums)}")
    print(f"  reduce(add, nums)   -> {sum_reduce(nums)}")
    print(f"  math.fsum(nums)     -> {sum_fsum(nums)}")
    return True


def show_precision_demo() -> None:
    """Compare modern ``sum``, ``reduce``, and ``math.fsum`` on float input."""
    builtin, reduced, precise = precision_example_results()
    print("\nPrecision note:")
    print("  [1e16, 1.0, 1.0, 1.0, -1e16] mathematically totals 3.0")
    print(f"  sum(nums)           -> {builtin}")
    print(f"  reduce(add, nums)   -> {reduced}")
    print(f"  math.fsum(nums)     -> {precise}")
    print("  Modern Python improves float summation; reduce still adds naively.")


def main(argv: Sequence[str] | None = None) -> int:
    """Run the interactive lesson or one-shot command-line summation."""
    parser = build_argument_parser()
    arguments = parser.parse_args([] if argv is None else argv)
    if arguments.numbers is not None:
        if not arguments.numbers:
            parser.error("--numbers requires at least one number.")
        try:
            numbers = parse_cli_numbers(arguments.numbers, arguments.allow_float)
        except ValueError as exc:
            parser.error(str(exc))
        print(f"Sum: {sum_builtin(numbers)}")
        return 0
    if arguments.allow_float:
        parser.error("--float requires --numbers.")

    print("== Summing in Python: multiple approaches ==")
    if not show_two_number_demo():
        return 0
    if show_many_number_demo():
        show_precision_demo()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
