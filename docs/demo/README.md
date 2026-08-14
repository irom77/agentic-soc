# ASP Feature Demo

This folder contains the repeatable demonstration package for the Case workflow and Agentic SOC investigation.

Start with [Setup and reset](setup-and-reset.md), then follow [Case triage, live LLM investigation, and AI quality](case-triage-and-ai-quality.md).

## Feature status on this branch

| Feature | Status |
| --- | --- |
| Case queue and individual Case triage | Available |
| Seeded Investigation reports | Available |
| Live structured-output LLM Case investigation | Available through queued jobs and the worker |
| LLM Providers administration and connection test | Available |
| Bulk Triage | Not implemented |
| Per-Case AI–Human Agreement | Not implemented |
| Global AI Quality page and evaluation lifecycle | Not implemented |

The default seed creates 25 Cases and never schedules an external LLM call. Add `--include-live-llm` to create a 26th unprocessed Case. Its Investigation tab initially shows **No data**. Run `queue_live_llm_case_demo` when ready; the Case analysis worker then calls the enabled `structured_output` provider and saves the report shown by the tab.

## Dataset at a glance

| Group | Count | Purpose |
| --- | ---: | --- |
| `[DEMO TRIAGE]` | 18 | Current Case queue and individual triage; future Bulk Triage |
| `[DEMO QUALITY]` | 7 | Seeded Investigation reports and future AI–Human Agreement evaluation |
| `[DEMO LIVE LLM]` | 0 or 1 | Real LLM investigation, included only with `--include-live-llm` |

The command creates or refreshes three local-only users:

| Username | Password | Role |
| --- | --- | --- |
| `demo.admin` | `demopass` | Platform administrator |
| `demo.alice` | `demopass` | Analyst |
| `demo.bob` | `demopass` | Analyst |
