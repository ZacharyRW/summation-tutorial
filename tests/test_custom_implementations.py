"""Direct tests for the extracted Claude custom-sum helpers."""

import pytest

from history.claude_v2_multiple_numbers import custom_sum as custom_sum_v2
from history.claude_v3_menu_demo import custom_sum as custom_sum_v3

pytestmark = pytest.mark.historical


@pytest.mark.parametrize("numbers", [[], [5], [1, 2, 3], [-5, 2, 3], [1.5, 2.5]])
@pytest.mark.parametrize("custom_sum", [custom_sum_v2, custom_sum_v3])
def test_custom_sum_uses_source_implementations(custom_sum, numbers):
    assert custom_sum(numbers) == sum(numbers)
