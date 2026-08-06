"""Tests for the canonical lesson's one-shot command-line interface."""

import pytest

from demos.summing_methods import main, parse_cli_numbers


def test_cli_sums_exact_integers(capsys):
    """One-shot integer mode preserves exact Python integer arithmetic."""
    assert main(["--numbers", "9007199254740993", "1"]) == 0
    assert capsys.readouterr().out == "Sum: 9007199254740994\n"


def test_cli_sums_finite_floats(capsys):
    """Float mode accepts finite values and reports their built-in sum."""
    assert main(["--float", "--numbers", "1.5", "2.25"]) == 0
    assert capsys.readouterr().out == "Sum: 3.75\n"


@pytest.mark.parametrize("value", ["nan", "inf", "-inf"])
def test_cli_rejects_nonfinite_floats(value, capsys):
    """Float command-line input follows the interactive finite-number rule."""
    with pytest.raises(SystemExit) as error:
        main(["--float", "--numbers", value])

    assert error.value.code == 2
    assert "valid finite number" in capsys.readouterr().err


def test_cli_rejects_fractional_integer_input(capsys):
    """Default command-line mode accepts whole numbers only."""
    with pytest.raises(SystemExit) as error:
        main(["--numbers", "1.5"])

    assert error.value.code == 2
    assert "valid whole number" in capsys.readouterr().err


def test_float_flag_requires_one_shot_numbers(capsys):
    """The float parser flag is not silently ignored in interactive mode."""
    with pytest.raises(SystemExit) as error:
        main(["--float"])

    assert error.value.code == 2
    assert "--float requires --numbers" in capsys.readouterr().err


def test_parse_cli_numbers_returns_typed_values():
    """The parser is directly testable outside the argparse boundary."""
    integers = parse_cli_numbers(["1", "2"], allow_float=False)
    assert integers == [1, 2]
    assert all(isinstance(number, int) for number in integers)

    assert parse_cli_numbers(["1.5", "2"], allow_float=True) == [1.5, 2.0]
