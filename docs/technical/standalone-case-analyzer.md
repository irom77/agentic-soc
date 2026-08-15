# Standalone Case Analyzer

The standalone analyzer applies the Case Analysis Worker's core LLM workflow to security cases exported as JSON. It does not require Django, the Agentic SOC database, job queues, or a running platform deployment.

Its external interface is deliberately small: normalized Case JSON and optional knowledge go in, and a validated `InvestigationReport` JSON document comes out. Source-specific adapters translate generic JSON and exports from other SOAR platforms into the canonical Case representation.

See [`case-analyzer/README.md`](../../case-analyzer/README.md) for setup, CLI examples, configuration, supported input fields, and privacy considerations.

For a detailed explanation of every module and the complete execution path, see the [Case Analyzer code walkthrough](../../case-analyzer/case-analyzer-code.md).

## Relationship to the worker

The production worker currently performs four jobs:

1. Serialize Django Case records and their related evidence.
2. Retrieve internal Knowledge records from PostgreSQL.
3. Invoke the LLM and validate its structured report.
4. Persist the report and update the Case analysis job.

The standalone package implements the third job and accepts plain JSON at its seam. Its adapters provide the equivalent of the first job for exported files. Knowledge is optional and supplied as a JSON array; scheduling and persistence remain the responsibility of the calling platform.

The existing Django worker has not yet been changed to import this package. Keeping that integration as a separate step avoids changing production behavior while the standalone adapters are validated with real, sanitized SOAR exports.
