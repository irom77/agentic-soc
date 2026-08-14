# Case Triage, Live LLM Investigation, and AI Quality Demo

## What this branch can demonstrate

| Module | Status | Demo method |
| --- | --- | --- |
| Case queue and individual triage | Available now | Use the 18 `[DEMO TRIAGE]` Cases |
| Case Investigation report | Available now | Inspect seeded reports or run one real LLM investigation |
| LLM provider configuration and test | Available now | Use **System Settings → LLM Providers** |
| Bulk Triage | Not implemented yet | Explain the planned workflow only; there is no button or API |
| Per-Case AI–Human Agreement | Not implemented yet | Seed data is prepared for it, but no comparison component exists |
| Global AI Quality | Not implemented yet | Seed data is prepared for it, but there is no System Settings tab |

Do not present planned features as clickable functionality. The runnable presentation on this branch is Parts 1–3 below. Part 4 is a preview of the prepared future dataset.

## Part 1: Start and verify the demo

1. From the repository root, start ASP:

   ```bash
   ./start.sh
   ```

   This starts PostgreSQL, Redis, RustFS, the backend, the frontend, and the Case analysis worker. Runtime logs are under `.asp-runtime/`.

2. Refresh the deterministic dataset and add one Case for a real LLM run:

   ```bash
   cd backend
   uv run python manage.py seed_case_triage_demo --include-live-llm
   ```

   This creates 26 Cases: 18 triage, 7 closed quality examples, and 1 live-LLM Case. The seed code does not invoke an LLM itself. It queues the live Case, and the running Case analysis worker performs the external LLM call.

3. Browse to `http://localhost:5173` and choose the **Platform** login method.

4. Sign in as `demo.admin` with password `demopass`.

5. Open **Cases**, search for `[DEMO`, and confirm the groups are visible. The table supports page sizes 20, 50, and 100; it does not offer a page size of 10.

## Part 2: Demonstrate Case triage available now

1. Search for `[DEMO TRIAGE]`. Expect 18 Cases.
2. Point out the mixed New, In Progress, and On Hold states, different categories, assignees, and structured severity/impact/priority/confidence fields.
3. Open `[DEMO TRIAGE] Identity campaign signal 01`.
4. Walk through the Case details, Summary, related records, comments, audit history, and Investigation tab.
5. Edit one Case using the existing individual Case controls. For example, assign it to `demo.alice`, set it In Progress, and record the analyst verdict.
6. Return to the queue and show that the saved values appear in the table.

Suggested narration:

> The current branch supports Case-level analyst triage and preserves structured human decisions. The seeded queue gives us repeatable states for demonstrating those controls. Multi-select Bulk Triage is planned but is not present on this branch.

To restore the starting state after editing Cases, rerun the seed command.

## Part 3: Demonstrate live LLM Case investigation

### A. Verify the LLM provider

1. As `demo.admin`, open **System Settings → LLM Providers**.
2. Confirm at least one provider is Enabled.
3. Open the provider and confirm it has the `structured_output` tag. Case investigation selects a provider using this tag.
4. Click **Test**. Continue only when the provider test succeeds.
5. Do not expose the API key while presenting.

### B. Show the live Case and its result

1. Open **Cases** and search for `[DEMO LIVE LLM]`.
2. Open **Suspicious privileged login investigation**.
3. Explain the supplied evidence in the description: a privileged identity, impossible travel, an unapproved source IP, and identity-administration API access.
4. Open the **Investigation** tab.
5. If the report is still being generated, wait a few seconds and use the tab's refresh button. The UI does not currently start analysis manually or update automatically.
6. Walk through the generated verdict, severity, impact, priority, confidence, digest, evidence findings, attack chain/timeline, indicators, remediation, and unknowns that the model returned.
7. Return to the Case details and show the denormalized AI fields beside the analyst-managed Case fields.

The key architecture to explain is:

```text
Case/Alert creation → pending CaseAnalysisJob → case-analysis worker
→ structured-output LLM provider → saved AI fields and Investigation report
```

The seed command uses `trigger=demo_live_llm`, making the run distinguishable from the prepared reports, whose trigger is `demo-seed`.

### C. Prove that the run was live

Run this from `backend`:

```bash
uv run python manage.py shell -c "from apps.agentic.models import CaseAnalysisJob; j=CaseAnalysisJob.objects.filter(trigger='demo_live_llm').latest('created_at'); print(j.status, j.started_at, j.completed_at, j.error)"
```

Expected status is `Success`. The start and completion timestamps were produced by the worker during this run.

If the status is `Failed`, inspect the exact failure and worker log:

```bash
uv run python manage.py shell -c "from apps.agentic.models import CaseAnalysisJob; j=CaseAnalysisJob.objects.filter(trigger='demo_live_llm').latest('created_at'); print(j.error)"
tail -n 100 ../.asp-runtime/case-analysis-worker.log
```

After correcting the provider, rerun `seed_case_triage_demo --include-live-llm` to create a fresh pending job. Failed jobs are retained as evidence and are not automatically retried.

## Part 4: Preview the prepared AI Quality dataset

Search for `[DEMO QUALITY]`. These seven Closed Cases make future AI quality behavior concrete even though the evaluator and UI are not implemented:

| Case | Prepared scenario |
| --- | --- |
| Ransomware behavior confirmed | AI and human values agree across five fields |
| Approved VPN created impossible travel | AI overestimates risk and verdict differs |
| Executive phishing campaign | AI underestimates risk |
| DNS tunneling investigation | Mixed agreement |
| Inconclusive cloud process activity | `Unknown` value semantics |
| Closed without an AI prediction | Missing-prediction coverage |
| Closed with an invalid AI prediction | Invalid-prediction coverage |

Open any valid example and use **Investigation** to show its prepared report. Make clear that these reports are deterministic fixtures, not calls made during the presentation.

Use **AI–Human Agreement**, **agreement rate**, and **mismatch** when describing the planned evaluator. Avoid calling the future metric AI accuracy or correctness: a final human disposition is a comparison reference, not proof of objective truth.

### Planned, not runnable on this branch

- Cross-page selection and Bulk Triage.
- Per-Case five-field AI–Human comparison.
- **System Settings → AI Quality** coverage, agreement, direction, confusion matrix, trend, filters, and sample drilldown.
- Evaluation lifecycle rebuild on close, reopen, and human-field correction.
- `rebuild_ai_quality_evaluations` management command.

## Close and reset

Reset only the scoped demo Cases:

```bash
cd backend
uv run python manage.py reset_case_triage_demo --confirm
```

Stop ASP while preserving database volumes:

```bash
cd ..
./stop.sh
```
