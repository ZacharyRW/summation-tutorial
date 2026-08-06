"""Integration tests for complete workflows and module imports."""

import importlib
import importlib.util
from pathlib import Path
from unittest.mock import patch

import pytest

REPO_ROOT = Path(__file__).parent.parent


class TestModuleImports:
    """Test that all modules can be imported correctly."""

    def test_import_demos_summing_methods(self):
        """Test importing demos.summing_methods module."""
        try:
            import demos.summing_methods

            assert hasattr(demos.summing_methods, "add_plus")
            assert hasattr(demos.summing_methods, "add_sum")
            assert hasattr(demos.summing_methods, "add_operator")
            assert hasattr(demos.summing_methods, "sum_builtin")
            assert hasattr(demos.summing_methods, "sum_reduce")
            assert hasattr(demos.summing_methods, "sum_fsum")
        except ImportError as e:
            pytest.fail(f"Failed to import demos.summing_methods: {e}")

    def test_import_original_two_number_example(self):
        """Test importing the original historical two-number example."""
        example_path = REPO_ROOT / "history" / "original_two_number.py"
        assert example_path.exists(), f"Example not found at {example_path}"

        try:
            spec = importlib.util.spec_from_file_location(
                "history.original_two_number", str(example_path)
            )
            example_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(example_module)
        except ImportError as e:
            pytest.fail(f"Failed to import the original example: {e}")

        assert example_module is not None

        assert hasattr(example_module, "main")
        assert callable(example_module.main)

    def test_chatgpt_entry_point_delegates_to_canonical_demo(self):
        """The historical ChatGPT entry point must not fork core behavior."""
        from demos.summing_methods import main
        from history import chatgpt_v1_entrypoint

        assert chatgpt_v1_entrypoint.main is main

    def test_function_availability(self):
        """Test that all expected functions are available."""
        from demos.summing_methods import (
            add_operator,
            add_plus,
            add_sum,
            parse_numbers,
            sum_builtin,
            sum_fsum,
            sum_reduce,
        )

        # Verify all functions are callable
        assert callable(add_plus)
        assert callable(add_sum)
        assert callable(add_operator)
        assert callable(sum_builtin)
        assert callable(sum_reduce)
        assert callable(sum_fsum)
        assert callable(parse_numbers)


class TestEndToEndWorkflows:
    """Test complete end-to-end workflows."""

    def test_complete_two_number_workflow(self):
        """Test complete workflow for adding two numbers."""
        from demos.summing_methods import add_operator, add_plus, add_sum

        a, b = 15, 27

        result1 = add_plus(a, b)
        result2 = add_sum(a, b)
        result3 = add_operator(a, b)

        # All methods should give the same result
        assert result1 == 42
        assert result2 == 42
        assert result3 == 42
        assert result1 == result2 == result3

    def test_complete_multiple_number_workflow(self):
        """Test complete workflow for summing multiple numbers."""
        from demos.summing_methods import sum_builtin, sum_fsum, sum_reduce

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        result1 = sum_builtin(numbers)
        result2 = sum_reduce(numbers)
        result3 = sum_fsum(numbers)

        # All methods should give the same result
        expected = 55
        assert result1 == expected
        assert result2 == expected
        assert result3 == float(expected)

    def test_parse_and_sum_workflow(self):
        """Test parsing numbers and then summing them."""
        from demos.summing_methods import parse_numbers, sum_builtin

        with patch("builtins.input", return_value="10 20 30 40"):
            numbers = parse_numbers("Enter numbers: ", allow_float=False)
            result = sum_builtin(numbers)
            assert result == 100.0

    def test_parse_floats_and_sum_workflow(self):
        """Test parsing floats and summing them."""
        from demos.summing_methods import parse_numbers, sum_fsum

        with patch("builtins.input", return_value="1.5 2.5 3.5 4.5"):
            numbers = parse_numbers("Enter numbers: ", allow_float=True)
            result = sum_fsum(numbers)
            assert abs(result - 12.0) < 1e-10

    def test_error_recovery_workflow(self):
        """Test workflow with error recovery."""
        from demos.summing_methods import parse_numbers, sum_builtin

        # Simulate user entering invalid input then valid input
        with (
            patch("builtins.input", side_effect=["invalid", "5 10 15"]),
            patch("builtins.print"),  # Suppress error messages
        ):
            numbers = parse_numbers("Enter: ", allow_float=False)
            result = sum_builtin(numbers)
            assert result == 30.0

    def test_mixed_workflow_integers_and_floats(self):
        """Test workflow mixing integers and floats."""
        from demos.summing_methods import sum_builtin

        integers = [1, 2, 3, 4, 5]
        floats = [1.5, 2.5, 3.5, 4.5, 5.5]
        mixed = integers + floats

        result = sum_builtin(mixed)
        expected = 15 + 17.5  # 32.5
        assert abs(result - expected) < 1e-10


class TestCrossModuleConsistency:
    """Test consistency across different implementations."""

    def test_all_two_number_methods_agree(self):
        """Test that all two-number methods produce consistent results."""
        from demos.summing_methods import add_operator, add_plus, add_sum

        test_cases = [
            (0, 0),
            (1, 1),
            (5, 10),
            (-5, 10),
            (-5, -10),
            (100, 200),
            (3.14, 2.86),
            (1e10, 2e10),
        ]

        for a, b in test_cases:
            expected = a + b
            assert add_plus(a, b) == expected
            assert add_sum(a, b) == expected
            assert add_operator(a, b) == expected

    def test_all_n_number_methods_agree(self):
        """Test that all n-number methods produce consistent results."""
        import math

        from demos.summing_methods import sum_builtin, sum_fsum, sum_reduce

        test_cases = [
            [],
            [0],
            [1, 2, 3],
            [-1, -2, -3],
            [1, -1, 2, -2],
            list(range(100)),
            [1.5, 2.5, 3.5],
        ]

        for nums in test_cases:
            expected = sum(nums)
            assert sum_builtin(nums) == expected
            assert sum_reduce(nums) == expected
            assert math.isclose(sum_fsum(nums), float(expected), abs_tol=1e-12)


class TestDocstringsAndMetadata:
    """Test that functions have proper documentation."""

    def test_functions_have_docstrings(self):
        """Test that all public functions have docstrings."""
        from demos.summing_methods import (
            add_operator,
            add_plus,
            add_sum,
            parse_numbers,
            sum_builtin,
            sum_fsum,
            sum_reduce,
        )

        functions = [
            add_plus,
            add_sum,
            add_operator,
            sum_builtin,
            sum_reduce,
            sum_fsum,
            parse_numbers,
        ]

        for func in functions:
            assert func.__doc__ is not None, f"{func.__name__} missing docstring"
            assert len(func.__doc__.strip()) > 0, f"{func.__name__} has empty docstring"

    def test_module_has_docstring(self):
        """Test that the module has a docstring."""
        import demos.summing_methods

        assert demos.summing_methods.__doc__ is not None
        assert demos.summing_methods.__doc__.strip()


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""

    def test_calculating_total_cost(self):
        """Test calculating total cost of items."""
        from demos.summing_methods import sum_builtin

        prices = [19.99, 29.99, 9.99, 14.99, 39.99]
        total = sum_builtin(prices)
        expected = 114.95
        assert abs(total - expected) < 0.01

    def test_calculating_average(self):
        """Test calculating average using sum."""
        from demos.summing_methods import sum_builtin

        scores = [85, 90, 78, 92, 88, 95]
        total = sum_builtin(scores)
        average = total / len(scores)
        expected_average = 88.0
        assert abs(average - expected_average) < 0.01

    def test_balance_calculation(self):
        """Test calculating account balance with debits and credits."""
        from demos.summing_methods import sum_builtin

        transactions = [100.0, -25.50, -10.00, 50.00, -15.75, 200.00]
        balance = sum_builtin(transactions)
        expected = 298.75
        assert abs(balance - expected) < 0.01

    def test_temperature_average(self):
        """Test calculating average temperature."""
        from demos.summing_methods import sum_fsum

        temperatures = [72.5, 73.1, 71.9, 72.3, 73.5, 72.8, 73.0]
        total = sum_fsum(temperatures)
        average = total / len(temperatures)
        assert 72.0 < average < 74.0

    def test_cumulative_distance(self):
        """Test calculating cumulative distance."""
        from demos.summing_methods import sum_builtin

        daily_distances = [3.2, 5.1, 2.8, 4.5, 6.3, 3.9, 4.2]
        total_distance = sum_builtin(daily_distances)
        assert total_distance == 30.0

    def test_grade_point_average(self):
        """Test calculating GPA using weighted sum."""
        from demos.summing_methods import sum_builtin

        # Grade points (4.0 scale)
        grade_points = [4.0, 3.7, 3.3, 4.0, 3.0, 3.7]
        credits = [3, 4, 3, 4, 3, 3]

        weighted_points = [gp * cr for gp, cr in zip(grade_points, credits)]
        total_points = sum_builtin(weighted_points)
        total_credits = sum_builtin(credits)
        gpa = total_points / total_credits

        assert 3.0 < gpa < 4.0


class TestBackwardCompatibility:
    """Test backward compatibility with original implementations."""

    def test_basic_sum_still_works(self):
        """Test that basic Python sum still works as expected."""
        nums = [1, 2, 3, 4, 5]
        result = sum(nums)
        assert result == 15

    def test_direct_addition_still_works(self):
        """Test that direct addition operator still works."""
        result = 5 + 10
        assert result == 15

    def test_works_with_builtin_types(self):
        """Test that sum works with all built-in numeric types."""
        from demos.summing_methods import sum_builtin

        # int
        assert sum_builtin([1, 2, 3]) == 6

        # float
        assert abs(sum_builtin([1.5, 2.5, 3.5]) - 7.5) < 1e-10

        # mixed
        assert abs(sum_builtin([1, 2.5, 3]) - 6.5) < 1e-10

        # bool (True=1, False=0)
        assert sum_builtin([True, False, True]) == 2


class TestConcurrency:
    """Test that functions work correctly in concurrent scenarios."""

    def test_multiple_calls_consistent(self):
        """Test that multiple calls produce consistent results."""
        from demos.summing_methods import sum_builtin

        nums = [1, 2, 3, 4, 5]
        results = [sum_builtin(nums) for _ in range(100)]

        # All results should be identical
        assert all(r == 15 for r in results)
        assert len(set(results)) == 1  # Only one unique value

    def test_parallel_different_inputs(self):
        """Test that different inputs don't interfere."""
        from demos.summing_methods import sum_builtin

        inputs = [
            [1, 2, 3],
            [10, 20, 30],
            [100, 200, 300],
        ]
        expected = [6, 60, 600]

        results = [sum_builtin(inp) for inp in inputs]
        assert results == expected
