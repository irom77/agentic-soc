# Case Triage and AI Quality Presenter Guide

## Goal

Demonstrate one continuous SOC workflow:

1. An analyst handles a campaign efficiently with bulk triage.
2. Closed Cases become quality samples automatically.
3. An administrator uses field-level AI–Human Agreement to identify where AI recommendations need investigation.

Use **AI–Human Agreement**, **agreement rate**, and **mismatch** throughout the presentation. Do not call the metric AI accuracy or correctness.

## Before the session

1. Follow [Setup and reset](setup-and-reset.md).
2. Sign in as `demo.admin` using password `demopass`.
3. Set the Case table page size to 10.
4. Search for `[DEMO TRIAGE]` and confirm that 18 Cases appear.
5. Open **System Settings → AI Quality**, keep the default last-30-days range, and confirm that seven Closed Cases are represented.
6. Reset and reseed after any rehearsal so statuses and evaluation samples begin from the documented state.

## Part 1: Campaign triage

### A. Explain the starting queue

On the main **Cases** page, search for `[DEMO TRIAGE]`.

Point out that the campaign intentionally contains a mix of:

- New Cases.
- In Progress Cases.
- On Hold Cases.
- Different current assignees.
- AI recommendations already available for comparison after closure.

Suggested narration:

> These signals belong to the same identity campaign. Instead of opening and editing each Case, the analyst can explicitly select the Cases they have reviewed and apply the same structured decision.

### B. Demonstrate cross-page selection

1. Select three Cases on page 1.
2. Move to page 2 and select two more.
3. Confirm that the toolbar shows five selected Cases.
4. Explain that selection is explicit and limited to 100 Cases; it does not apply to every filtered result.
5. Do not change the search or filters yet, because doing so intentionally clears the selection.

### C. Apply a combined triage update

Open **Bulk Triage** and enable only:

| Field | Value |
| --- | --- |
| Assignee | `demo.alice` |
| Status | `In Progress` |
| Severity | `High` |
| Verdict | `Suspicious` |
| Reason | `Identity campaign reviewed during demo` |

Before submitting, point out the enabled-field preview. Fields whose edit toggle is off must remain unchanged.

After submitting, show:

- The success/failure summary.
- Successful Cases removed from the selection.
- Failed Cases, if any, retained for correction.
- Refreshed values in the Case list.
- One aggregated assignment notification for `demo.alice`, rather than one notification per Case.

Suggested narration:

> Each Case is committed independently. One bad transition cannot roll back valid analyst work, and every successful update shares an operation ID for traceability.

### D. Demonstrate partial success deliberately

Reset the search to `[DEMO TRIAGE]`. Select one **New** Case and one **In Progress** Case. Set only **Status → Resolved** and submit.

Expected result:

- New → Resolved fails with `invalid_transition`.
- In Progress → Resolved succeeds.
- The failed New Case remains selected.

Explain that request-structure errors reject the entire request, while Case-specific state errors produce safe per-Case failures.

### E. Demonstrate bulk closure

Select two In Progress or Resolved demo Cases. In **Bulk Triage**, enable:

| Field | Value |
| --- | --- |
| Status | `Closed` |
| Verdict | `False Positive` |
| Reason | `Confirmed approved VPN activity after campaign review.` |

Point out that selecting Closed makes the disposition reason required. Submit, then open one successful Case.

Verify:

- `closed_time` is populated.
- Verdict is False Positive.
- Summary contains a **Bulk disposition** Markdown section with UTC time, actor, and reason.
- Audit contains one `updated` entry with `source=bulk_triage`, the shared operation ID, actual field changes, and reason.

If time permits, reopen that Case by changing Closed → In Progress. Verify that `closed_time` and verdict are cleared while the acknowledgement time, Summary, and audit history remain.

## Part 2: Per-Case AI–Human Agreement

Clear the Case search and search for `[DEMO QUALITY]`. Open **Approved VPN created impossible travel**, then select its **Investigation** tab.

At the top, use the five-row comparison to explain:

| Field | AI | Human | Expected interpretation |
| --- | --- | --- | --- |
| Verdict | Suspicious | False Positive | Mismatch |
| Severity | High | Medium | Overestimate, distance 1 |
| Impact | Medium | Low | Overestimate, distance 1 |
| Priority | High | Low | Overestimate, distance 2 |
| Confidence | High | High | Agreement |

Explain these rules:

- Each field is measured separately; there is no composite score.
- Verdict uses exact enum agreement and a full confusion matrix.
- Severity, impact, priority, and confidence also show ordinal direction and distance.
- `Unknown` is a real value and participates in agreement, but it has no ordinal distance.
- An empty AI or human value is **Not evaluable** and is excluded from that field's denominator.
- The reference prediction is the latest successful analysis completed no later than Case closure.

Next, briefly open:

- **Ransomware behavior confirmed** to show five-field agreement.
- **Executive phishing campaign** to show AI underestimation.
- **Inconclusive cloud process activity** to explain `Unknown`.
- **Closed without an AI prediction** to show `No prediction`.
- **Closed with an invalid AI prediction** to show `Invalid prediction`.

## Part 3: Global AI Quality

Open **System Settings → AI Quality** as `demo.admin`.

### A. Coverage

With the last-30-days filter, expect:

- Total Closed Cases: 7.
- Evaluated: 5.
- No prediction: 1.
- Invalid prediction: 1.
- Prediction Coverage: 5 / 7, approximately 71.4%.

Explain that both missing and invalid predictions remain in the coverage denominator, while invalid results are shown separately for diagnosis.

### B. Agreement and direction

Show the five field cards and their sample counts. Avoid presenting any field rate without its denominator.

Then show:

- The full Verdict confusion matrix.
- Mean absolute distance for ordinal fields.
- Match, overestimate, and underestimate counts.
- The agreement trend, noting that bucket size changes from daily to weekly to monthly as the selected range grows.

Suggested narration:

> This page tells us whether disagreement is concentrated in a particular judgment. Direction matters: persistent severity overestimation creates alert fatigue, while underestimation can hide risk.

### C. Filter and drill down

1. Filter Category to IAM to isolate the VPN mismatch.
2. Clear Category and filter Human severity to High.
3. Filter Coverage state to Invalid prediction.
4. Reset filters and choose **Severity mismatches only** in the sample table.
5. Open a Case from the drilldown.

Point out that filters use the closure-time snapshots for category and assignee. Later reassignment does not rewrite historical grouping unless the Closed Case evaluation is rebuilt by an allowed human-field correction.

Also explain what is intentionally absent:

- No model, provider, prompt, or profile filters.
- No analyst leaderboard.
- No pass/fail threshold.
- No combined quality score.
- No raw analysis payload or full investigation report in the sample API.

## Part 4: Lifecycle proof

Use a seeded Closed quality Case for this final sequence:

1. Record its current presence in the AI Quality sample table.
2. Reopen it as In Progress.
3. Refresh AI Quality and verify that its evaluation is gone; open Cases do not participate.
4. Set a valid human verdict and close the Case again with a disposition reason.
5. Refresh AI Quality and verify that a new current evaluation appears.
6. While the Case remains Closed, change one human comparison field and verify that the same current evaluation is rebuilt.

Explain that evaluation work runs after the Case transaction. A quality-build failure must never block closure, reopening, or analyst corrections; administrators can reconcile missing samples with:

```bash
cd backend
uv run python manage.py rebuild_ai_quality_evaluations
```

## Closing message

> Bulk triage improves analyst throughput without weakening Case-level validation or auditability. AI Quality then turns final structured decisions into explainable feedback: coverage first, agreement by field, direction and distance where meaningful, and direct access to the samples behind every metric.
