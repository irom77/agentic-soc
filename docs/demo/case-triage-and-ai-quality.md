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

Do not present planned features as clickable functionality. The runnable presentation on this branch is Parts 1–4 below. Part 5 is a preview of the prepared future dataset.

## Part 1: Start and verify the demo

1. From the repository root, start ASP:

   ```bash
   ./start.sh
   ```

   This starts PostgreSQL, Redis, RustFS, the backend, the frontend, and the Case analysis worker. Runtime logs are under `.asp-runtime/`.

2. Refresh the deterministic dataset and add both Cases for real LLM runs:

   ```bash
   cd backend
   uv run python manage.py seed_case_triage_demo --include-live-llm --include-complex-live-llm
   ```

   This creates 27 Cases: 18 triage, 7 closed quality examples, and 2 unprocessed live-LLM Cases. It does not queue or invoke the LLM yet.

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

### B. Show the Case before the LLM call

1. Open **Cases** and search for `[DEMO LIVE LLM]`.
2. Open **Suspicious privileged login investigation**.
3. Explain the supplied evidence in the description: a privileged identity, impossible travel, an unapproved source IP, and identity-administration API access.
4. Open the **Investigation** tab.
5. Confirm that it shows **No data**. At this point `investigation_report_ai_json` is empty, the AI fields are empty, and no `CaseAnalysisJob` exists.
6. Explain that opening or refreshing this tab only reads a saved report; it never sends the Case to an LLM.

### C. Send the Case to the LLM and show the result

1. From `backend`, run:

   ```bash
   uv run python manage.py queue_live_llm_case_demo
   ```

   This is the exact presentation moment when analysis is requested. The command creates a Pending `CaseAnalysisJob`; the continuously running worker claims it and sends the serialized Case and retrieved Knowledge context to the LLM provider.

2. Return to the already-open Investigation tab. It does not update automatically, so wait a few seconds and use its refresh button.
3. After the worker succeeds, the tab changes from **No data** to the structured report.
4. Walk through the generated verdict, severity, impact, priority, confidence, digest, evidence findings, attack chain/timeline, indicators, remediation, and unknowns.
5. Return to the Case details and show that the same response populated the Case's denormalized AI fields.

The before/after state is:

| Moment | Analysis job | Case AI fields | Investigation tab |
| --- | --- | --- | --- |
| Immediately after seeding | None | Empty | **No data** |
| Immediately after queue command | Pending or Running | Empty | **No data** |
| Worker completes successfully | Success | Populated | Structured LLM report |

### D. Explain how the verdict was produced

The verdict is an LLM recommendation, not the result of a hard-coded True Positive rule. For the seeded live Case, the investigation input contains:

- The Case title and description.
- Category `IAM` and the identity, privileged-access, and impossible-travel tags.
- The current structured Case fields, including High severity, impact, and priority and Medium confidence. The prompt tells the model to treat these as reference values and reassess them.
- Case timestamps, status, assignee, Summary, and audit history.
- Any related Alerts, enrichments, comments, audit entries, and matching Knowledge records that exist at run time.

The initial seeded Case deliberately has no related Alerts, artifacts, enrichments, comments, or Knowledge records. Its substantive evidence is therefore limited to these three assertions in the description:

1. A privileged account successfully signed in from a new country shortly after a successful login from its usual location.
2. The new source IP was outside the approved VPN range.
3. The account subsequently accessed identity-administration APIs.

In the observed demo run, the model used those assertions to report:

- Impossible travel as evidence of possible credential compromise or session hijacking.
- The unapproved network as evidence that the access did not follow the expected VPN path.
- Identity-administration API access as a high-risk post-login action by a privileged identity.

It then selected `True Positive`. That selection is model judgment: the prompt asks whether the Case is closer to a real incident, Suspicious, False Positive, Benign, or Insufficient Data, but it does not encode a formula that forces True Positive for these inputs. A different conforming model or added context may return a different verdict.

Be explicit about the boundary between evidence and inference:

| Report statement | Classification |
| --- | --- |
| The description says the login succeeded | Supplied Case assertion |
| The source was outside the approved VPN range | Supplied Case assertion |
| Identity-administration APIs were accessed | Supplied Case assertion |
| Credentials were compromised or a session was hijacked | LLM inference, not confirmed |
| The actor attempted privilege escalation or configuration changes | LLM inference, not confirmed |
| The activity is a True Positive | LLM recommendation requiring analyst validation |

The model should list missing account identity, source IP, exact timestamps, API calls, resulting changes, authentication method, and broader scope under **Unknowns**. Because the seed lacks the underlying telemetry, an analyst can reasonably challenge a High-confidence True Positive and prefer Suspicious or Medium confidence. Use that disagreement to demonstrate why the Investigation report exposes evidence and unknowns instead of presenting the verdict as ground truth.

Suggested narration:

> The model classified this as True Positive because the Case text asserts a successful impossible-travel login followed by privileged identity API access. Those are strong signals, but the raw authentication and API events are not attached to this seeded Case. The compromise and attacker intent are inferences, so an analyst should validate the report and may lower the verdict or confidence until the missing telemetry is obtained.

The key architecture to explain is:

```text
Case/Alert creation → pending CaseAnalysisJob → case-analysis worker
→ structured-output LLM provider → saved AI fields and Investigation report
```

The seed command uses `trigger=demo_live_llm`, making the run distinguishable from the prepared reports, whose trigger is `demo-seed`.

### E. Prove that the run was live

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

After correcting the provider, rerun `seed_case_triage_demo --include-live-llm` to recreate the empty Case, then run `queue_live_llm_case_demo` at the presentation cue. Failed jobs are retained as evidence and are not automatically retried.

## Part 4: Demonstrate artifact enrichment in a complex investigation

This example is independent of the simple Case in Part 3. It demonstrates that the LLM receives structured related evidence, not just assertions copied into the Case description.

### A. Show the enriched evidence before analysis

1. Search Cases for `[DEMO COMPLEX LLM]` and open **Correlated identity and endpoint activity**.
2. Open its **Investigation** tab and confirm **No data**. The seed created no analysis job and made no LLM call.
3. Inspect the related records before queueing. The Case contains two temporally correlated Alerts:

   - An allowed interactive sign-in by `svc-finance-automation` from `198.51.100.42` followed by privileged-role enumeration.
   - Eight minutes later, encoded PowerShell launched under the same account on `fin-app-07.corp.example`.

4. Open the artifacts/enrichments visible from the Case and Alerts. Point out:

   - Source IP reputation: recent credential-stuffing activity with high confidence.
   - Identity context: a non-interactive finance service account with no approved interactive sign-ins.
   - CMDB context: the affected host is a High-criticality production finance server.
   - Process-tree review: no matching approved deployment, while outbound network telemetry remains unavailable.

All domains and IP addresses are documentation-only examples. They are not live threat indicators.

### B. Queue the enriched Case

At the presentation cue, run from `backend`:

```bash
uv run python manage.py queue_complex_llm_case_demo
```

Refresh Investigation after the worker finishes. Walk through how the report joins the identity event, endpoint event, shared account artifact, IP reputation, identity policy, and asset criticality into one timeline and set of evidence findings.

### C. Explain exactly what the LLM received

The serializer builds this nested structure at run time:

```text
Case
├── Alert: unfamiliar service-account sign-in
│   ├── Artifact: source IP
│   │   └── Enrichment: threat-intelligence reputation
│   └── Artifact: service account
│       └── Enrichment: identity directory context
└── Alert: encoded PowerShell
    ├── Artifact: same service account (and its identity enrichment)
    ├── Artifact: finance application host
    │   └── Enrichment: CMDB asset context
    ├── Artifact: redacted command line
    └── Enrichment: EDR process-tree review
```

The investigation profile sends the Alerts' descriptive and detection fields; each artifact's name, type, role, and value; and each enrichment's name, type, provider, value, and description. The enrichment `data` JSON is retained in the product database but is not part of the current investigation profile, so do not claim the LLM saw fields such as the numeric risk score.

### D. Discuss evidence, inference, and expected judgment

The strongest supplied evidence is the sequence and correlation: an account whose directory context disallows interactive use performs an unusual allowed sign-in, then the same account runs encoded PowerShell on a critical production host without an approved change. The reputation enrichment strengthens the source-IP signal. This gives the model substantially more grounded evidence than Part 3.

The report is still a recommendation, and its exact values are not predetermined. A model may reasonably choose True Positive with High confidence, but it must not claim that payload execution, persistence, data theft, or command-and-control succeeded. Outbound telemetry is explicitly unavailable, and the command payload is redacted. Those belong in **Unknowns** and follow-up recommendations.

Suggested narration:

> Here the model is not relying on a prose-only Case summary. It correlates two Alerts through a shared account and interprets artifact enrichments from threat intelligence, the identity directory, CMDB, and EDR review. The evidence strongly supports unauthorized activity, while the missing network telemetry and redacted payload limit claims about the incident's full impact.

To prove this run was live:

```bash
uv run python manage.py shell -c "from apps.agentic.models import CaseAnalysisJob; j=CaseAnalysisJob.objects.filter(trigger='demo_complex_live_llm').latest('created_at'); print(j.status, j.started_at, j.completed_at, j.error)"
```

## Part 5: Preview the prepared AI Quality dataset

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
