# Summation Tutorial

An educational Python summation tutorial. The maintained lesson is
`demos/summing_methods.py`; the [`history/`](history/) package contains
runnable historical AI-assisted iterations retained for comparison and
provenance.

## Files

| File | Description |
|---|---|
| `demos/summing_methods.py` | Canonical reusable summation lesson and interactive demo |
| `history/` | Historical runnable examples and a former-name mapping |
| `history/chatgpt_v1_entrypoint.py` | Historical ChatGPT entry point that runs the canonical lesson |
| `history/original_two_number.py` | Historical original two-number CLI example |
| `history/claude_v1_integer_demo.py` | Historical Claude v1 integer-input demonstration |
| `history/claude_v2_multiple_numbers.py` | Historical Claude v2 float and multiple-number demonstration |
| `history/claude_v3_menu_demo.py` | Historical Claude v3 menu and sign-analysis demonstration |
| `history/chatgpt_v2_test_snapshot.py` | Historical pytest snapshot; not part of the active test suite |

## Summation Methods Demonstrated

- Direct addition: `a + b`
- Built-in: `sum([a, b])`
- Manual loop accumulation
- Functional: `reduce(operator.add, nums, 0)`
- High precision: `math.fsum(nums)`

## Input Behavior

- Integer prompts accept whole numbers and preserve their exact Python `int`
  value, including values above `2**53`.
- Float prompts accept finite values only; `nan`, `inf`, and `-inf` are
  rejected.
- Closing standard input ends the current demo with a friendly message instead
  of a traceback.
- The count-based Claude v2/v3 examples accept from 1 to 100 values per run.

## Tests

The repository includes a pytest suite covering core summation behavior, input validation, edge cases, and integration paths. `tests/test_summation_methods.py` is the single active core arithmetic suite; `history/chatgpt_v2_test_snapshot.py` is retained only as a historical test snapshot. The project requires Python 3.12 or later. Current test totals and coverage are not claimed until CI-generated results are available.

CI runs the test and Ruff lint/format checks on Python 3.12, 3.13, and 3.14.
It also executes the historical-progression notebook on Python 3.14. The
source-only tutorial does not run a package build.

```bash
# Create a repository-local environment and install the declared toolchain
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements-dev.txt

# Run all tests
./.venv/bin/python -m pytest tests/

# Run with verbose output
./.venv/bin/python -m pytest tests/ -v

# Run the configured linter
./.venv/bin/python -m ruff check .

# Check formatting for maintained Python sources and active tests
./.venv/bin/python -m ruff format --check .
```

## Formatting policy

Ruff formatting is enforced for the maintained lesson and active test suite.
The preserved `history/` artifacts and the historical-progression notebook are
excluded to retain their archival presentation; they remain subject to Ruff
lint. Run `./.venv/bin/python -m ruff format demos tests` when intentionally
reformatting maintained Python files.

## Package-build status

This is a source-based tutorial, not a distributable package. Its
`pyproject.toml` contains only pytest and Ruff configuration; the repository
does not define a package build backend or publish wheels/source distributions.
Do not rely on `pip install .` as a supported workflow. Any move to
distribution support will add and validate the necessary build path before it
is documented as supported.

## Command-line use

Running the module with no arguments starts the interactive lesson. For a
scriptable one-shot sum, pass one or more values with `--numbers`:

```bash
# Exact integer arithmetic (the default)
python -m demos.summing_methods --numbers 9007199254740993 1

# Finite floating-point input
python -m demos.summing_methods --float --numbers 1.5 2.25
```

`--numbers` rejects fractional values by default. `--float` accepts only finite
floating-point values; `nan`, `inf`, and `-inf` are rejected. File input is not
part of the current CLI contract.

## Historical progression notebook

[`notebooks/historical_progression.ipynb`](notebooks/historical_progression.ipynb)
is an optional, executable walkthrough from the original two-number example
through the historical Claude variants to the maintained canonical lesson. It
links to the current paths and the former-name mapping in
[`history/README.md`](history/README.md); historical modules are comparison
artifacts, not alternatives to `demos/summing_methods.py`.

To execute it from a clean checkout, install the tutorial's development tools
and its optional notebook dependency, then run it from the repository root:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements-dev.txt
./.venv/bin/python -m pip install -r requirements-notebook.txt
./.venv/bin/python -m jupyter nbconvert --to notebook --execute \
  --output historical_progression.executed.ipynb --output-dir /tmp \
  notebooks/historical_progression.ipynb
```

The command was verified successfully on 2026-08-05 with Python 3.14.6,
Jupyter nbconvert 7.17.1, and the declared notebook dependencies. The
generated `/tmp/historical_progression.executed.ipynb` is a disposable
verification artifact and is not tracked.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
