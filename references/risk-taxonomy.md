# AI Product Risk Taxonomy

Every risk uses the same fields:

`风险编号｜类别｜触发条件｜影响｜当前控制｜降级方案｜验证方法｜状态`

## 1. Facts, Hallucination, and Incorrect Citations

Cover unsupported claims, fabricated sources, wrong source mapping, stale
facts, internal contradictions, and citation content that does not support the
claim.

Required controls usually include grounding-only generation, mandatory
citations, no-evidence refusal, citation validation, and explicit separation
between facts and inference.

## 2. Model Capability Boundaries

Cover long context, complex tables, ambiguous questions, domain terminology,
multilingual content, weak OCR, conflicting documents, and tasks that require
authoritative human judgment.

Define both model-level fallback and product-level human escalation.

## 3. Input Ambiguity and Data Quality

Cover missing metadata, malformed files, OCR errors, outdated versions,
duplicate documents, permission gaps, sensitive content, and contradictory
sources.

Define validation, quarantine, versioning, and fail-closed behavior.

## 4. Error Propagation and Automation Runaway

Cover persistent bad indexes, stale caches, prompt or model regressions,
automated actions, retries, downstream consumers, and duplicated errors.

Define version pinning, rollback, circuit breakers, idempotency, and stopping
conditions.

## 5. Human Confirmation and Responsibility Boundaries

Cover users treating model output as formal policy or approval, unclear
accountability, missing escalation, over-trust, and unreviewed high-impact
answers.

Define disclaimer behavior, review responsibility, escalation paths, and
audit records.

## 6. Evaluation, Monitoring, and Rollback

Cover missing golden datasets, weak online metrics, no regression gate,
unmonitored refusal or citation quality, lack of version rollback, and no
incident replay.

Define offline evaluation, online monitoring, canary release, rollback
criteria, and ownership.

## Status Values

Use a small local set such as:

- `OPEN`
- `MITIGATING`
- `CONTROLLED`
- `ACCEPTED`

Do not confuse risk status with pipeline status.
