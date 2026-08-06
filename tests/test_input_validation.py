"""Tests for input validation functions."""

from unittest.mock import patch

import pytest

from demos.summing_methods import main, parse_numbers, show_two_number_demo


def assert_exact_integer_result(result, expected):
    """Assert the integer parser preserved values and Python ``int`` types."""
    assert result == expected
    assert result is not None
    assert all(isinstance(number, int) for number in result)


class TestParseNumbers:
    """Test the parse_numbers function from demos.summing_methods."""

    def test_parse_single_integer(self):
        """Test parsing a single integer."""
        with patch("builtins.input", return_value="42"):
            result = parse_numbers("Enter: ", allow_float=False)
            assert_exact_integer_result(result, [42])

    def test_parse_multiple_integers(self):
        """Test parsing multiple space-separated integers."""
        with patch("builtins.input", return_value="10 20 30"):
            result = parse_numbers("Enter: ", allow_float=False)
            assert_exact_integer_result(result, [10, 20, 30])

    def test_parse_single_float(self):
        """Test parsing a single float."""
        with patch("builtins.input", return_value="3.14"):
            result = parse_numbers("Enter: ", allow_float=True)
            assert result == [3.14]

    def test_parse_multiple_floats(self):
        """Test parsing multiple floats."""
        with patch("builtins.input", return_value="1.5 2.7 3.9"):
            result = parse_numbers("Enter: ", allow_float=True)
            assert result == [1.5, 2.7, 3.9]

    def test_parse_negative_numbers(self):
        """Test parsing negative numbers."""
        with patch("builtins.input", return_value="-5 -10 15"):
            result = parse_numbers("Enter: ", allow_float=False)
            assert_exact_integer_result(result, [-5, -10, 15])

    def test_parse_mixed_positive_negative_floats(self):
        """Test parsing mixed positive and negative floats."""
        with patch("builtins.input", return_value="-3.5 4.25 0 -1.75"):
            result = parse_numbers("Enter: ", allow_float=True)
            assert result == [-3.5, 4.25, 0.0, -1.75]

    def test_parse_zero(self):
        """Test parsing zero."""
        with patch("builtins.input", return_value="0"):
            result = parse_numbers("Enter: ", allow_float=False)
            assert_exact_integer_result(result, [0])

    def test_parse_large_numbers(self):
        """Test parsing large numbers."""
        with patch("builtins.input", return_value="1000000 2000000"):
            result = parse_numbers("Enter: ", allow_float=False)
            assert_exact_integer_result(result, [1_000_000, 2_000_000])

    def test_integer_mode_preserves_large_integer_precision(self):
        """Integer parsing must not round values larger than 2**53."""
        with patch("builtins.input", return_value="9007199254740993 1"):
            result = parse_numbers("Enter: ", allow_float=False)
            assert_exact_integer_result(result, [9_007_199_254_740_993, 1])

    def test_parse_scientific_notation(self):
        """Test parsing scientific notation (only with allow_float=True)."""
        with patch("builtins.input", return_value="1e10 3.5e-2"):
            result = parse_numbers("Enter: ", allow_float=True)
            assert result == [1e10, 3.5e-2]

    def test_reject_float_when_not_allowed(self):
        """Test that floats are rejected when allow_float=False."""
        # First attempt with float (invalid), then valid input
        with (
            patch("builtins.input", side_effect=["3.14", "3"]),
            patch("builtins.print") as mock_print,
        ):
            result = parse_numbers("Enter: ", allow_float=False)
            assert_exact_integer_result(result, [3])
            # Verify error message was printed
            mock_print.assert_called()

    def test_retry_on_invalid_input(self):
        """Test retry behavior on invalid input."""
        # First attempt invalid, second attempt valid
        with (
            patch("builtins.input", side_effect=["abc", "42"]),
            patch("builtins.print") as mock_print,
        ):
            result = parse_numbers("Enter: ", allow_float=False)
            assert_exact_integer_result(result, [42])
            # Verify error message was printed
            mock_print.assert_called()

    def test_retry_on_empty_input(self):
        """Test retry behavior on empty input."""
        with (
            patch("builtins.input", side_effect=["", "10 20"]),
            patch("builtins.print") as mock_print,
        ):
            result = parse_numbers("Enter: ", allow_float=False)
            assert_exact_integer_result(result, [10, 20])
            # Verify prompt was shown
            mock_print.assert_called()

    def test_reject_nan_in_integer_mode(self):
        """Test that 'nan' is rejected in integer mode."""
        with (
            patch("builtins.input", side_effect=["nan", "42"]),
            patch("builtins.print") as mock_print,
        ):
            result = parse_numbers("Enter: ", allow_float=False)
            assert_exact_integer_result(result, [42])
            mock_print.assert_called()

    def test_reject_inf_in_integer_mode(self):
        """Test that 'inf' is rejected in integer mode."""
        with (
            patch("builtins.input", side_effect=["inf", "42"]),
            patch("builtins.print") as mock_print,
        ):
            result = parse_numbers("Enter: ", allow_float=False)
            assert result == [42.0]
            mock_print.assert_called()

    @pytest.mark.parametrize("nonfinite", ["nan", "inf", "-inf"])
    def test_reject_nonfinite_float_input(self, nonfinite):
        """Float mode accepts finite values only."""
        with (
            patch("builtins.input", side_effect=[nonfinite, "1.25"]),
            patch("builtins.print") as mock_print,
        ):
            assert parse_numbers("Enter: ", allow_float=True) == [1.25]
            mock_print.assert_called()

    def test_eof_returns_none_with_friendly_message(self):
        """Closed standard input should not leak an EOFError."""
        with (
            patch("builtins.input", side_effect=EOFError),
            patch("builtins.print") as mock_print,
        ):
            assert parse_numbers("Enter: ", allow_float=False) is None
            mock_print.assert_called_with("Input closed. Exiting this demo.")

    def test_whitespace_handling(self):
        """Test handling of extra whitespace."""
        with patch("builtins.input", return_value="  10   20  30  "):
            result = parse_numbers("Enter: ", allow_float=False)
            assert_exact_integer_result(result, [10, 20, 30])

    def test_leading_zeros(self):
        """Test handling of leading zeros."""
        with patch("builtins.input", return_value="007 0123"):
            result = parse_numbers("Enter: ", allow_float=False)
            assert_exact_integer_result(result, [7, 123])

    def test_negative_zero(self):
        """Test parsing negative zero."""
        with patch("builtins.input", return_value="-0"):
            result = parse_numbers("Enter: ", allow_float=True)
            assert result == [-0.0]


def test_two_number_demo_retries_after_one_number_input(capsys):
    """The two-number demo should not crash when given only one integer."""
    with patch("builtins.input", side_effect=["5", "3 5"]):
        show_two_number_demo()

    output = capsys.readouterr().out
    assert "Please enter exactly two integers separated by spaces." in output
    assert "a + b               -> 8" in output


def test_main_stops_after_eof_in_the_first_demo(capsys):
    with patch("builtins.input", side_effect=EOFError):
        main()

    assert capsys.readouterr().out.count("Input closed. Exiting this demo.") == 1
