# PRD Template

## Document Header

- Product name
- Product version
- PRD version
- Run ID
- Framework version
- Pipeline status
- Review state
- Timestamp
- Input summary

## Required Sections

### 1. Product Overview

Describe the product, target outcome, and hard boundaries. Do not use
unverified claims.

### 2. Product Goals

State measurable outcomes and explicit non-goals.

### 3. Users and Scenarios

Use concrete users and workflows. Mark inferred personas with `[推断]`.

### 4. Scope

Separate in-scope and out-of-scope behavior.

### 5. Functional Capabilities

For every capability, include all of these fields:

- User goal
- Input
- Processing rules
- Output
- Failure states
- Boundary conditions
- Acceptance criteria

For AI products, explicitly cover grounding, citation, permission filtering,
refusal, human review, failure-closed behavior, and data lifecycle events.

### 6. Non-Functional Requirements

Define performance, security, privacy, availability, observability,
auditability, permissions, rollback, and data retention.

### 7. Quantitative Quality Targets

Use unambiguous denominators, sampling rules, and evaluation sources. Do not
write goals such as "high accuracy" without a number and measurement method.

### 8. Lifecycle Behavior

Describe update, delete, offline, revocation, index invalidation, cache
invalidation, and historical-reference behavior.

### 9. Acceptance Scenarios

Cover success, refusal, blocked, review, permission changes, deletion,
outdated documents, model failures, and rollback.

### 10. AI Risks

Use the fixed risk fields from the risk taxonomy.

### 11. Human Review Gate

Record `pipeline_status`, `review_state`, review inputs, decisions, and the
conditions required for report assembly.

### 12. Report Assembly

Require Markdown and a self-contained HTML artifact built from the approved
revision.

### Appendix A: Pending Decisions

Use one entry per unresolved item:

```text
Gxx
Current default:
Decision owner:
Gate impact:

| Option | Business impact | Development impact |
|---|---|---|
| A | ... | ... |
| B | ... | ... |

Recommendation:
Status: [待确认:Gxx]
```

Do not leave unnumbered `[待确认]` markers in the main document.

## Capability Pattern

Use this compact pattern when a table would be hard to read:

```markdown
#### F1 Capability name

- User goal:
- Input:
- Processing rules:
- Output:
- Failure states:
- Boundary conditions:
- Acceptance criteria:
```
