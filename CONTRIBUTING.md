# Contributing

## Before Opening a Pull Request

1. Describe the problem and the smallest behavior change that solves it.
2. Add or update tests.
3. Run:

```bash
pytest
ruff check .
python scripts/harness.py self-test
```

4. Update `CHANGELOG.md`.
5. Confirm that no private documents, credentials, endpoints, or run logs are
   included.

## Rule Changes

The following changes are breaking changes:

- adding or removing a pipeline status
- changing Gate behavior
- changing `review_state` transitions
- changing the required stage order
- changing the report artifact contract

Breaking changes require migration notes.

## Data Policy

Use synthetic examples only. Do not submit company documents, customer data,
personal information, API keys, private URLs, or model credentials.
