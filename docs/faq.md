# Frequently Asked Questions

## Are Workers agents?

No. A Worker describes how code runs, while an agent describes how decisions are made.

A Worker is a long-running Django process that polls for work and executes it. An agent typically works toward a goal by deciding which tools or actions to use, observing their results, and adapting its next steps. A Worker can host an agent or an agentic workflow, but the Worker itself is execution infrastructure rather than an agent.

## Is the Case Analysis Worker an agent?

The Case Analysis Worker is best described as an LLM-assisted workflow running inside a background Worker. Calling it a Case Analysis Agent can be useful as a product term, but the current implementation is a bounded workflow rather than a fully autonomous agent.

Its sequence is defined in Python:

1. Claim a pending Case analysis job.
2. Load and serialize the Case and its evidence.
3. Ask the LLM for Knowledge search keywords.
4. Search Knowledge records through the Django ORM.
5. Ask the LLM for a structured investigation report.
6. Save the report and mark the job as Success or Failed.

The LLM performs bounded reasoning within this sequence. It does not dynamically select arbitrary tools, modify the workflow, or continue through an open-ended plan-and-observe loop.

Use these terms when discussing the component:

- **Case Analysis Worker** for the deployed Django process.
- **Case analysis job** for one queued analysis request.
- **Case Analysis workflow** for the fixed orchestration of analysis steps.
- **LLM-assisted analyst** for its user-facing behavior.
- **Case Analysis Agent** only as a broader product term for the bounded agentic behavior.

## What is Case serialization, and why is it needed?

Serialization converts a Django `Case` and its related evidence into a plain Python dictionary that can be encoded as JSON and included in an LLM message. An LLM cannot consume a Django model object directly, so the Case Analysis workflow creates a controlled snapshot of the data the model is allowed to see.

The Investigation serialization profile:

- selects relevant Case triage fields;
- includes related Alerts, Artifacts, summarized Enrichments, comments, and filtered audit history;
- converts values such as dates and UUIDs into JSON-compatible strings;
- represents the assignee by display name instead of passing a Django user object; and
- excludes internal identifiers, raw/unmapped Alert data, full Enrichment data, and previous AI-generated Case fields.

Serialization only reads the database and builds the request payload. It does not modify the Case, call the LLM, or save an investigation report. The resulting dictionary is subsequently used for Knowledge keyword generation and as part of the final investigation prompt.

## Are the other Workers agents?

No. The current Workers provide execution infrastructure for different kinds of work:

| Worker | Responsibility |
| --- | --- |
| Case Analysis | Runs a fixed LLM and Knowledge-retrieval workflow. |
| Playbook | Executes a predefined Playbook script. |
| Agentic Module | Loads Modules and processes Redis Stream messages. |
| ELK Action | Polls and normalizes ELK Action documents. |
| Dashboard Cache | Periodically calculates and caches dashboard data. |

The useful architectural distinction is: **Workers provide the execution infrastructure; agentic workflows and Playbooks can run inside Workers, but the Workers themselves are not agents.**

The Case Analysis component would more closely match the technical meaning of an agent if it gained dynamic tool selection, observation-driven iteration, planning, and explicit termination rules.

For implementation details, see [Workers and Agentic Runtime](technical/workers-and-runtime.md) and [LLM investigation and enrichment](technical/llm-and-enrichment.md).

## How difficult would it be to replace Django while keeping React?

Keeping React is straightforward if the replacement backend preserves the existing `/api` and WebSocket contracts. Replacing Django itself would be a major migration because Django currently provides more than HTTP routing: the project depends on its ORM and migrations, authentication and permissions, serialization and validation, audit signals, storage, Redis-backed realtime events, management commands, and background Workers. The Python implementation also contains the existing LLM, SIEM, threat-intelligence, CMDB, Splunk, Elasticsearch, and OpenCTI integrations.

A complete Bun and Elysia rewrite would therefore be one of the highest-effort options. It would require replacing the Django data model and rewriting Python-specific Workers and integrations in TypeScript. For one experienced developer, full production parity would likely take several months rather than weeks.

Lower-effort options are:

| Option | Relative effort | Result |
| --- | --- | --- |
| Improve the existing Django/DRF backend | Lowest | Retains the current architecture while addressing measured performance or maintainability problems. |
| Gradually replace DRF endpoints with Django Ninja | Low | Adds typed schemas and more explicit endpoints while retaining Django models, migrations, authentication, and Workers. |
| Add FastAPI as the HTTP layer while temporarily retaining Django models and Workers | Medium | Provides a gradual path away from DRF, but Django remains a dependency during the transition. |
| Replace Django with FastAPI or Litestar and SQLAlchemy | High | Eliminates Django while preserving more of the existing Python integrations and workflow code. |
| Replace Django with Bun and Elysia | Highest | Moves to a TypeScript backend but requires the broadest rewrite. |

The recommended choice depends on the goal:

- For performance, profile and optimize the existing ASGI Django application first.
- For typed request and response schemas, migrate selected DRF endpoints to Django Ninja.
- If eliminating Django is mandatory, use a gradual FastAPI migration and retain the Python Workers until their interfaces are separated from Django.
- Choose Bun and Elysia only when adopting a TypeScript-only backend is valuable enough to justify a full rewrite.

Generating TypeScript types or a frontend client from the existing OpenAPI schema can provide frontend/backend type sharing without replacing Django.
