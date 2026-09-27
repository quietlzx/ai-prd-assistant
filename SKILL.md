---
name: ai-prd-assistant
description: Convert raw product requirements into a structured Brief, Gate decision, PRD, AI risk list, human-reviewed report, and single-file HTML through a deterministic serial workflow. Use when the user asks to normalize requirements, generate or review a PRD, assess AI product risks, or validate the structure of an AI product deliverable.
license: MIT
metadata:
  short-description: Staged PRD and AI risk workflow
  version: "0.2.0"
  framework-version: "v1.0-framework"
---

# AI PRD Assistant

Turn an unprocessed product request into a reviewable PRD package. Keep the
workflow serial so later stages do not inherit attention drift from the full
conversation.

## Fixed Workflow

Run these stages in order:

1. Input normalization: produce only a structured Brief.
2. Requirement validation: produce ambiguities and one Gate conclusion.
3. PRD generation: consume the validated Brief and follow the PRD template.
4. AI risk identification: analyze the Brief and PRD against the six risk
   categories.
5. Human review gate: wait for `review_state=approved` before report assembly.
6. Report assembly: produce Markdown and a self-contained HTML file.

Stages 1 through 4 are production stages. Human review is a control gate
between AI risk identification and report assembly.

## State Model

Pipeline status is exactly one of:

- `RUNNING`
- `READY`
- `DRAFT_WITH_GAPS`
- `BLOCKED`
- `HARNESS_FAILED`

Human review state is stored separately in `review_state`:

- `pending`
- `approved`
- `rejected`
- `revision`

Never add a review state to the pipeline status enum.

## Gate Rules

- Critical gaps or hard conflicts produce `BLOCKED`.
- `BLOCKED` outputs clarification questions only and stops.
- Non-critical gaps produce `DRAFT_WITH_GAPS`.
- `DRAFT_WITH_GAPS` may continue with unresolved items marked
  `[待确认:Gxx]`.
- Sufficient information produces `READY`.
- `HARNESS_FAILED` records the failure and stops immediately. Do not retry or
  continue to another stage.
- Human review never converts `BLOCKED` or `HARNESS_FAILED` into a pass.
- Human review never upgrades the Gate to `READY`.

## Stage Contracts

Write each stage to a structured artifact. Downstream stages read those files,
not the complete conversation.

```text
run.json
01_brief.json
02_validation.json
03_prd.md
04_ai_risks.md
04_review_packet.json
04_human_review.json
05_report.md
05_report.html
```

Use these source markers consistently:

- `[来源]`: directly supported by user input.
- `[推断]`: a necessary design inference.
- `[假设]`: a temporary assumption used to continue.
- `[待确认:Gxx]`: unresolved item referenced from the centralized appendix.

Do not invent company facts, policy values, metrics, roles, permissions, or
model capabilities. Put unresolved information in the appendix rather than
silently filling gaps.

## PRD Requirements

Every capability must define:

- user goal
- input
- processing rules
- output
- failure states
- boundary conditions
- acceptance criteria

Collect all unresolved items into one final section named
`附录 A：待确认事项清单`. Every item must include options, business impact,
development impact, recommendation, decision owner, and Gate impact.

Read [references/prd-template.md](references/prd-template.md) when generating
or revising a PRD.

## Risk Requirements

Analyze all six categories:

1. Facts, hallucination, and incorrect citations.
2. Model capability boundaries.
3. Input ambiguity and data quality.
4. Error propagation and automation runaway.
5. Human confirmation and responsibility boundaries.
6. Evaluation, monitoring, and rollback.

Every risk must include:

`风险编号｜类别｜触发条件｜影响｜当前控制｜降级方案｜验证方法｜状态`

Read [references/risk-taxonomy.md](references/risk-taxonomy.md) when producing
the AI risk list.

## Human Review

After Stage 4 and before Stage 5:

1. Freeze the current artifact revision.
2. Build a review packet.
3. Set `review_state=pending`.
4. Wait for `approved`, `rejected`, or `revision`.
5. On `revision`, return to the affected production stage and rebuild the
   review packet.
6. On `rejected`, retain artifacts and stop.
7. On `approved`, lock the revision and continue to report assembly.

Read [references/workflow.md](references/workflow.md) for the transition
contract.

## Report Assembly

Generate Markdown and one self-contained HTML file from the approved revision.
The HTML file must not depend on external scripts, stylesheets, or network
resources.

Read [references/output-contract.md](references/output-contract.md) before
assembling the final report.

## Harness

Use the deterministic helper:

```bash
python scripts/harness.py validate <run-directory>
python scripts/harness.py self-test
```

The Harness validates structure, stage order, field presence, status values,
review state, and artifact references. It does not judge whether the product
requirements or PRD content are semantically good.
