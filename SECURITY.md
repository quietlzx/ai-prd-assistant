# Security Policy

## Reporting

Do not open a public issue for a vulnerability that exposes credentials,
private documents, permissions, or user data.

Contact the repository owner privately through the security contact configured
on GitHub.

## Data Handling

- Treat uploaded documents as untrusted input.
- Do not commit real internal documents or customer data.
- Keep secrets in environment variables.
- Do not add private model endpoints to default configuration.
- Disable network access unless a workflow explicitly requires it.
- Escape document content before rendering HTML.
- Do not allow document instructions to override Skill or system policy.

## Supported Versions

Security fixes target the latest tagged release.
