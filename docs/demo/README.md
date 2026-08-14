# ASP Feature Demo

This folder contains the repeatable demonstration package for the Case workflow and Agentic SOC investigation.

Start with [Setup and reset](setup-and-reset.md), then follow [Case triage, live LLM investigation, and AI quality](case-triage-and-ai-quality.md).

The walkthrough defines a numbered screenshot sequence for the Case queue, every Case tab, nested Alert and Artifact evidence, and the Investigation before/after state. Image references use the repository placeholder convention (`img.png`, `img_1.png`, and so on); replace them with captures from the local demo environment before publishing the guide.

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

The default seed creates 25 Cases and never schedules an external LLM call. Add `--include-live-llm` for the simple text-only investigation, `--include-complex-live-llm` for an enriched investigation, or both. Each added Case initially shows **No data** in Investigation. Its matching queue command starts the real LLM run.

## Dataset at a glance

| Group | Count | Purpose |
| --- | ---: | --- |
| `[DEMO TRIAGE]` | 18 | Current Case queue and individual triage; future Bulk Triage |
| `[DEMO QUALITY]` | 7 | Seeded Investigation reports and future AI–Human Agreement evaluation |
| `[DEMO LIVE LLM]` | 0 or 1 | Real LLM investigation, included only with `--include-live-llm` |
| `[DEMO COMPLEX LLM]` | 0 or 1 | Correlated Alerts, artifacts, and enrichments, included only with `--include-complex-live-llm` |

The command creates or refreshes three local-only users:

| Username | Password | Role |
| --- | --- | --- |
| `demo.admin` | `demopass` | Platform administrator |
| `demo.alice` | `demopass` | Analyst |
| `demo.bob` | `demopass` | Analyst |
