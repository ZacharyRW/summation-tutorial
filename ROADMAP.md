# Project Roadmap

**Derived from:** `ANALYSIS.md` audited 2026-07-22; live GitHub `main` was `009058c` and local `main` was `0386973` (one commit ahead of `origin/main`).
**Principle:** prioritize verified user-contract failures and release-confidence gaps before optional features; preserve historical artifacts unless a change explicitly selects them.

## Roadmap Principles

Order work by learner impact, risk reduction, evidence strength, effort, dependency order, and fit with the small local-tutorial identity. Completed historical work is not backlog. Speculative product directions remain exploratory until a maintainer selects them.

## Phase 0: Immediate Safety and Repository Hygiene

**Completed 2026-08-05.** No critical security issue, broken test suite, unsafe branch, or default-branch migration is required. Keep protected `main` as default and do not delete branches: it is the only remote branch. Do not push local changes without explicit approval.

## Phase 1: Stabilization

- **TEST-001 — Completed 2026-08-05:** Integer-mode parser tests now assert exact values and `int` types, including the exact-large-integer regression case.
- **DOC-002 — Completed 2026-08-05:** README and developer guidance establish the current source-tutorial scope: package distribution is not a supported workflow.
- **NB-001 — Completed 2026-08-05:** The documented `jupyter nbconvert --execute` command succeeded on the normal host with Python 3.14.6 and Jupyter nbconvert 7.17.1; it wrote the disposable output to `/tmp/historical_progression.executed.ipynb`.
- **GH-005 — Completed 2026-08-05:** GitHub secret scanning and push protection are enabled and were read back through the GitHub API. No secret exposure was found; these are preventive controls.

## Phase 2: Maintainability and Developer Experience

- **PKG-001 — Completed 2026-08-06:** The source-only decision is enforced by removing PEP 517 build and package metadata; `pyproject.toml` now contains only tool configuration.
- **DX-001:** Decide formatting scope for historical Python and the notebook; enforce the chosen Ruff format policy in CI.
- **CI-001:** Add the chosen build/format/notebook checks only after they are deterministic and their support policy is documented.
- **TEST-002:** Separate canonical-contract tests from historical demonstration tests in documentation and, if useful, pytest markers; use coverage for the maintained module rather than an aggregate historical percentage.

## Phase 3: Product Improvements

- **FEAT-001:** Add a brief precision lesson comparing builtin `sum`, `reduce`, and `math.fsum`, with a small reproducible example.
- **FEAT-002:** Add property-based tests only if the educational value exceeds setup complexity; retain clear deterministic examples.

## Phase 4: Strategic Expansion

No expansion is committed. Hosted lessons, file input, network integrations, publishing automation, or web UI require a selected audience, maintenance owner, and a new security review.

## Exploratory Ideas

- A concise contributor guide if outside contributions become active.
- A `SECURITY.md` that states the local-only threat model and security reporting route before the attack surface grows.
- An intentional release/checklist process if versioned distributions are actually published.

## Deferred or Rejected Ideas

- File input: defer until format, encoding, size/count bounds, finite-number policy, error behavior, and a security review are approved.
- Automatic releases/dependency merging: do not add without an explicit release ownership policy.
- Reformatting history: do not do it as cleanup unless maintainers choose archival uniformity over literal historical presentation. Narrow exception authorized 2026-08-05: `history/` and the notebook were edited to satisfy Ruff's default rule set after the 0.16 expansion. That covers lint compliance only and does not pre-decide `DX-001`, which remains a separate `ruff format` policy decision.

## Documentation Plan

1. Keep the completed integer type contract and source-tutorial package scope accurate as the lesson evolves.
2. Decide `DX-001`; document historical-code formatting scope.
3. Add `CONTRIBUTING.md`, `SECURITY.md`, changelog, or release guide only when their corresponding workflow exists.

## GitHub Improvement Plan

The live GitHub review is complete: the public description, topics, README presentation, default branch, protections, Actions, Dependabot configuration, Issues, PRs, releases/tags, and repository features were verified. Keep the current description/topics and branch-protection rule; latest `main` CI is green and no Issues or PRs are open. Do not create releases, packages, a homepage, or showcase media unless a distribution goal is selected.

`GH-005` is complete: secret scanning and push protection were enabled and verified on 2026-08-05. These are preventive controls, not evidence of a current secret leak. If external contributions become an active goal, create focused issue forms/templates, a PR template, and a concise `CONTRIBUTING.md`; otherwise the 42% community-profile score is informational rather than a backlog defect. After `PKG-001`/`DX-001`, add only validated checks to the required-check policy. The social-preview asset remains a manual visual setting to review if public showcasing becomes important.

## Branch Cleanup Plan

| Category | Action |
| --- | --- |
| Safe to delete now | None. |
| Review before deletion | None visible locally. |
| Keep | The only remote branch, protected `main`; local `main` is one reviewed commit ahead of `origin/main`. |
| Rename or migrate | None; default branch is already `main`. |
| Manual GitHub action required | None for branch hygiene. Push the local documentation commit only when it has been reviewed and explicitly approved. |

## Milestones

| ID | Initiative | Priority | Effort | Dependencies | Target phase | Success criteria |
| --- | --- | --- | --- | --- | --- | --- |
| TEST-001 | Assert exact integer type contract | High | S | None | 1 (completed) | Integer parser tests fail if values become floats. |
| NB-001 | Verify notebook on socket-capable host | Medium | S | Normal host/CI | 1 (completed) | Documented nbconvert command exits 0. |
| GH-005 | Enable GitHub secret scanning and push protection | Medium | XS | None | 1 (completed) | Both controls are enabled and verified through the GitHub API. |
| PKG-001 | Narrow package expectations for the source tutorial | High | S-M | None | 2 (completed) | No build backend or package metadata remains; distribution is explicitly unsupported. |
| DX-001 | Establish formatting policy | Medium | S | Maintainer decision | 2 | `ruff format --check` is green for selected scope. |
| CI-001 | Align CI with supported validation | Medium | S | PKG-001/DX-001/NB-001 | 2 | Required checks match documented support. |
| FEAT-001 | Explain numeric precision tradeoffs | Low | S | None | 3 | Lesson includes tested, readable comparison. |

## Success Metrics

- All tests pass and integer type assertions protect the documented contract.
- Every documented setup/build command is reproducibly green on a supported host.
- CI runs every validation the project claims to enforce.
- `main` remains clean and synchronized; no unverified branch deletion.
- Planning documents are updated whenever selected work changes canonical behavior.

## Recommended Execution Order

1. Decide formatting treatment for historical files, then implement DX-001/CI-001.
2. Revisit PKG-001 only if a maintainer selects distribution support.
3. Select at most one Phase 3 improvement.
