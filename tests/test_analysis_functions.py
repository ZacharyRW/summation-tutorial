"""Direct tests for the v3 sign-breakdown helper."""

import pytest

from history.claude_v3_menu_demo import analyze_numbers, method_positive_negative_demo

pytestmark = pytest.mark.historical


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        (
            [10, -5, 0, 3, -8, 0],
            {
                "total": 0,
                "positive": [10, 3],
                "negative": [-5, -8],
                "zeros": [0, 0],
                "positive_sum": 13,
                "negative_sum": -13,
                "positive_count": 2,
                "negative_count": 2,
                "zero_count": 2,
                "mean": 0.0,
                "median": 0.0,
                "minimum": -8,
                "maximum": 10,
            },
        ),
        (
            [],
            {
                "total": 0,
                "positive": [],
                "negative": [],
                "zeros": [],
                "positive_sum": 0,
                "negative_sum": 0,
                "positive_count": 0,
                "negative_count": 0,
                "zero_count": 0,
                "mean": None,
                "median": None,
                "minimum": None,
                "maximum": None,
            },
        ),
    ],
)
def test_analyze_numbers_uses_v3_source(numbers, expected):
    assert analyze_numbers(numbers) == expected


@pytest.mark.parametrize(
    ("numbers", "error"),
    [([1, float("inf")], ValueError), ([1, "two"], TypeError)],
)
def test_analyze_numbers_rejects_values_outside_its_numeric_contract(numbers, error):
    with pytest.raises(error):
        analyze_numbers(numbers)


def test_positive_negative_menu_displays_summary_statistics(monkeypatch, capsys):
    responses = iter(["3", "-2", "0", "4"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(responses))

    method_positive_negative_demo()

    output = capsys.readouterr().out
    assert "Summary statistics:" in output
    assert "Mean:" in output
    assert "Median:" in output
    assert "Minimum:" in output
    assert "Maximum:" in output
