# Lint Remediation Plan — resolve 42 Ruff findings and make the config version-proof

*Prepared 2026-08-05. All counts in this document were verified on that date against Ruff 0.16.1 and the repository state at commit `5537658`.*

## Context

`requirements-dev.txt` pins `ruff>=0.15.22,<1` — an open-ended upper bound, so CI resolves whatever Ruff is newest at run time. Ruff 0.16 expanded its default rule set from **61 to 415 rules** for git-backed projects, so `ruff check .` now reports **42 errors** against code that has not changed.

This is why all four open Dependabot pull requests (#58 `setup-python`, #59 `ipykernel`, #60 `nbconvert`, #61 `ruff`) fail CI with *identical* errors — none of them is at fault. The last green run on `main` was 2026-07-23; `main` would fail today if re-run. Every failing CI job ends with `Found 42 errors.` after `pytest` has already passed.

Commit `5537658` added a stopgap `[tool.ruff.lint] select = ["E4","E7","E9","F"]` to `pyproject.toml`. That restores a green CI by *disabling* the new rules. This plan replaces that stopgap with the real fix.

**The stopgap stays in place until this plan is executed** — it is what currently keeps CI green.

### Decisions already taken

1. Remove the `select` pin entirely, enabling all Ruff default rules.
2. Tighten `requirements-dev.txt` to `ruff>=0.16.0,<0.17`, so a future rule-set expansion arrives as a reviewable Dependabot PR rather than a surprise CI failure.
3. Fix all 42 findings, **including those in `history/` and the notebook**. This explicitly overrides `AGENTS.md:28` ("Preserve historical variants unless the request explicitly authorizes … rewriting them") and `ROADMAP.md:47` ("Reformatting history: do not do it as cleanup …").
4. For `BLE001`, move the asserts out of the `try` block rather than suppressing the rule.
5. The supported Python floor stays at `>=3.10`. Python 3.10 reaches end-of-life in October 2026, but raising the floor is a separate support-policy change requiring its own CI-matrix update, and is deliberately out of scope here.

Removing the `select` pin produces exactly these 42 findings, so the target state is self-consistent.

## Precondition: confirm your Ruff version first

The rule set that produces these 42 findings only exists in Ruff 0.16 and later. If you run this plan with an older Ruff, deleting `select` from `pyproject.toml` will make `ruff check .` fall back to that older binary's narrower defaults and print `All checks passed!` while CI still fails on all 42.

Stand up the environment `AGENTS.md:41` prescribes, and verify the version before trusting any lint output:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements-dev.txt
./.venv/bin/python -m ruff --version    # must report 0.16.x
```

Note that `.gitignore` currently covers `venv/` and `env/` but **not** `.venv/`. Either add it as part of this work or take care not to commit the environment.

## The 42 findings

| Rule | Count | Autofixable | Location |
|---|---|---|---|
| I001 unsorted-imports | 14 | yes | tests ×9, history ×3, notebook ×2 |
| UP045 non-pep604-annotation-optional | 11 | yes | demos ×2, history ×9 |
| SIM117 multiple-with-statements | 8 | **no** | test_input_validation ×7, test_integration ×1 |
| UP006 non-pep585-annotation | 3 | yes | demos ×3 |
| UP007 non-pep604-annotation-union | 3 | **no** | demos:12, claude_v2:7, claude_v3:7 |
| UP035 deprecated-import | 2 | display only | demos:10 |
| BLE001 blind-except | 1 | **no** | test_integration:44 |

Distribution by area: `demos/` 8, `tests/` 18, `history/` and the notebook 16.

## Commit sequence

Remove `select` in the working tree early so the counts you see are honest, but **commit the switch-flip last**, so every committed tree is green under its own committed configuration and each step remains independently bisectable.

| # | Commit | Gate |
|---|---|---|
| 1 | Pin Ruff to `>=0.16.0,<0.17` in `requirements-dev.txt` | green; no code risk |
| 2 | Add `[tool.ruff.lint.isort] combine-as-imports = true` | 42 → 41, with zero code edits |
| 3 | Autofix sweep, iterated to a fixpoint | 41 → 14; 153 tests pass |
| 4 | UP007 ×3 by hand, then re-run autofix | 14 → 11; 153 tests pass |
| 5 | SIM117 ×7 in `tests/test_input_validation.py` | 11 → 4; 24 tests collected |
| 6 | SIM117 ×1 and BLE001 in `tests/test_integration.py` | 4 → 0; 25 tests collected |
| 7 | Delete `[tool.ruff.lint] select` from `pyproject.toml` | `ruff check .` clean under 0.16 |
| 8 | Documentation: `AGENTS.md:28`, `ROADMAP.md:47`, `ANALYSIS.md:43` | — |

### Step 2 — the one configuration addition that earns its keep

Add `[tool.ruff.lint.isort] combine-as-imports = true`.

Without it, `tests/test_claude_input.py:8–19` — already written in combined-alias style — is flagged I001, and the autofix **explodes it into six separate `from history.claude_vN import (...)` statements**. With the setting, that file is already clean: the count drops 42 → 41 with no code edit at all. It also matches the import style the repository already uses.

Do **not** add `known-first-party` or `force-sort-within-sections`. Ruff's `src` detection already resolves `demos`, `history`, and `tests` as first-party from the project root; the defaults are correct here, and extra configuration would be noise a future maintainer has to justify.

### Step 3 — the autofix does not converge in a single pass

UP045 and UP006 rewrite `Optional[List[Number]]` into `list[Number] | None`, which strands `List` and `Optional` in the `typing` import as fresh **F401** violations. `Union` survives until UP007 is fixed by hand; only then does the whole `typing` import line disappear — which is also what makes the two display-only UP035 findings evaporate, since those are never fixed directly.

Re-run until the count stops moving. It is not monotonic within a single invocation:

```bash
./.venv/bin/python -m ruff check . --fix    # repeat to a fixpoint
```

No `--unsafe-fixes` is required for any of the 28 autofixable findings.

### Step 4 — UP007, the only runtime-evaluated change

Change `Number = Union[int, float]` to `Number = int | float` in three places: `demos/summing_methods.py:12`, `history/claude_v2_multiple_numbers.py:7`, and `history/claude_v3_menu_demo.py:7`. Then re-run the autofix to drop the now-unused `typing` imports.

The target import block for `demos/summing_methods.py` contains no `typing` import at all:

```python
from __future__ import annotations

import argparse
import math
import operator
import sys
from collections.abc import Iterable, Sequence
from functools import reduce

Number = int | float
```

### Steps 5 and 6 — the hand edits

**SIM117, eight occurrences.** Use the parenthesized form, which is valid at `target-version = "py310"`, and dedent the body by four spaces:

```python
with (
    patch('builtins.input', side_effect=['3.14', '3']),
    patch('builtins.print') as mock_print,
):
```

Seven of these are in `tests/test_input_validation.py` (lines 76, 86, 95, 104, 112, 121, 128), all of the identical shape — an outer `patch('builtins.input', ...)` wrapping an inner `patch('builtins.print') as mock_print`. The two patches target different attributes with no interdependency, so merging them is exactly equivalent.

The eighth, at `tests/test_integration.py:130`, needs more care: its inner `with` carries an inline `# Suppress error messages` comment, which blocks the autofix. Keep that comment attached to the `patch('builtins.print')` line inside the parentheses. `E501` is not in the enforced rule set, but `AGENTS.md:32` mandates PEP 8, so wrap rather than running the line long.

**BLE001, one occurrence** — `tests/test_integration.py:28–45`. The `try` currently wraps both the `importlib` calls *and* four asserts (lines 32, 40, 42, 43), so an `AssertionError` is swallowed and re-reported as `"Failed to import the original example: {e}"`, hiding the real failure. A missing `main` attribute is reported as an import failure.

Narrow the `try` to the `importlib` calls only, use `except ImportError as e: pytest.fail(...)`, and let all four asserts run outside it. This mirrors the sibling test at lines 17–26, which already uses the narrow form. `history/original_two_number.py` has a proper `if __name__ == "__main__":` guard, so `exec_module` is side-effect-free and does not call `input()`.

## Accepted deviations

- **Pedagogical import ordering is alphabetized in two files, not one.** Both `history/chatgpt_v2_test_snapshot.py:13–20` and `tests/test_summation_methods.py:7–14` order their members `add_plus, add_sum, add_operator, sum_builtin, sum_reduce, sum_fsum` to mirror the `# Two-number methods` and `# N-number methods` section headers in those same files. The autofix alphabetizes both. This is accepted; the section-header comments still document the grouping. Decide before running `--fix` — afterwards the original ordering is only recoverable from git, and `# noqa: I001` on the import line is the only mechanism to preserve it.
- `history/chatgpt_v1_entrypoint.py:8` — the I001 fix here is purely deleting one of two blank lines before the `__main__` guard. Cosmetic, but a genuine edit to a preserved file, in scope under decision 3.
- The notebook diff touches cell *source* only. Every code cell already has `"outputs": []` and `"execution_count": null`, so no stored output is invalidated.

## Risks

**PEP 604 at runtime.** `from __future__ import annotations` defers *annotations*, but not module-level assignments, so `Number = int | float` is evaluated at import time and produces a `types.UnionType`. This was verified working on Python 3.10.20, the CI floor. There is no `isinstance(x, Number)` anywhere, no `typing.get_type_hints`, no `__annotations__` introspection, and nothing imports `Number` from another module.

**The two history files carry more runtime exposure than `demos/`.** Neither `history/claude_v2_multiple_numbers.py` nor `history/claude_v3_menu_demo.py` has `from __future__ import annotations`, so their *signature* annotations are evaluated at `def` time — `-> Number | None` evaluates `(int | float) | None` at import. Valid on 3.10, but confirm by actually importing both modules rather than by reading them.

**Load-bearing imports must not move.** `import demos.summing_methods` at `tests/test_integration.py:18` and `:218` sits inside `try:` blocks whose entire purpose is catching `ImportError`. Hoisting either to module scope would convert a single-test failure into a collection failure for the whole file. Ruff's isort does not hoist function-body imports to module scope — the I001 diff produces seven hunks, none at those lines — but assert it afterwards regardless.

**The SIM117 dedent is the likeliest way to silently break a test.** A mis-dedent that moves an assert outside the `patch` context makes the test call the real `input()`, which fails loudly under pytest. But a mis-dedent that *drops* an assert passes for the wrong reason. Guard with per-file collected-test counts.

**Scope boundary.** This work does **not** close DX-001. That roadmap item is a `ruff format` policy — `ruff format --check .` still wants to reformat 12 files — and is orthogonal to lint rule selection.

## Verification

```bash
./.venv/bin/python -m ruff check .                      # All checks passed!
./.venv/bin/python -m pytest tests/                     # 153 passed
./.venv/bin/python -m pytest tests/test_input_validation.py --collect-only -q | tail -1   # 24
./.venv/bin/python -m pytest tests/test_integration.py --collect-only -q | tail -1        # 25
```

Confirm the load-bearing imports were not relocated:

```bash
git diff -U0 tests/test_integration.py | grep 'import demos.summing_methods'   # expect no output
```

Confirm notebook integrity:

```bash
./.venv/bin/python -c "import json; nb=json.load(open('notebooks/historical_progression.ipynb')); \
print(nb['nbformat'], len(nb['cells']), all('id' in c for c in nb['cells']))"
```

Confirm the Python 3.10 floor, which is where the PEP 604 change could bite:

```bash
python3.10 -m venv /tmp/py310
/tmp/py310/bin/pip install -r requirements-dev.txt
/tmp/py310/bin/python -m pytest tests/
/tmp/py310/bin/python -m compileall -q demos history tests   # catches parenthesized-with syntax
/tmp/py310/bin/python -c "import demos.summing_methods as m; print(m.Number)"
/tmp/py310/bin/python -c "import history.claude_v2_multiple_numbers, history.claude_v3_menu_demo; print('ok')"
/tmp/py310/bin/python -m demos.summing_methods --numbers 1 2 3
```

Nothing in this change is specific to a version beyond 3.10, so 3.14 coverage can be deferred to CI.

### Dependabot branches

All four Dependabot branches are based on `origin/main` (`27c2efd`), not on this fix, so the fix must land on `main` before they can pass. Merge-preview them first:

```bash
for b in dependabot/github_actions/actions/setup-python-7 \
         dependabot/pip/ipykernel-gte-7.3.0-and-lt-8 \
         dependabot/pip/nbconvert-gte-7.17.1-and-lt-8; do
  git merge --no-commit --no-ff origin/$b && ./.venv/bin/python -m ruff check . ; git merge --abort
done
```

Those three touch only `.github/workflows/ci.yml` and `requirements-notebook.txt` — zero overlap with anything this plan changes — so they go green purely by inheriting the fix.

## Follow-ups this work must include

1. **PR #61 works against decision 2.** It proposes `ruff>=0.16.0,<1`, re-opening the exact unbounded upper bound that caused this outage. Close it with an explanatory comment rather than merging it. Dependabot will not reopen it, because `>=0.16.0,<0.17` already satisfies its floor.
2. **Amend `AGENTS.md:28` and `ROADMAP.md:47`** to record the maintainer authorization for editing `history/` and the notebook. Without that, a future contributor or agent reads those lines and reverts this work as a policy violation.
3. **Refresh `ANALYSIS.md:43`**, which cites a passing lint result under a rule set that no longer exists. `AGENTS.md` forbids carrying stale verification claims.

Once this lands on `main`, comment `@dependabot rebase` on #58, #59, and #60, and their CI will go green.
