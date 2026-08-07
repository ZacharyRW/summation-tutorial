# Project Roadmap

**Derived from:** the verified 2026-08-06 assessment in `ANALYSIS.md`
**Current commitment:** Verify the selected SEC-002, SEC-003, and GH-002 changes in GitHub CI. Outside contributions are not accepted; other entries are conditional, not an implementation backlog.

## Roadmap Principles

Prioritize confirmed user/project impact, risk reduction, dependency order, effort, maintainability, and fit with the local source-tutorial identity. Prefer small reversible changes. A roadmap item needs current evidence, an owner/decision where applicable, and measurable completion criteria; closed issues and speculative TODOs do not return here without verification.

## Phase 0: Immediate Safety and Repository Hygiene

No critical bug, secret exposure, broken build, default-branch migration, or safely deletable branch was found.

- **SEC-002 / SEC-003 — Pin executable GitHub Actions.** Implemented locally: `actions/checkout@v7` and `actions/setup-python@v7` now use published full commit SHAs with readable version comments. Keep Dependabot updates, then verify CI after push.

## Phase 1: Stabilization

- **GH-002 — Require notebook verification.** Implemented: `Historical progression notebook` is now in `main` branch protection's required-check set. Verify it remains green after CI runs.
- **TEST-001 — Retain focused interactive regression coverage.** No repair is due now. Add tests for interactive success/error presentation branches only when `main()`, prompts, or CLI error behavior changes.

## Phase 2: Maintainability and Developer Experience

- **DX-001 — Make a type-checking decision.** Evaluate a lightweight checker for canonical code and tests; adopt it only if its teaching/maintenance value justifies extra setup and CI.
- **GH-003 / DOC-001 — Maintain the selected contribution posture.** Outside contributions are not accepted. Keep the README boundary and do not add contributor, conduct, issue-form, or PR-template boilerplate. Treat a security reporting policy as a separate future decision.
- **DX-002 — Keep toolchain alignment.** For every dependency/toolchain change, keep Python support, requirements, README commands, Ruff scope, CI, and branch protection aligned.

## Phase 3: Product Improvements

No product work is selected. If learner demand warrants it, select only one narrowly scoped addition:

- **FEAT-001:** A compact compensated-summation or `Decimal` comparison that remains clear beside `sum`, `reduce`, and `math.fsum`.
- **FEAT-002:** A small exercise/answer path using existing canonical functions rather than a competing implementation.

## Phase 4: Strategic Expansion

- **ARCH-001 — Distribution support:** requires a selected audience, package structure, build/release owner, support policy, and validated install path.
- **ARCH-002 — Hosted/web expansion:** requires product discovery, accessibility and operating design, bounded inputs, ownership, and a new security review.

## Exploratory Ideas

- Property-based tests when they demonstrably improve the lesson over deterministic examples.
- A custom social preview or short visual demo if public discovery becomes a goal.
- A reusable template for preserving AI-assisted tutorial progression.

## Deferred or Rejected Ideas

| Idea | Status | Reason |
| --- | --- | --- |
| File input | Deferred | Needs format, encoding, size/count limits, error contract, and security review. |
| Network, persistence, authentication, web API | Rejected for current scope | Changes the tutorial's identity and threat model. |
| Package builds/releases | Deferred | No distribution audience or release owner. |
| Historical whole-file formatting | Deferred | Archival presentation is an explicit policy. |
| Git pruning/cleanup | Rejected for audit | Backup and dangling objects are recovery evidence; no stale branch is safe to delete. |

## Documentation Plan

1. Keep README, AGENTS, history guidance, analysis, and roadmap aligned with selected behavior.
2. After GH-002, document whether notebook CI is required or advisory.
3. Keep contributor/conduct/template documents absent while the maintainer-led, no-outside-contributions posture remains selected; create a security policy only after selecting a reporting route.
4. Do not create changelog, release, deployment, package, or API documentation before the capability exists.

## GitHub Improvement Plan

1. SHA-pin third-party actions and retain Dependabot updates (SEC-002/003).
2. Align protected-branch checks with the notebook decision (GH-002).
3. Keep public contribution guidance and templates out of scope unless the contribution posture changes; evaluate a security policy separately if a reporting route is selected.
4. Preserve `main` protection, secret scanning, push protection, and Dependabot security updates.
5. Leave homepage, wiki, Discussions, packages, releases, and social preview unchanged unless discovery/distribution becomes an explicit objective.

## Branch Cleanup Plan

| Category | Refs | Action |
| --- | --- | --- |
| Safe to delete now | None | No deletion. |
| Review before deletion | Unreachable local objects | Review in a dedicated Git-maintenance session before pruning/GC. |
| Keep | `main`, `origin/main`, `backup/pre-reset-0386973` | Main is current/protected; backup preserves distinct recovery history. |
| Rename or migrate | None | Default branch is already `main`; `master` is only historical. |
| Manual GitHub action | None | Notebook protection was updated and verified through the GitHub API. |

## Milestone Table

| ID | Initiative | Priority | Effort | Dependencies | Target Phase | Success Criteria |
| --- | --- | --- | --- | --- | --- | --- |
| SEC-002 | Pin `actions/checkout` | P2 | XS | Current SHA and CI | 0 | All uses are immutable SHA pins; CI passes. |
| SEC-003 | Pin `actions/setup-python` | P2 | XS | Current SHA and CI | 0 | All uses are immutable SHA pins; CI passes. |
| GH-002 | Require notebook check | P2 | XS | Stable check name | 1 | Notebook check is required by `main` protection. |
| TEST-001 | Interactive coverage on change | P3 | XS | Relevant behavior change | 1 | Changed interactive paths have focused regression tests. |
| DX-001 | Type-checking decision | P3 | S | Clear benefit | 2 | Accept/reject decision recorded; if accepted, CI is green. |
| GH-003 | Maintainer-led contribution boundary | P3 | XS | README update | 2 | README states that outside contributions are not accepted. |
| DX-002 | Toolchain alignment | P3 | XS | Toolchain change | 2 | Docs, CI, requirements, and checks agree. |
| FEAT-001 | Focused numeric extension | P4 | S | Learner need | 3 | Fits canonical lesson with tests/docs. |
| ARCH-001 | Distribution support | P4 | M | Audience, owner, release policy | 4 | Supported install/build/release is validated. |
| ARCH-002 | Hosted/web product | P4 | L | Discovery, owner, security review | 4 | Design has bounded inputs, accessibility, and operations plan. |

## Success Metrics

- All executable GitHub Action references are immutable SHAs, with reviewable upgrade comments and Dependabot coverage.
- Notebook CI is intentionally required or intentionally advisory, never ambiguous.
- Tests, Ruff, formatting, and notebook execution remain green on documented toolchains.
- Maintained-module coverage does not regress without a documented reason.
- Zero open confirmed arithmetic, parsing, or CI-integrity defects.
- If collaboration is selected, community-profile guidance matches the real contribution and security-reporting workflow.

## Recommended Execution Order

1. Make a small SEC-002/003 change that pins the two Actions, then verify GitHub CI.
2. Decide GH-002 and update branch protection plus documentation in one focused change.
3. Retain the selected maintainer-led posture; revisit GH-003/DOC-001 only if that decision changes. Evaluate `SECURITY.md` separately if a reporting route is selected.
4. Reassess optional product/testing ideas only when a learner or maintainer need is explicit.

## Change Rules

- Preserve historical artifacts and uncommitted user work.
- Do not rewrite shared history, force-push, delete unmerged branches, or prune recovery objects during roadmap work.
- Keep Python 3.12+ and source-only scope unless a maintainer explicitly changes them.
- Add focused regression tests for behavior changes and report current scope-appropriate validation.
- Do not present exploratory ideas as committed work.
