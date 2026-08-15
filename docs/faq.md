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
