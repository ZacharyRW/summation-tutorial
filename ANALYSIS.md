# Current Project Assessment

**Reviewed:** 2026-08-06 (America/Denver)

## Current state

Summation Tutorial is a small Python 3.12+ educational repository. The
maintained lesson is `demos/summing_methods.py`; `history/` preserves runnable
AI-assisted iterations for comparison and provenance.

The maintained scope is intentionally local and source-based:

- Python distribution artifacts are unsupported; `pyproject.toml` configures
  pytest and Ruff only.
- The canonical lesson accepts interactive input and one-shot `--numbers`
  input, but deliberately has no file, network, persistence, or hosted-execution
  interface.
- CI tests Python 3.12–3.14, runs Ruff lint and format checks, and executes the
  historical-progression notebook on Python 3.14.
- Ruff formatting applies to maintained code and active tests. Historical
  source and the notebook remain linted but are formatting-exempt to preserve
  their archival presentation.
- `canonical` and `historical` pytest markers distinguish the maintained lesson
  from preserved demonstrations; unmarked integration tests cross that
  boundary.
- GitHub secret scanning and push protection are enabled as preventive
  controls.

## Quality and security posture

The design remains intentionally simple: local numeric parsing, arithmetic,
and terminal output. The canonical lesson rejects non-finite float input and
handles EOF cleanly. No file, network, eval, subprocess, secret, persistence,
or authentication path is part of the maintained product.

For maintained-code confidence, run coverage against
`demos.summing_methods`; an aggregate measure that includes historical
artifacts is not meaningful. Keep deterministic tests as the default teaching
tool: property-based testing is not selected at the current scale.

## Conditional future directions

There is no committed implementation backlog. Revisit an item only after its
required product decision is made:

- Distribution support requires a selected audience and a maintained build and
  release policy.
- File input, hosted lessons, web UI, network integrations, or persistence
  require an audience, maintenance owner, and a new security review.
- Contributor templates, `CONTRIBUTING.md`, and a public reporting route belong
  to an active external-contribution workflow.
- Release automation or dependency merging requires an explicit release owner
  and policy.
- Whole-file reformatting of historical artifacts requires a deliberate choice
  to prefer archival uniformity over literal presentation.
