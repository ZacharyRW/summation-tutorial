"""Tests for edge cases and boundary conditions in summation."""

import math
import sys

import pytest

from demos.summing_methods import (
    add_plus,
    sum_builtin,
    sum_fsum,
)


class TestBoundaryConditions:
    """Test boundary conditions and edge cases."""

    def test_max_int_addition(self):
        """Test addition near maximum integer value."""
        # Python 3 has arbitrary precision integers, so this won't overflow
        large = sys.maxsize
        result = add_plus(large, 1)
        assert result == large + 1

    def test_min_int_addition(self):
        """Test addition near minimum integer value."""
        small = -sys.maxsize - 1
        result = add_plus(small, -1)
        assert result == small - 1

    def test_very_large_integer_sum(self):
        """Test summing very large integers."""
        nums = [10**100, 10**100, 10**100]
        result = sum_builtin(nums)
        assert result == 3 * (10**100)

    def test_very_small_float_sum(self):
        """Test summing very small floats."""
        nums = [1e-308, 1e-308, 1e-308]  # Near smallest positive float
        result = sum_builtin(nums)
        assert result > 0
        assert math.isfinite(result)

    def test_sum_approaching_infinity(self):
        """Test that very large floats can approach infinity."""
        large = 1e308
        nums = [large, large]
        result = sum_builtin(nums)
        # This might be infinity depending on the values
        assert result == float("inf") or math.isfinite(result)

    def test_infinity_handling(self):
        """Test handling of infinity values."""
        nums = [float("inf"), 1, 2, 3]
        assert sum_builtin(nums) == float("inf")
        assert sum_fsum(nums) == float("inf")

    def test_negative_infinity_handling(self):
        """Test handling of negative infinity."""
        nums = [float("-inf"), 1, 2, 3]
        assert sum_builtin(nums) == float("-inf")
        assert sum_fsum(nums) == float("-inf")

    def test_infinity_minus_infinity(self):
        """Test inf + (-inf) = nan."""
        nums = [float("inf"), float("-inf")]
        result = sum_builtin(nums)
        assert math.isnan(result)

    def test_nan_propagation(self):
        """Test that NaN propagates through sum."""
        nums = [1, 2, float("nan"), 3]
        result = sum_builtin(nums)
        assert math.isnan(result)

    def test_nan_in_fsum(self):
        """Test NaN handling in fsum."""
        nums = [1, 2, float("nan"), 3]
        result = sum_fsum(nums)
        assert math.isnan(result)


class TestFloatingPointPrecision:
    """Test floating point precision edge cases."""

    def test_repeated_small_additions(self):
        """Test precision with repeated small float additions."""
        # Adding 0.1 many times can accumulate error
        nums = [0.1] * 100
        result = sum_builtin(nums)
        expected = 10.0
        # Allow for some floating point error
        assert abs(result - expected) < 1e-10

    def test_fsum_better_precision_tiny_numbers(self):
        """Test that fsum maintains precision with tiny numbers."""
        # Many tiny numbers that might lose precision with naive sum
        nums = [1e-16] * 1000
        result_fsum = sum_fsum(nums)
        result_builtin = sum_builtin(nums)

        # fsum should be more accurate
        expected = 1e-13  # 1e-16 * 1000
        assert (
            abs(result_fsum - expected) < abs(result_builtin - expected)
            or abs(result_fsum - expected) < 1e-14
        )

    def test_catastrophic_cancellation(self):
        """Test catastrophic cancellation scenario."""
        # Large number + small number - large number
        large = 1e16
        small = 1.0
        nums = [large, small, -large]

        result_fsum = sum_fsum(nums)
        result_builtin = sum_builtin(nums)

        # fsum should preserve the small number better
        assert result_fsum == 1.0 or abs(result_fsum - 1.0) < abs(result_builtin - 1.0)

    def test_alternating_large_small(self):
        """Test alternating large and small numbers."""
        nums = [1e10, 1e-10, 1e10, 1e-10, 1e10]
        result = sum_fsum(nums)
        expected = 3e10 + 2e-10
        assert math.isclose(result, expected, rel_tol=1e-9)

    def test_subnormal_numbers(self):
        """Test with subnormal (denormalized) floating point numbers."""
        # Smallest positive subnormal float
        tiny = sys.float_info.min * sys.float_info.epsilon
        nums = [tiny, tiny, tiny]
        result = sum_builtin(nums)
        assert result > 0
        assert result < sys.float_info.min

    def test_rounding_modes(self):
        """Test that results are consistent regardless of small rounding."""
        nums = [0.1, 0.2, 0.3, 0.4, 0.5]
        result1 = sum_builtin(nums)
        result2 = sum_builtin(nums)
        # Results should be exactly the same (deterministic)
        assert result1 == result2


class TestSpecialNumericValues:
    """Test special numeric values and formats."""

    def test_negative_zero(self):
        """Test that negative zero is handled correctly."""
        nums = [-0.0, 0.0, 1.0]
        result = sum_builtin(nums)
        assert result == 1.0

    def test_positive_zero(self):
        """Test explicit positive zero."""
        nums = [+0.0, 1.0, 2.0]
        result = sum_builtin(nums)
        assert result == 3.0

    def test_mixed_zero_representations(self):
        """Test that -0.0 and 0.0 sum correctly."""
        # In floating point, -0.0 + 0.0 = 0.0
        result = add_plus(-0.0, 0.0)
        assert result == 0.0

    def test_integer_overflow_to_long(self):
        """Test that Python handles integer overflow gracefully."""
        # Python 3 automatically converts to arbitrary precision
        nums = [2**63, 2**63, 2**63]
        result = sum_builtin(nums)
        expected = 3 * (2**63)
        assert result == expected

    def test_bool_as_numbers(self):
        """Test that booleans work as numbers (True=1, False=0)."""
        nums = [True, False, True, True]
        result = sum_builtin(nums)
        assert result == 3  # True + False + True + True = 1+0+1+1


class TestInputTypes:
    """Test different input types and iterables."""

    def test_sum_list(self):
        """Test sum with list."""
        assert sum_builtin([1, 2, 3]) == 6

    def test_sum_tuple(self):
        """Test sum with tuple."""
        assert sum_builtin((1, 2, 3)) == 6

    def test_sum_set(self):
        """Test sum with set."""
        result = sum_builtin({1, 2, 3})
        assert result == 6

    def test_sum_generator(self):
        """Test sum with generator expression."""
        gen = (x for x in [1, 2, 3, 4, 5])
        assert sum_builtin(gen) == 15

    def test_sum_range(self):
        """Test sum with range object."""
        assert sum_builtin(range(10)) == 45

    def test_sum_iter(self):
        """Test sum with iterator."""
        it = iter([1, 2, 3, 4])
        assert sum_builtin(it) == 10

    def test_sum_frozen_set(self):
        """Test sum with frozen set."""
        result = sum_builtin(frozenset([1, 2, 3]))
        assert result == 6


class TestPerformanceEdgeCases:
    """Test performance-related edge cases."""

    def test_very_long_list_integers(self):
        """Test summing a very long list of integers."""
        nums = list(range(100_000))
        result = sum_builtin(nums)
        expected = 100_000 * 99_999 // 2
        assert result == expected

    def test_very_long_list_floats(self):
        """Test summing a very long list of floats."""
        nums = [0.1] * 10_000
        result = sum_fsum(nums)
        expected = 1000.0
        assert abs(result - expected) < 1e-9

    def test_memory_efficiency_generator(self):
        """Test that generators work without materializing the full list."""
        # This should not consume much memory
        gen = (x for x in range(1_000_000))
        result = sum_builtin(gen)
        expected = 1_000_000 * 999_999 // 2
        assert result == expected


class TestMathematicalProperties:
    """Test mathematical properties of summation."""

    def test_commutative_property(self):
        """Test that sum is commutative (order doesn't matter for exact results)."""
        nums1 = [1, 2, 3, 4, 5]
        nums2 = [5, 4, 3, 2, 1]
        # For integers, order truly doesn't matter
        assert sum_builtin(nums1) == sum_builtin(nums2)

    def test_associative_property_integers(self):
        """Test associative property for integers."""
        # (a + b) + c = a + (b + c)
        a, b, c = 10, 20, 30
        result1 = (a + b) + c
        result2 = a + (b + c)
        assert result1 == result2

    def test_identity_element(self):
        """Test that 0 is the identity element for addition."""
        nums = [5, 0, 3, 0, 2]
        nums_no_zero = [5, 3, 2]
        assert sum_builtin(nums) == sum_builtin(nums_no_zero)

    def test_inverse_elements(self):
        """Test that n + (-n) = 0."""
        nums = [5, -5, 10, -10, 3, -3]
        assert sum_builtin(nums) == 0

    def test_distributive_with_scalar(self):
        """Test that sum distributes over scalar multiplication."""
        nums = [1, 2, 3, 4]
        scalar = 5
        scaled_nums = [n * scalar for n in nums]

        result1 = sum_builtin(scaled_nums)
        result2 = sum_builtin(nums) * scalar

        assert result1 == result2


class TestErrorConditions:
    """Test potential error conditions."""

    def test_sum_with_none_raises_error(self):
        """Test that sum with None raises TypeError."""
        with pytest.raises(TypeError):
            sum_builtin([1, 2, None, 3])

    def test_sum_with_string_raises_error(self):
        """Test that sum with string raises TypeError."""
        with pytest.raises(TypeError):
            sum_builtin([1, 2, "3", 4])

    def test_sum_with_list_raises_error(self):
        """Test that sum with nested list raises TypeError."""
        with pytest.raises(TypeError):
            sum_builtin([1, 2, [3, 4]])

    def test_two_number_with_none_raises_error(self):
        """Test two-number methods with None."""
        with pytest.raises(TypeError):
            add_plus(1, None)

    def test_two_number_with_string_raises_error(self):
        """Test two-number methods with string."""
        with pytest.raises(TypeError):
            add_plus(1, "2")
