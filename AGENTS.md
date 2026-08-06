# Summation Tutorial Repository Agent Guide

## Purpose and scope

Summation Tutorial is an educational Python summation tutorial that preserves AI-assisted implementation iterations as teaching artifacts. `demos/summing_methods.py` is the canonical reusable lesson; historical runnable examples live in `history/`.

## Authoritative sources

- Current code and `LICENSE` are authoritative for behavior and licensing. GPL-3.0 is the maintainer-selected license.
- `ANALYSIS.md` is the current dated assessment; `ROADMAP.md` is the current execution tracker.
- `README.md`, this guide, and generated reports must not make claims that conflict with current code, tests, or `LICENSE`.
- Historical audit, review, and coverage reports were reviewed and removed on 2026-07-17. Do not recreate their stale test counts or coverage estimates as current evidence.

## Repository layout

- `demos/summing_methods.py`: canonical reusable summation functions and interactive lesson.
- `history/`: historical examples and former-name mapping; run examples as modules from the repository root.
- `history/original_two_number.py`: original two-number CLI example.
- `history/claude_v*_*.py`: historical, independently runnable Claude iterations.
- `history/chatgpt_v1_entrypoint.py`: historical ChatGPT entry point that delegates to the canonical lesson.
- `history/chatgpt_v2_test_snapshot.py`: historical pytest snapshot; it is deliberately not collected.
- `tests/`: pytest suite; `test_summation_methods.py` is the single active core arithmetic suite.
- Python 3.12 or later is supported; do not reintroduce Python 3.11 or earlier compatibility without an explicit maintainer decision. The floor was raised from 3.10 to 3.12 by maintainer decision on 2026-08-05, ahead of the Python 3.10 end-of-life in October 2026.

## Working conventions

- Inspect current code, `ANALYSIS.md`, and `ROADMAP.md` before proposing or implementing work.
- Preserve historical variants unless the request explicitly authorizes moving, deleting, or rewriting them. Keep their provenance labels accurate when the canonical lesson changes.
- Exception, authorized 2026-08-05: `history/` and `notebooks/historical_progression.ipynb` were edited to clear Ruff lint findings when Ruff 0.16 expanded its default rule set. Import sorting and PEP 585/604 annotation modernization applied there deliberately, and are not a policy violation to revert. This authorization covers lint compliance only; whole-file reformatting remains out of scope pending `DX-001`.
- Add focused regression tests for behavior changes. Do not claim coverage for a source function when a test exercises a local copy instead.
- The canonical lesson supports a one-shot CLI through `python -m demos.summing_methods --numbers ...`; preserve no-argument interactive behavior and keep file input out of scope unless explicitly authorized with a new security review.
- The repository is currently a source-based tutorial, not a supported distributable package. `pyproject.toml` carries project/tool metadata; do not add, document, or rely on package-build or installation workflows unless a maintainer explicitly selects distribution support.
- Keep documentation repository-relative and avoid volatile assertions about test counts, line counts, coverage percentages, or branch state unless freshly verified.
- Use clear docstrings, type hints where they improve the lesson, PEP 8 formatting, and user-facing validation/error messages.
- Do not shadow built-ins such as `sum`.

## Current caution points

- Historical test and coverage claims are non-authoritative. Use the declared Python 3.12+ toolchain and current CI results when reporting verification evidence.

## Verification and Git

- Create a repository-local environment with `python3 -m venv .venv`, install the declared development tools with `./.venv/bin/python -m pip install -r requirements-dev.txt`, then run `./.venv/bin/python -m pytest tests/` and `./.venv/bin/python -m ruff check .`. The CI workflow runs the same checks.
- Before making Git claims, check `git branch --show-current`, `git rev-parse --short HEAD`, and `git status --short`.
- Push only when explicitly requested. Confirm the branch and staged scope immediately before committing or pushing.
