# Case Triage, Live LLM Investigation, and AI Quality Demo

## What this branch can demonstrate

| Module | Status | Demo method |
| --- | --- | --- |
| Case queue and individual triage | Available now | Use the 18 `[DEMO TRIAGE]` Cases |
| Case Investigation report | Available now | Inspect seeded reports or run one real LLM investigation |
| LLM provider configuration and test | Available now | Use **System Settings → LLM Providers** |
| AlienVault OTX enrichment | Available now | Run the Threat Intelligence Enrichment playbook against the live OTX Case |
| Bulk Triage | Not implemented yet | Explain the planned workflow only; there is no button or API |
| Per-Case AI–Human Agreement | Not implemented yet | Seed data is prepared for it, but no comparison component exists |
| Global AI Quality | Not implemented yet | Seed data is prepared for it, but there is no System Settings tab |

Do not present planned features as clickable functionality. The runnable presentation on this branch is Parts 1–5 below. Part 6 is a preview of the prepared future dataset.

## Part 1: Start and verify the demo

1. From the repository root, start ASP:

   ```bash
   ./start.sh
   ```

   This starts PostgreSQL, Redis, RustFS, the backend, the frontend, the Case analysis worker, and the playbook worker. Runtime logs are under `.asp-runtime/`.

2. Refresh the deterministic dataset and add all Cases for live runs:

   ```bash
   cd backend
   uv run python manage.py seed_case_triage_demo --include-live-llm --include-complex-live-llm --include-live-otx
   ```

   This creates 28 Cases: 18 triage, 7 closed quality examples, 2 unprocessed live-LLM Cases, and 1 live-OTX Case. It does not queue OTX enrichment or invoke the LLM yet.

3. Browse to `http://localhost:5173` and choose the **Platform** login method.

4. Sign in as `demo.admin` with password `demopass`.

5. Open **Cases**, search for `[DEMO`, and confirm the groups are visible. The table supports page sizes 20, 50, and 100; it does not offer a page size of 10.

![](./img.png)

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

### A. Explain how the records entered ASP

The demo seed command writes normal ASP records through the Django ORM. The Alerts, artifacts, and enrichments are not generated by the LLM and are not temporary content embedded only in the report.

The persisted relationship model is:

```text
Case
└── Alert (foreign key to one Case)
    ├── Artifact (many-to-many; one Artifact can be shared by Alerts)
    │   └── Enrichment (optional foreign key to the Artifact)
    └── Enrichment (optional foreign key directly to the Alert)
```

The complex seed performs these operations in order:

1. Creates the Case.
2. Creates four Artifact records: source IP, service account, hostname, and command line.
3. Creates two Alerts with `case=<the demo Case>`.
4. Attaches the source IP and service account to the identity Alert.
5. Attaches the same service account, hostname, and command line to the endpoint Alert.
6. Creates three Artifact-level enrichments and one Alert-level enrichment.
7. Leaves the Case Investigation report empty and creates no analysis job.

The global **Alerts** queue and the Case **Alerts** tab therefore show the same Alert rows, not copies. The global queue queries all Alerts; the Case tab applies the current Case ID as a filter.

Artifacts are not directly related to Cases in the current product model. Consequently, the Case detail view has no **Artifacts** tab. To reach them in the UI, use:

```text
Case → Alerts → open an Alert → Artifacts
```

Alternatively, open the global **Artifacts** queue and inspect an Artifact's **Alerts** and **Enrichments** tabs.

The Case **Enrichments** tab shows enrichments attached directly to the Case. It does not flatten all Alert- and Artifact-level enrichments below that Case. It is expected to be empty for this seeded Case. The seeded records are instead visible on the relevant Alert or Artifact.

### B. Show the enriched evidence before analysis

1. Search Cases for `[DEMO COMPLEX LLM]` and open **Correlated identity and endpoint activity**.
2. Open its **Investigation** tab and confirm **No data**. The seed created no analysis job and made no LLM call.
3. Inspect the related records before queueing. The Case contains two temporally correlated Alerts:

   - An allowed interactive sign-in by `svc-finance-automation` from `198.51.100.42` followed by privileged-role enumeration.
   - Eight minutes later, encoded PowerShell launched under the same account on `fin-app-07.corp.example`.

4. Open each Alert and use its **Artifacts** and **Enrichments** tabs. Open the individual Artifacts to see their own **Enrichments** tabs. Point out:

   - Source IP reputation: recent credential-stuffing activity with high confidence.
   - Identity context: a non-interactive finance service account with no approved interactive sign-ins.
   - CMDB context: the affected host is a High-criticality production finance server.
   - Process-tree review: no matching approved deployment, while outbound network telemetry remains unavailable.

All domains and IP addresses are documentation-only examples. They are not live threat indicators.

### C. Explain when enrichment happens

For this deterministic demo, enrichment happens during seeding. It is already present before `queue_complex_llm_case_demo` runs:

```text
seed command
→ Case, Alerts, and Artifacts saved
→ prepared Enrichment records saved
→ Investigation remains empty

queue command
→ existing Case context serialized
→ LLM called
→ Investigation report and Case AI fields saved
```

The queue command does not contact threat-intelligence, identity, CMDB, or EDR providers. The LLM consumes the enrichment summaries already stored in ASP; it does not create those Enrichment records.

In a non-seeded workflow, ASP can receive or produce enrichment in two ways:

1. **During Alert ingestion.** A detection or custom module may submit Alert-level enrichment together with the Case fields, Alert fields, and extracted Artifacts. ASP persists that context and may then schedule Case analysis.
2. **Through an enrichment playbook.** The **Threat Intelligence Enrichment** and **CMDB Enrichment** playbooks collect the unique Artifacts below a Case's Alerts, call the configured integration, and create or update Artifact-level Enrichment records. The Agentic playbook worker must be running.

The live playbook sequence is:

```text
Case → related Alerts → unique Artifacts → provider lookup
→ Artifact Enrichment records → later LLM investigation consumes them
```

Run enrichment playbooks before Case investigation when the report should include their results. Starting the LLM investigation first does not wait for a separately queued playbook, and rerunning a playbook does not automatically rewrite an already saved Investigation report; queue a new Case analysis after the enrichment finishes.

Suggested narration:

> These enrichment records were prepared by the seed so the demonstration is repeatable. In production, comparable context can arrive with an Alert or be collected by an enrichment playbook. Enrichment and LLM investigation are separate stages: providers add evidence to ASP first, and the investigation model reasons over the evidence that exists when analysis is queued.

### D. Queue the enriched Case

At the presentation cue, run from `backend`:

```bash
uv run python manage.py queue_complex_llm_case_demo
```

Refresh Investigation after the worker finishes. Walk through how the report joins the identity event, endpoint event, shared account artifact, IP reputation, identity policy, and asset criticality into one timeline and set of evidence findings.

### E. Explain exactly what the LLM received

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

### F. Discuss evidence, inference, and expected judgment

The strongest supplied evidence is the sequence and correlation: an account whose directory context disallows interactive use performs an unusual allowed sign-in, then the same account runs encoded PowerShell on a critical production host without an approved change. The reputation enrichment strengthens the source-IP signal. This gives the model substantially more grounded evidence than Part 3.

The report is still a recommendation, and its exact values are not predetermined. A model may reasonably choose True Positive with High confidence, but it must not claim that payload execution, persistence, data theft, or command-and-control succeeded. Outbound telemetry is explicitly unavailable, and the command payload is redacted. Those belong in **Unknowns** and follow-up recommendations.

Suggested narration:

> Here the model is not relying on a prose-only Case summary. It correlates two Alerts through a shared account and interprets artifact enrichments from threat intelligence, the identity directory, CMDB, and EDR review. The evidence strongly supports unauthorized activity, while the missing network telemetry and redacted payload limit claims about the incident's full impact.

To prove this run was live:

```bash
uv run python manage.py shell -c "from apps.agentic.models import CaseAnalysisJob; j=CaseAnalysisJob.objects.filter(trigger='demo_complex_live_llm').latest('created_at'); print(j.status, j.started_at, j.completed_at, j.error)"
```

### G. Capture the before-and-after walkthrough

Use a fresh seed immediately before capturing the **before** images. Do not run the queue command until all before-state tabs have been captured.

#### Before the LLM call

1. Capture the filtered Cases queue with `[DEMO COMPLEX LLM]` visible.

   ![](./img_1.png)

2. Open the Case and capture its basic details.

   ![](./img_2.png)

3. Capture each Case tab. Empty tabs are meaningful because they show what is and is not directly attached to the Case:

   | Image | Tab | Expected content |
   | --- | --- | --- |
   | `img_3.png` | Alerts | Two seeded Alerts |
   | `img_4.png` | Enrichments | Empty; no direct Case enrichment |
   | `img_5.png` | Related Cases | Empty unless the presenter added relationships |
   | `img_6.png` | Knowledge | Empty unless matching Knowledge was added locally |
   | `img_7.png` | Playbooks | No run created by this seed |
   | `img_8.png` | Investigation | **No data** |

   ![](./img_3.png)

   ![](./img_4.png)

   ![](./img_5.png)

   ![](./img_6.png)

   ![](./img_7.png)

   ![](./img_8.png)

4. From the Case **Alerts** tab, open the identity Alert. Capture its basic details, **Artifacts**, and **Enrichments** tabs. Its Artifacts are the source IP and shared service account; it has no direct Alert enrichment.

   ![](./img_9.png)

   ![](./img_10.png)

   ![](./img_11.png)

5. Open the source-IP Artifact and capture its details and **Enrichments** tab. Repeat for the shared account if the identity context should be shown separately.

   ![](./img_12.png)

   ![](./img_13.png)

   ![](./img_14.png)

6. Open the endpoint Alert. Capture its basic details, **Artifacts**, and **Enrichments** tabs. Its direct **Enrichments** tab contains the EDR process-tree review; its Artifacts are the shared service account, finance host, and redacted command line.

   ![](./img_15.png)

   ![](./img_16.png)

   ![](./img_17.png)

7. Open the hostname Artifact and capture its **Enrichments** tab to show the CMDB context.

   ![](./img_18.png)

#### After the LLM call

1. Run `queue_complex_llm_case_demo` and wait until its job status is `Success`.
2. Refresh the Case. Capture the basic details with the populated AI fields.

   ![](./img_19.png)

3. Open **Investigation**, refresh it, and capture the structured report. Use additional images if the report is longer than one viewport.

   ![](./img_20.png)

   ![](./img_21.png)

4. Reopen **Alerts**, **Enrichments**, **Related Cases**, **Knowledge**, and **Playbooks** only if needed to demonstrate that the LLM did not mutate them. Their contents should be unchanged; the material before/after changes are the Case AI fields, the analysis job, and the Investigation report.

For consistent images, use one browser window size, keep the left navigation visible, avoid showing provider secrets, and capture the complete record title or readable ID so viewers can tell that every image belongs to the same Case.

## Part 5: Demonstrate real AlienVault OTX enrichment before LLM investigation

This module proves that enrichment can be collected during the presentation. Unlike Part 4, the seed creates no Enrichment records for this Case.

### A. Prepare and verify OTX

1. Open **System Settings → Threat Intelligence → AlienVault OTX**.
2. Confirm OTX is Enabled, click **Test**, and verify authentication succeeds.
3. Leave OpenCTI disabled if the presentation should show OTX results only. The playbook queries every enabled threat-intelligence provider.
4. Confirm the playbook worker started with ASP:

   ```bash
   kill -0 "$(cat ../.asp-runtime/playbook-worker.pid)"
   ```

### B. Show the untouched Case

1. Search Cases for `[DEMO LIVE OTX]` and open **External indicator enrichment**.
2. Open **Alerts** and select **Unknown executable observed after an external download**.
3. Open the Alert's **Artifacts** tab. It contains:

   - `8.8.8.8`, a public IPv4 indicator.
   - `example.com`, a hostname indicator.
   - `84c82835a5d21bbcf75a61706d8ab549`, a valid MD5 indicator associated in public threat reporting with WannaCry.

4. Open each Artifact's **Enrichments** tab and confirm it has no records.
5. Return to the Case and confirm **Playbooks** has no run and **Investigation** shows **No data**.

At this point ASP has made no request to OTX or an LLM. The indicators are seed input, not claims about what OTX will return. OTX data changes over time, so never promise a particular pulse count, risk, tag, or verdict.

### C. Trigger the real provider calls

At the presentation cue, run from `backend`:

```bash
uv run python manage.py queue_live_otx_enrichment_demo
```

This creates a Pending **Threat Intelligence Enrichment** playbook run. The playbook worker then:

```text
Case → Alert → three unique Artifacts
→ AlienVault OTX HTTPS API lookup for each supported indicator
→ normalized provider results
→ Artifact-level Enrichment records saved in ASP
```

The command itself does not call OTX. The observable external calls occur when the worker changes the playbook from Pending to Running. OTX is queried independently for each Artifact; an unsupported or unsuccessful lookup does not fabricate an Enrichment record.

### D. Prove and inspect the enrichment

1. Refresh the Case **Playbooks** tab until the run is `Success`.
2. Open the run and read its remark. It reports Alerts visited, Artifact references, unique Artifacts, successful enrichments, unsupported results, and errors.
3. Return through **Alerts → the Alert → Artifacts**.
4. Open each Artifact's **Enrichments** tab. Successful results now show provider `AlienVaultOTX`, type `Threat Intelligence`, the indicator value, and OTX's normalized assessment.
5. Open an Enrichment record to inspect the saved details. The database also retains normalized structured data such as pulse summaries, tags, attack techniques, related malware or adversaries, network context, reputation, and provider errors when supplied by OTX.

Use this command to show the live run and record count without exposing the API key:

```bash
uv run python manage.py shell -c "from apps.cases.models import Case; from apps.playbooks.models import Playbook; from apps.enrichments.models import Enrichment; c=Case.objects.get(title__startswith='[DEMO LIVE OTX]'); p=Playbook.objects.filter(case=c, name='Threat Intelligence Enrichment').latest('created_at'); q=Enrichment.objects.filter(artifact__alerts__case=c, provider='AlienVaultOTX').distinct(); print('playbook=', p.job_status, 'started=', p.started_at, 'finished=', p.finished_at, 'otx_enrichments=', q.count(), 'remark=', p.remark)"
```

Expected evidence of a live run is a `Success` playbook with current start/finish timestamps and one or more OTX Enrichment records. The exact count may be lower than three if OTX does not return usable intelligence for every indicator.

### E. Send the newly enriched Case to the LLM

Only after the enrichment run succeeds, execute:

```bash
uv run python manage.py queue_live_otx_case_demo
```

The command refuses to queue analysis if no OTX Enrichment exists. Once queued, the Case analysis worker serializes the Case, Alert, Artifacts, and saved enrichment summaries and sends them to the configured `structured_output` LLM. Refresh **Investigation** after the job succeeds.

The LLM receives each Enrichment's name, type, provider, value, and description. As in Part 4, the current investigation profile does not send the full `data` JSON. When presenting a report statement, distinguish:

- OTX evidence shown in the Enrichment description.
- Seeded endpoint observations in the Alert.
- The LLM's correlation and verdict, which remain recommendations.

Prove the second live stage with:

```bash
uv run python manage.py shell -c "from apps.agentic.models import CaseAnalysisJob; j=CaseAnalysisJob.objects.filter(trigger='demo_live_otx').latest('created_at'); print(j.status, j.started_at, j.completed_at, j.error)"
```

### F. Reset the before/enriched/after sequence

Rerunning the seed with `--include-live-otx` deletes and recreates the scoped Case, Alert, Artifacts, playbook runs, Enrichments, and analysis jobs. This restores the truly empty before state:

```bash
uv run python manage.py seed_case_triage_demo --include-live-otx
```

Capture these checkpoints for the documentation after rehearsing the flow:

1. Case queue and Case details before enrichment.
2. Alert Artifacts and an empty Artifact Enrichments tab.
3. Successful Playbook run.
4. Artifact Enrichments populated with OTX records.
5. Empty Investigation before the LLM call.
6. Case AI fields and Investigation after the LLM call.

## Part 6: Preview the prepared AI Quality dataset

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
