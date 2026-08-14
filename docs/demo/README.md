# ASP Feature Demo

This folder contains the repeatable demonstration package for the Case workflow and Agentic SOC investigation.

Start with [Setup and reset](setup-and-reset.md), then follow [Case triage, live LLM investigation, and AI quality](case-triage-and-ai-quality.md).

The walkthrough includes numbered screenshots from the local ASP demo for the Case queue, every Case tab, nested Alert and Artifact evidence, and the Investigation before/after state.

## Feature status on this branch

| Feature | Status |
| --- | --- |
| Case queue and individual Case triage | Available |
| Seeded Investigation reports | Available |
| Live structured-output LLM Case investigation | Available through queued jobs and the worker |
| Live AlienVault OTX artifact enrichment | Available through the Threat Intelligence playbook and worker |
| LLM Providers administration and connection test | Available |
| Bulk Triage | Not implemented |
| Per-Case AI–Human Agreement | Not implemented |
| Global AI Quality page and evaluation lifecycle | Not implemented |

The default seed creates 25 Cases and never schedules an external call. Add `--include-live-llm` for the simple text-only investigation, `--include-complex-live-llm` for a deterministically enriched investigation, and `--include-live-otx` for real AlienVault OTX enrichment. Each added Case initially has no analysis job. Queue enrichment first for the OTX Case, then queue its LLM investigation.

## Dataset at a glance

| Group | Count | Purpose |
| --- | ---: | --- |
| `[DEMO TRIAGE]` | 18 | Current Case queue and individual triage; future Bulk Triage |
| `[DEMO QUALITY]` | 7 | Seeded Investigation reports and future AI–Human Agreement evaluation |
| `[DEMO LIVE LLM]` | 0 or 1 | Real LLM investigation, included only with `--include-live-llm` |
| `[DEMO COMPLEX LLM]` | 0 or 1 | Correlated Alerts, artifacts, and enrichments, included only with `--include-complex-live-llm` |
| `[DEMO LIVE OTX]` | 0 or 1 | Empty-to-live OTX enrichment-to-LLM workflow, included only with `--include-live-otx` |

The command creates or refreshes three local-only users:

| Username | Password | Role |
| --- | --- | --- |
| `demo.admin` | `demopass` | Platform administrator |
| `demo.alice` | `demopass` | Analyst |
| `demo.bob` | `demopass` | Analyst |
