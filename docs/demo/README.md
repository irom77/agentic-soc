# Case Triage and AI Quality Demo

This folder contains the repeatable demonstration package for:

- Bulk Case triage.
- Per-Case AI–Human Agreement.
- Global AI Quality analytics.

Start with [Setup and reset](setup-and-reset.md), then use the presenter script in [Case triage and AI quality](case-triage-and-ai-quality.md).

The seed command creates a small, clearly labeled dataset and never calls an LLM. The reset command deletes only Cases whose `correlation_uid` starts with `DEMO-CASE-TRIAGE-`. Related analysis jobs and future quality evaluations are removed through their Case relationships.

## Current branch status

The seed/reset commands work with the current Case and `CaseAnalysisJob` models. The v0.6.0 bulk-triage API and AI Quality evaluation model/UI are still specifications on this branch. Until those features are implemented, the seeded Cases can be inspected through the existing Case list and Investigation tab, but the Bulk Triage action and global AI Quality page will not appear.

The seed command detects a future `rebuild_ai_quality_evaluations` management command. When available, it runs that command after seeding so the same dataset becomes immediately usable by the completed AI Quality page.

## Dataset at a glance

| Group | Count | Purpose |
| --- | ---: | --- |
| `[DEMO TRIAGE]` | 18 | Cross-page selection, combined field updates, partial success, close, and reopen |
| `[DEMO QUALITY]` with valid prediction | 5 | Agreement, mismatch, overestimate, underestimate, and `Unknown` semantics |
| `[DEMO QUALITY]` without prediction | 1 | `No prediction` coverage state |
| `[DEMO QUALITY]` with malformed result | 1 | `Invalid prediction` coverage state |

The command also creates or refreshes three local users:

| Username | Password | Intended role |
| --- | --- | --- |
| `demo.admin` | `demopass` | Admin; global AI Quality and all triage actions |
| `demo.alice` | `demopass` | Analyst |
| `demo.bob` | `demopass` | Analyst |

These credentials are for local demonstrations only.
