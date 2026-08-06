"""Historical pytest-style summation checks.

This snapshot is retained for provenance only.  The active core tests live in
``tests/test_summation_methods.py``; this root-level module is not collected
by the repository's pytest configuration.
"""
import math

import pytest

# Prevent collection if this module is ever imported by a test collector.
__test__ = False

from demos.summing_methods import (  # type: ignore
    add_operator,
    add_plus,
    add_sum,
    sum_builtin,
    sum_fsum,
    sum_reduce,
)

# ---------- Two-number methods ------------------------------------------------

@pytest.mark.parametrize("a,b", [
    (0, 0),
    (1, 2),
    (-5, 7),
    (1_000_000, 2_000_000),
    (3.5, 4.25),
])
def test_two_number_methods_agree(a, b):
    expected = a + b
    assert add_plus(a, b) == expected
    assert add_sum(a, b) == expected
    assert add_operator(a, b) == expected

# ---------- N-number variants: correctness -----------------------------------

@pytest.mark.parametrize("nums", [
    [],
    [0],
    [1],
    [1, 2, 3, 4, 5],
    list(range(100)),                 # 0..99
    [-1, -2, 3, 0, 10],
    [3.5, 4.25, -1.75, 0.0],
])
def test_n_number_methods(nums):
    # All should equal the mathematically expected sum.
    exp = sum(nums)
    assert sum_builtin(nums) == exp
    assert sum_reduce(nums) == exp
    # fsum returns float; coerce exp to float for numeric parity with tolerance.
    assert math.isclose(sum_fsum(nums), float(exp), rel_tol=0, abs_tol=1e-12)

# ---------- Empty and single-element edge cases -------------------------------

def test_empty_iterables_return_zero_like():
    assert sum_builtin([]) == 0
    assert sum_reduce([]) == 0
    assert sum_fsum([]) == 0.0

@pytest.mark.parametrize("x", [0, 1, -3, 2.5])
def test_single_element_lists(x):
    assert sum_builtin([x]) == x
    assert sum_reduce([x]) == x
    assert sum_fsum([x]) == float(x)

# ---------- Large inputs sanity/perf ------------------------------------------

def test_large_integer_range_sum_is_correct():
    # Sum of 0..n-1 = n*(n-1)/2
    n = 200_000
    nums = range(n)
    expected = n * (n - 1) // 2
    assert sum_builtin(nums) == expected
    assert sum_reduce(nums) == expected
    assert sum_fsum(nums) == float(expected)

# ---------- Float precision: fsum should be more stable -----------------------

def test_float_precision_fsum_better_or_equal():
    # Construct a numerically tricky sequence
    # Large + tiny numbers where naive summation can lose precision.
    nums = [1e16] + [1.0] * 10_000 + [-1e16]
    naive = sum_builtin(nums)
    precise = sum_fsum(nums)
    # Exact mathematical result is 10_000.0
    assert math.isclose(precise, 10_000.0, rel_tol=0, abs_tol=1e-12)
    # Built-in sum is allowed to be worse; it should not beat fsum here.
    # We assert fsum error <= builtin error.
    builtin_err = abs(naive - 10_000.0)
    fsum_err = abs(precise - 10_000.0)
    assert fsum_err <= builtin_err

# ---------- Type/robustness checks --------------------------------------------

def test_two_number_accepts_int_and_float():
    assert add_plus(2, 3.5) == 5.5
    assert add_sum(2.0, 3) == 5.0
    assert add_operator(2.0, 3.0) == 5.0

def test_no_nan_inf_in_variants():
    # Why: downstream code usually expects finite results
    nums = [1.0, 2.0, 3.0]
    assert math.isfinite(sum_builtin(nums))
    assert math.isfinite(sum_reduce(nums))
    assert math.isfinite(sum_fsum(nums))
