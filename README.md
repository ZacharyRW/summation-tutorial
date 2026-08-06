# Summation Tutorial

An educational Python summation tutorial. The maintained lesson is
`demos/summing_methods.py`; the [`history/`](history/) package contains
runnable historical AI-assisted iterations retained for comparison and
provenance.

## Project scope

This is a local, source-based tutorial for Python 3.12+. It intentionally does
not provide a distributable package, file input, network integration,
persistence, or hosted execution. The maintained lesson and its tests are
separate from the runnable historical artifacts. See [ANALYSIS.md](ANALYSIS.md)
for the current assessment and [ROADMAP.md](ROADMAP.md) for conditional future
work.

## Contributions

This is a maintainer-led educational archive and is not currently accepting
outside contributions. Please do not open pull requests or expect public
contributor support.

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

## Floating-point precision

For ordinary values, `sum`, `reduce(operator.add, ...)`, and `math.fsum` agree.
Floating-point rounding can make their results differ, though. The interactive
lesson includes this reproducible example:

```python
from demos.summing_methods import precision_example_results

assert precision_example_results() == (3.0, 0.0, 3.0)
```

The mathematical total is `3.0`. On supported modern Python versions, builtin
`sum` uses improved float summation and matches `math.fsum` here; the direct
`reduce(operator.add, ...)` accumulation loses the small values beside `1e16`.
Use `math.fsum` when improved floating-point accuracy matters, especially when
you need its documented numerical behavior across input patterns.

## Input Behavior

- Integer prompts accept whole numbers and preserve their exact Python `int`
  value, including values above `2**53`.
- Float prompts accept finite values only; `nan`, `inf`, and `-inf` are
  rejected.
- Closing standard input ends the current demo with a friendly message instead
  of a traceback.
- The count-based Claude v2/v3 examples accept from 1 to 100 values per run.

## Tests

The repository includes a pytest suite covering core summation behavior, input
validation, edge cases, and integration paths. `tests/test_summation_methods.py`
is the active core arithmetic suite; `history/chatgpt_v2_test_snapshot.py` is
retained only as a historical test snapshot. The project requires Python 3.12
or later.

CI runs the test and Ruff lint/format checks on Python 3.12, 3.13, and 3.14.
It also executes the historical-progression notebook on Python 3.14. The
source-only tutorial does not run a package build.

The `canonical` marker selects tests for the maintained lesson; `historical`
selects tests for the preserved comparison artifacts. `tests/test_integration.py`
exercises both boundaries and remains unmarked. When assessing maintained-code
coverage, scope it to the canonical module rather than combining it with
history:

```bash
./.venv/bin/python -m pytest tests/ --cov=demos.summing_methods
```

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
