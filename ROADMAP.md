# Project Roadmap

**Updated:** 2026-08-06 (America/Denver)

## Current status

No implementation work is currently committed. The maintained tutorial has a
documented source-only scope, deterministic validation, CI coverage for its
supported checks, and a deliberate boundary between canonical and historical
artifacts.

## Conditional backlog

Select an item only when its prerequisites and ownership are explicit.

| Initiative | Classification | Prerequisites | Success criteria |
| --- | --- | --- | --- |
| Distribution support | Optional enhancement | Audience, maintenance owner, build and release policy | A supported wheel/sdist path is documented, validated, and owned. |
| Property-based tests | Optional enhancement | Clear teaching benefit over deterministic examples | New tests improve the lesson without obscuring its numeric contracts. |
| File input | Deferred | Format, encoding, size/count limits, finite-number policy, error contract, and security review | A bounded, tested input design is approved. |
| Hosted/web/network expansion | Speculative direction | Audience, maintenance owner, and security review | A selected product scope has a safe, sustainable design. |
| Contribution guidance | Optional enhancement | Active external-contribution workflow | Contributor, issue, and PR guidance fits the actual workflow. |
| Security reporting guidance | Optional enhancement | Chosen reporting route | `SECURITY.md` reflects the local-only threat model and reporting process. |
| Release automation or dependency merging | Deferred | Explicit release owner and policy | Automation has review, rollback, and ownership controls. |
| Historical whole-file formatting | Deferred | Maintainer decision favoring archival uniformity | Historical presentation is changed deliberately and documented. |

## Maintenance rules

- Keep the Python support matrix, README, CI, and Ruff scope aligned.
- Preserve historical provenance unless a selected item explicitly changes it.
- Keep coverage claims scoped to the maintained lesson.
- Reassess this roadmap only when a conditional item becomes selected work.
