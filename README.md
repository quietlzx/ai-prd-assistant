# AI PRD Assistant

AI PRD Assistant is a Codex Skill for turning raw product requirements into a
structured, reviewable PRD package.

It uses a serial workflow, explicit Gate decisions, staged artifacts, a
human-review control gate, and a deterministic structure-only Harness.

## Workflow

```text
Input normalization
→ Requirement validation
→ PRD generation
→ AI risk identification
→ Human review
→ Report assembly
```

The first four stages produce the working artifacts. Human review is a control
gate between AI risk identification and final report assembly.

## What It Produces

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

The final HTML report is self-contained and requires no external scripts,
styles, fonts, or network resources.

## Status Model

Pipeline status:

```text
RUNNING
READY
DRAFT_WITH_GAPS
BLOCKED
HARNESS_FAILED
```

Human review state:

```text
pending
approved
rejected
revision
```

`review_state` never changes the pipeline status enum.

## Gate Rules

- Critical gaps or hard conflicts produce `BLOCKED`.
- `BLOCKED` outputs clarification questions and stops.
- Non-critical gaps produce `DRAFT_WITH_GAPS`.
- `DRAFT_WITH_GAPS` marks unresolved decisions as `[待确认:Gxx]`.
- `HARNESS_FAILED` records the failure and stops immediately.
- Human review never bypasses `BLOCKED` or `HARNESS_FAILED`.
- Human review never upgrades the Gate to `READY`.

## Installation

Clone this repository into your Codex skills directory:

```powershell
git clone https://github.com/quietlzx/ai-prd-assistant.git
Copy-Item -Recurse -Force `
  ".\ai-prd-assistant" `
  "$env:USERPROFILE\.codex\skills\ai-prd-assistant"
```

Invoke it in Codex with:

```text
Use $ai-prd-assistant to turn this raw requirement into a staged PRD package.
```

## Usage

Provide the raw requirement and ask for a Brief, validation result, PRD, risk
list, and review-ready report package.

The Skill will:

1. Normalize the input into a structured Brief.
2. Decide whether the request is `READY`, `DRAFT_WITH_GAPS`, or `BLOCKED`.
3. Generate the PRD only after requirement validation.
4. Analyze all six AI product risk categories.
5. Stop at human review.
6. Assemble Markdown and HTML only after `review_state=approved`.

## Harness

Run the built-in validation:

```bash
python scripts/harness.py self-test
python scripts/harness.py validate <run-directory>
```

The Harness checks:

- stage order
- required files
- required fields
- status values
- review state transitions
- artifact references
- unnumbered `[待确认]` markers
- self-contained HTML constraints
- required disclaimer text

The Harness does not judge business semantics or PRD quality.

## Repository Layout

```text
ai-prd-assistant/
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- llm-default.yaml
|-- references/
|   |-- output-contract.md
|   |-- prd-template.md
|   |-- risk-taxonomy.md
|   `-- workflow.md
|-- scripts/
|   `-- harness.py
`-- test-cases/
    |-- conflict/
    |-- empty-input/
    |-- missing-info/
    `-- normal/
```

## Configuration

`llm-default.yaml` contains a provider-neutral default model configuration.
Use environment variables for credentials and deployment-specific endpoints.
Do not commit API keys, private model URLs, or internal documents.

## Development

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
pytest
ruff check .
python scripts/harness.py self-test
```

## Contributing

Read `CONTRIBUTING.md`. Changes to status values, Gate behavior, review-state
transitions, or output structure are breaking changes and require tests and a
CHANGELOG entry.

## Security

Read `SECURITY.md`. Do not submit real company documents, customer data,
credentials, private endpoints, or unredacted run artifacts.

## License

MIT
