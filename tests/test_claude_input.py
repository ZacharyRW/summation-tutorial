"""Direct input-contract tests for the historical Claude variants."""

from unittest.mock import patch

import pytest

from history.claude_v1_integer_demo import get_number as get_number_v1
from history.claude_v2_multiple_numbers import (
    MAX_INPUT_COUNT as MAX_INPUT_COUNT_V2,
    get_multiple_numbers as get_multiple_numbers_v2,
    get_number as get_number_v2,
)
from history.claude_v3_menu_demo import (
    MAX_INPUT_COUNT as MAX_INPUT_COUNT_V3,
    get_multiple_numbers as get_multiple_numbers_v3,
    get_number as get_number_v3,
    main as main_v3,
)

pytestmark = pytest.mark.historical


def test_v1_retries_then_returns_an_integer():
    with patch("builtins.input", side_effect=["not-a-number", "-7"]):
        assert get_number_v1("Number: ") == -7


@pytest.mark.parametrize("get_number", [get_number_v2, get_number_v3])
def test_claude_integer_input_retries_then_returns_an_integer(get_number):
    with patch("builtins.input", side_effect=["not-a-number", "-7"]):
        assert get_number("Number: ", allow_float=False) == -7


@pytest.mark.parametrize("get_number", [get_number_v2, get_number_v3])
def test_claude_float_input_rejects_nonfinite_values(get_number):
    with patch("builtins.input", side_effect=["nan", "-2.5"]):
        assert get_number("Number: ") == -2.5


@pytest.mark.parametrize("get_number", [get_number_v1, get_number_v2, get_number_v3])
def test_claude_get_number_handles_eof(get_number):
    kwargs = {"allow_float": False} if get_number is not get_number_v1 else {}
    with patch("builtins.input", side_effect=EOFError):
        assert get_number("Number: ", **kwargs) is None


def test_v3_menu_handles_eof(capsys):
    with patch("builtins.input", side_effect=EOFError):
        main_v3()
    assert "Input closed. Exiting this demo." in capsys.readouterr().out


@pytest.mark.parametrize(
    ("get_multiple_numbers", "maximum"),
    [
        (get_multiple_numbers_v2, MAX_INPUT_COUNT_V2),
        (get_multiple_numbers_v3, MAX_INPUT_COUNT_V3),
    ],
)
def test_claude_multiple_number_limit_is_enforced(
    get_multiple_numbers, maximum, capsys
):
    assert get_multiple_numbers(0) is None
    assert get_multiple_numbers(maximum + 1) is None
    assert f"1 to {maximum}" in capsys.readouterr().out
