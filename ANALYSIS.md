# Project Analysis

**Audited:** 2026-07-22 (America/Denver)
**Revision:** local `main` at `0386973b23218d24eacf0647fb864bd758b2903f`; live GitHub `main` at `009058c96efbec950c98b125515c32af4c53153f` during the GitHub review.
**Scope:** tracked working tree, local Git metadata/history, declared validation, and live GitHub API/public-page checks.

## Executive Summary

Summation Tutorial is a small Python 3.12+ educational project. Its maintained lesson is `demos/summing_methods.py`; `history/` deliberately preserves the original and AI-assisted iterations as runnable comparison material. The code is healthy for its stated local-learning purpose: the core CLI handles integer and finite-float inputs, the suite passes, Ruff lint passes, and the notebook dependencies install.

No confirmed security vulnerability or user-facing correctness defect was found. The remaining risks are maintenance confidence rather than runtime safety: CI does not check formatting or notebook execution; the repository intentionally does not support package distribution; and the prior planning documents were stale after commit `009058c`.

Recommended direction: retain the focused tutorial-plus-history identity. Phase 1 has closed the integer-test-contract gap, documented the source-tutorial (non-distribution) scope, and verified notebook execution on a normal host. Treat file input, hosted execution, and broad product expansion as opt-in work requiring a new security review.

## Project Overview

| Topic | Assessment |
| --- | --- |
| Purpose / audience | Teach several Python summation approaches to learners, while preserving the iteration history. |
| Technology | Python 3.12+, `argparse`, stdlib numeric APIs; pytest, pytest-cov, Ruff; optional Jupyter/nbconvert. |
| Architecture | Local stdin/argv -> numeric parsing -> arithmetic helpers -> terminal output. Historical modules are separate runnable artifacts; no shared service, persistence, or external API. |
| Features | Interactive two-/many-number lesson; exact integer and finite-float CLI mode; historical v1–v3 demos; v3 sign/statistics helper; progression notebook. |
| Maturity | A maintained educational repository, not a deployed application or library release pipeline. |
| Build/release | `pyproject.toml` declares setuptools packaging metadata, but CI currently validates tests and lint only; no releases/tags are present locally. |

## Repository Structure

| Path | Role |
| --- | --- |
| `demos/summing_methods.py` | Canonical maintained reusable lesson and CLI. |
| `history/` | Labeled runnable provenance artifacts; `history/README.md` maps former names. |
| `tests/` | Active pytest suite (153 collected tests in this audit). |
| `notebooks/` | Optional historical-progression walkthrough. |
| `.github/workflows/ci.yml` | Test/lint matrix covering every supported Python version, 3.12 through 3.14. |
| `requirements-*.txt`, `pyproject.toml` | Tooling and optional notebook dependency contracts. |

## Validation Results

| Check | Result | Evidence / limitation |
| --- | --- | --- |
| Declared dependency install | Passed | Both requirements files were already satisfied in the repository-local Python 3.14.6 environment. Pip disabled its cache because the host cache was not writable; this did not affect resolution. |
| Tests | Passed | `./.venv/bin/python -m pytest tests/`: **153 passed**. |
| Lint | Passed | `./.venv/bin/python -m ruff check .`: `All checks passed!` Re-verified 2026-08-05 under Ruff 0.16.1 with the default rule set and no `select` pin. The original result predates Ruff 0.16, which expanded the git-backed default from 61 to 415 rules; the 42 findings that expansion surfaced were fixed on that date. |
| Coverage | Observed | `pytest --cov=demos --cov=history`: 55% across maintained plus intentionally historical files; canonical lesson 88%, historical artifacts vary 0–67%. This is diagnostic, not a project coverage target. |
| Compile check | Passed | `compileall` completed for `demos`, `history`, and `tests`. |
| CLI smoke tests | Passed | Exact integer and finite-float modes returned expected sums; `nan` exited with argparse error status 2. |
| Formatting check | Scoped policy selected | Ruff formatting applies to maintained Python and active tests; historical code and the notebook are excluded to preserve their archival presentation. CI enforcement is tracked by CI-001. |
| Package build | Intentionally unsupported | The project is a source-based tutorial. `pyproject.toml` contains only tool configuration; no build backend or package metadata remains. A supported build path requires a new maintainer decision. |
| Notebook execution | Passed on normal host | On 2026-08-05, the documented `jupyter nbconvert --to notebook --execute` command exited 0 with Python 3.14.6 and nbconvert 7.17.1, writing a disposable artifact to `/tmp/historical_progression.executed.ipynb`. The tool sandbox itself still prohibits binding the local kernel port. |
| Type/static analysis | Not configured | No type checker or type-checking configuration is declared. |

CI installs `requirements-dev.txt`, then runs pytest, Ruff lint, and Ruff format checks across Python 3.12–3.14. A separate Python 3.14 job installs `requirements-notebook.txt` and executes the historical-progression notebook. It intentionally does not build a package or run a type checker.

## Existing Issue Verification

| Existing item | Source | Current status | Verification | Still relevant? | Recommended action |
| --- | --- | --- | --- | --- | --- |
| Python 3.12+ baseline | Prior analysis/roadmap, `pyproject.toml`, CI | Confirmed | Metadata and Ruff target are `py312`; CI matrix declares 3.12/3.13/3.14, matching the declared support range exactly. Raised from 3.10 on 2026-08-05 ahead of the 3.10 end-of-life in October 2026. | Yes | Maintain; extend the matrix and the required-check list together whenever `requires-python` changes. |
| Canonical one-shot CLI | Prior roadmap | Confirmed / completed | `--numbers` is implemented and smoke-tested. | No backlog item | Keep contract stable. |
| Historical v3 statistics | Prior roadmap, GitHub issue #25 | Confirmed / completed | Implemented in `history/claude_v3_menu_demo.py`, covered by direct tests; issue #25 was closed with merged PR #56. | No backlog item | Keep the historical-provenance boundary. |
| Historical notebook | Prior roadmap, GitHub issue #28 | Confirmed / completed | Notebook and dependencies exist; issue #28 was closed with merged PR #56. Execution is blocked only by this sandbox's socket restriction. | No backlog item | Verify on a normal host/CI before claiming a portable execution result. |
| Security-scope closure | Prior analysis | Confirmed | Repository-wide source review found only local numeric parsing and terminal output; no file/network/eval/subprocess/secret path. | Yes, conditionally | Reassess before file, network, persistence, hosted, auth, or plugin work. |
| “No verified local defect” | Prior analysis | Partially confirmed | No runtime bug found; package-build and test-contract gaps remain. | No, wording too broad | Replace with this qualified assessment. |

Searches found no active TODO/FIXME/HACK/XXX markers, skipped or xfailed active tests, placeholder implementations, or tracked secrets. The historical test snapshot is explicitly `__test__ = False` and its non-collection is intentional.

## Newly Discovered Findings

### Medium

**PKG-001 — Declared distribution is not validated in local setup or CI**
Affected: `pyproject.toml`, `requirements-dev.txt`, `.github/workflows/ci.yml`.
Evidence: build frontend `build` and backend `setuptools` are absent from the declared local dev environment; a non-isolated wheel attempt fails importing `setuptools.build_meta`; CI does not build.
Impact: packaging regressions can land unnoticed, and the repository does not yet prove whether it intends to be installable/distributable.
Current decision: source-tutorial scope. README and developer guidance now state that the project does not support, validate, or publish package distributions. Revisit only if a maintainer selects distribution support. **Confidence: high.**

**TEST-001 — Several integer parser tests permit a type-contract regression — Resolved 2026-08-05**
Affected: `tests/test_input_validation.py:12-143`, `demos/summing_methods.py:25-44`.
Evidence: tests expect values such as `[42.0]` while the documented and implemented integer mode returns `int`; Python equality makes `[42] == [42.0]` pass. Only the large-integer case asserts types.
Impact: a future conversion to floats could silently violate exact-integer teaching and precision behavior for ordinary inputs.
Resolution: integer-mode tests now assert exact values and `int` types across ordinary, retry, whitespace, leading-zero, and exact-large-integer cases. **Confidence: high.**

### Low

**DX-001 — Formatting policy is unresolved and unenforced**
Affected: 12 Python/notebook files, CI.
Evidence: lint passes, but `ruff format --check .` reports 12 files would change.
Impact: contributors cannot infer whether formatting drift is accepted, especially in preserved history.
Fix: decide whether historical artifacts are formatting-exempt; then either format approved paths or configure/exclude them and add the chosen check to CI. **Confidence: high.**

**DOC-001 — Planning files were stale at audit start**
Affected: `ANALYSIS.md`, `ROADMAP.md`.
Evidence: they were reconciled at `15b7df5`/July 19 but `009058c` added the notebook and statistics on July 21.
Impact: readers could mistake post-audit feature work for pending work.
Fix: this audit replaces both documents and records current limitations. **Confidence: high.**

### Informational

The historical original program does not handle invalid input or EOF as gracefully as the maintained lesson. That is intentional provenance, not a defect in the canonical product. No confirmed performance bottleneck exists; `math.fsum` appropriately demonstrates the precision tradeoff. No reportable security/privacy issue was found.

## Architecture, Quality, Security, and Performance

The architecture is appropriately simple: one canonical implementation, explicit historical separation, and no external services. The strongest design choice is avoiding duplicated maintained logic; the ChatGPT historical entrypoint delegates to the canonical lesson. Pytest `canonical` and `historical` markers now identify the maintained and archival suites, while unmarked integration tests explicitly cross that boundary. Coverage reporting for maintained confidence should target `demos.summing_methods` rather than aggregate historical code.

Security posture is low-risk by design. All reviewed input reaches conversion, arithmetic, sorting, or output only; finite-float checks and EOF handling exist in maintained paths. Local resource exhaustion from enormous literals/iterables is not a cross-boundary security finding. File input should remain out of scope without explicit size/format/security design.

Performance is not a concern at this scale. The only potentially unbounded maintained behavior is accepting arbitrarily many CLI tokens / arbitrarily large local numeric literals; a limit would be a UX/resource policy decision, not a demonstrated bottleneck.

## Documentation Assessment

| Document | Status | Problems | Recommended action |
| --- | --- | --- | --- |
| `README.md` | Accurate with limitation | Notebook execution claim cannot be verified in this sandbox; no contributor/release guidance. | Keep; add only verified build/notebook guidance after CI decision. |
| `history/README.md` | Accurate | Concise by design. | Keep. |
| `AGENTS.md` / `CLAUDE.md` | Accurate | Operational, not public contributor documentation. | Keep. |
| `ANALYSIS.md` | Replaced | Prior revision stale. | Keep current audit as canonical assessment. |
| `ROADMAP.md` | Replaced | Prior revision mixed completed and current work without phases. | Keep current execution tracker. |
| `LICENSE` | Accurate | GPL-3.0-only is clear. | Keep. |
| Missing public docs | Incomplete | No CONTRIBUTING, SECURITY, release/process guide, or changelog. | Create only if external contributions/releases become active; a short `SECURITY.md` is worthwhile before expanding attack surface. |

## GitHub and Branch Assessment

Live GitHub review on 2026-07-22 confirmed that [`ZacharyRW/summation-tutorial`](https://github.com/ZacharyRW/summation-tutorial) is a public, active, non-archived Python repository. Its concise description and five topics (`python`, `education`, `tutorial`, `summation`, and `ai-assisted-development`) accurately describe the project, and the rendered README clearly distinguishes the maintained lesson from historical artifacts. There is no homepage URL, social-preview asset was not verifiable through the public page/API, and the repository has no releases, packages, Wiki, Discussions, or Projects. Those omissions fit the current local-tutorial scope; create a homepage, release process, or showcase media only after selecting a distribution goal.

GitHub's community profile reports 42% health because `CONTRIBUTING.md`, a code of conduct, issue forms/templates, and a pull-request template are absent. This is not a current operational defect: Issues are enabled but there are **zero open Issues**, **zero open PRs**, and no milestones. The completed notebook and historical-statistics work is reconciled: issues #25 and #28 closed when PR #56 merged. Recent external contribution PRs are closed rather than left abandoned.

The Actions view shows active CI, Dependabot Updates, and Dependency Graph workflows. The latest `main` CI run for `009058c` completed successfully on 2026-07-22. Dependabot security updates are enabled, and the checked-in configuration covers pip and GitHub Actions. `main` is protected with strict required checks for Python 3.12, 3.13, and 3.14, matching the CI matrix after the support floor was raised on 2026-08-05; the protection applies to administrators and forbids force-pushes and branch deletion. (The 2026-07-22 audit recorded required checks for 3.10, 3.11, and 3.14. A live API read on 2026-08-05, before the floor change, returned all five matrix versions as required contexts, so that earlier three-version claim was incomplete rather than a record of subsequent drift.) No rulesets are configured, which is acceptable because the classic branch-protection rule supplies the required safeguards. On 2026-08-05, GitHub secret scanning and push protection were enabled and verified through the GitHub API. No secret was found in the source audit; the controls are preventive.

Live branch inspection found one remote branch, `main`, at `009058c`; it is the protected default branch, and there are zero tags. The local checkout is at `0386973`, one committed documentation update ahead of `origin/main`; that local state must be reviewed and explicitly pushed before GitHub can reflect it. Historical `master` exists only in old commit ancestry and merged-PR history, not as a current branch.

| Branch | Last activity | Merge status | Associated PR | Unique commits | Recommended action | Reason |
| --- | --- | --- | --- | --- | --- | --- |
| `main` / `origin/main` | 2026-07-22 | Protected default/current | None open | Local `main` is 1 commit ahead of `origin/main` | Keep; push only after review | The sole active branch is healthy; the local documentation commit has not yet reached GitHub. |

## Product Opportunities and Recommended Priorities

The precision lesson now compares `sum`, `reduce`, and `math.fsum` with a small deterministic example. Property-based tests are deliberately not selected: clear deterministic cases better fit the tutorial's current scale. Larger directions (file input, web lesson, hosted notebook, integrations) require clear audience demand and a new security/privacy design. Do not pursue file input merely for feature breadth, automatic releases, or a generic web frontend without a defined educational need.

## Limitations

This audit authenticated to GitHub and inspected live metadata, public presentation, Issues, PRs, workflows, releases/tags, branch protection, and repository settings. It did not verify an uploaded social-preview image because GitHub does not expose that asset through the reviewed public/API surfaces. It also did not install a missing build frontend/backend, run a build in isolated networked mode, run a type checker (none is configured), or execute the notebook because the sandbox prohibits local kernel socket binding. No destructive cleanup, branch deletion, or GitHub-setting change was performed.
