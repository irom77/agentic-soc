# AI Quality Evaluation

Status: Confirmed

## 1. Purpose

Compare the final structured human judgment on a Closed Case with the last valid AI analysis result before closure, and produce an explainable AI–Human Agreement metric.

This feature does not claim that human labels are absolute truth, so product wording should not use Accuracy/Correctness. It does not evaluate report text quality, and it does not automatically optimize prompts.

## 2. Evaluated fields

Compare the following fields one by one:

- Verdict ↔ `verdict_ai`.
- Severity ↔ `severity_ai`.
- Impact ↔ `impact_ai`.
- Priority ↔ `priority_ai`.
- Confidence ↔ `confidence_ai`.

Do not collapse them into a single overall score.

## 3. Reference prediction

Each Case can have at most one primary quality sample, using:

1. A `CaseAnalysisJob` with `status=Success`.
2. `completed_at` no later than the current `closed_time`.
3. The Job originally ran for this target Case.
4. The last Job that satisfies the conditions above.

Reuse `CaseAnalysisJob.result_json`; do not create a separate Prediction table.

## 4. Metadata exclusion

AI Quality does not add, use, or display:

- Provider.
- Model.
- Prompt ID/content/hash/language.
- Profile version.
- Trigger.
- base URL.
- Input payload.

Even if `CaseAnalysisJob`/`AnalysisRecord` already has some of these fields, the global quality page does not filter by them. The accepted limitation is that model or prompt version quality cannot be compared.

## 5. Evaluation trigger and lifecycle

### Create

When a Case enters Closed, create the current Evaluation and snapshot:

- Reference Job.
- The five AI values.
- The five human values.
- Case category.
- Assignee.
- `closed_time`.
- `evaluated_at`.

### Closed field correction

If a Case remains Closed and any human comparison field changes, resubmit the Case and rebuild the same Evaluation. The category and assignee snapshot are refreshed during rebuild as well.

### Reopen

When a Case is Reopened, delete the current Evaluation. Open Cases do not participate in quality statistics. When the Case is Closed again, create a new Evaluation and do not retain the first closure’s quality version.

### Delete

Evaluation does not provide its own mutation API and is cascaded when the Case is deleted. The reference `CaseAnalysisJob` cannot be deleted independently.

### Failure isolation

Evaluation build failures must not prevent Case Close, Reopen, or human field edits:

- The Case transaction succeeds first.
- Rebuild happens after commit.
- Failures are written to safe logs.
- Provide a `rebuild_ai_quality_evaluations` management command for backfill and repair.
- Do not add a dedicated Worker.

The implementation must not return a “successful response with a failure shape.” The Case API may succeed, but logs and later reconciliation must detect missing Evaluations.

## 6. Coverage states

Each Closed Case Evaluation has one of the following states:

- Evaluated: there is an eligible Job and `result_json` can be parsed.
- No prediction: there is no eligible Job.
- Invalid prediction: the eligible successful Job’s `result_json` cannot be parsed into the required structure.

Prediction Coverage:

```text
Evaluated Cases / all filtered Closed Cases
```

No prediction and Invalid prediction both count in the denominator and not in the numerator. The page shows Invalid count separately.

A Case can still be Evaluated even if one AI field is empty; that field is marked separately as Not evaluable.

## 7. Missing values

A field only enters the agreement denominator when both the AI and human values exist.

- AI empty: Not evaluable.
- Human empty: Not evaluable.
- Both empty: Not evaluable.
- Unknown is an explicit valid value and is not treated as empty.

Closing does not require all five human fields to be filled. The existing Verdict close constraint remains in place.

## 8. Comparison semantics

### Verdict

- Use the full `CaseVerdict` enum.
- Exact agreement.
- Full confusion matrix.
- Do not collapse into binary or ternary classes.

### Ordinal fields

Severity, Impact, Priority, and Confidence:

- Exact agreement.
- Absolute ordinal distance.
- AI overestimate.
- AI underestimate.

The ordering uses the business order of the existing enums. Unknown:

- Participates in exact agreement.
- Appears in confusion counts.
- If either side is Unknown, do not compute distance/direction.

### Naming

All UI/API wording must use:

- AI–Human Agreement.
- Agreement rate.
- Mismatch.
- Overestimate/Underestimate.

Do not use AI Accuracy, Correctness, or analyst accuracy.

## 9. Data model

Each Case has one OneToOne `AiQualityEvaluation` with explicit fields instead of JSON.

Suggested fields:

- `case` OneToOne.
- `reference_job` nullable FK.
- `coverage_state`.
- `ai_verdict` / `human_verdict` / `verdict_agrees`.
- `ai_severity` / `human_severity` / `severity_agrees` / `severity_distance` / `severity_direction`.
- `ai_impact` / `human_impact` / `impact_agrees` / `impact_distance` / `impact_direction`.
- `ai_priority` / `human_priority` / `priority_agrees` / `priority_distance` / `priority_direction`.
- `ai_confidence` / `human_confidence` / `confidence_agrees` / `confidence_distance` / `confidence_direction`.
- `category_snapshot`.
- `assignee_snapshot` nullable FK.
- `closed_at`.
- `evaluated_at`.

Derived fields are stored as explicit nullable columns to support PostgreSQL aggregation and filtering; they are computed in one pass during rebuild.

Suggested indexes:

- `closed_at`.
- `coverage_state`.
- `category_snapshot`.
- `assignee_snapshot`.
- `human_severity`.
- Combination indexes for the `agrees` fields as needed by actual query plans.

## 10. Case relationships

- Case Relationships do not change Evaluation creation, selection, or aggregation.
- Each Case uses only its own eligible Job and human fields.
- Formal relationships and Artifact suggestions are not included in AI Quality query conditions.

## 11. Historical backfill

Backfill via a management command during or after upgrade:

- Current Closed Cases.
- Current human fields.
- The last eligible successful Job before `closed_time`.
- Create No prediction when there is no Job.
- Create Invalid prediction when parsing fails.
- Do not call the LLM.
- Do not create notifications or Evaluation AuditLog entries.

## 12. Permissions

| Surface | Admin | User | Viewer |
| --- | --- | --- | --- |
| Current Case comparison | Yes | Yes | Yes |
| Global summary | Yes | No | No |
| Global samples | Yes | No | No |
| Mutation | No | No | No |

Assignee may be used for Admin filtering, but there is no analyst leaderboard, best/worst ranking, or performance score.

## 13. Global analytics

Location: `System Settings → AI Quality`.

Default range is the last 30 days, and the time dimension is `Case.closed_time`.

Filters:

- closed time range.
- category snapshot.
- human severity.
- assignee snapshot.
- coverage state.

Do not filter by model/provider/prompt/profile/trigger.

### Required metrics

- Prediction Coverage and total count.
- Evaluated/No prediction/Invalid counts.
- Five-field exact agreement rate + sample count.
- Verdict confusion matrix.
- Mean absolute distance for the four ordinal fields.
- Over/under/match counts for the four ordinal fields.
- Agreement trend for the five fields.

Do not provide:

- composite score.
- pass/fail threshold.
- red/yellow/green target.
- severity-weighted score.
- analyst leaderboard.

### Trends

- ≤31 days: daily.
- 32–180 days: weekly.
- >180 days: monthly.
- Each point includes a sample count.
- Empty buckets are not returned and are not shown as 0%.

## 14. Sample drilldown

Admin-only paginated table:

- Case ID/title link.
- `closed_at`.
- assignee snapshot.
- category/human severity.
- coverage state.
- the five AI/human value pairs.
- agreement/direction/distance.

Filters:

- mismatch field.
- only mismatches.
- global filters.

The table does not return the full Investigation Report, analysis input, knowledge context, or raw Job JSON.

## 15. Case UI

Add a five-row comparison table to the top of the existing Investigation tab:

- Field.
- AI value.
- Human value.
- Agreement.
- Direction/distance, where applicable.

Show:

- No prediction.
- Invalid prediction.
- Not evaluable.

Do not add a separate Case Quality tab. The full report continues to use the existing Investigation view.

## 16. API

### Global summary

`GET /api/ai-quality/summary/`

- Admin only.
- Accepts the confirmed filters.
- Returns coverage, agreement, matrix, ordinal stats, and trend.
- Uses live PostgreSQL aggregation.

### Samples

`GET /api/ai-quality/evaluations/`

- Admin only.
- Cursor/page pagination.
- Returns a safe structured snapshot.

### Case surface

The Case Investigation or Case detail read-only fields return the current Evaluation. User/Viewer can read it.

There is no create/update/delete API and no CSV/JSON export.

## 17. Aggregation

- Live PostgreSQL queries.
- Default 30 days.
- The medium baseline is at most about 10,000 Evaluations, so no cache, Worker, or materialized daily table is added.
- `closed_at` and the filter dimensions must have appropriate indexes.
- The API must return sample counts to avoid misreading small samples.

## 18. Audit

- Evaluation create/rebuild/delete does not write AuditLog.
- Admin viewing summary/sample does not write AuditLog.
- Case Close/Reopen/human field edits continue to use the existing Case audit.
- `reference_job` and `evaluated_at` are for technical traceability.

## 19. Acceptance criteria

1. The five fields are compared correctly and are not collapsed into a single score.
2. The latest eligible pre-close Job is selected correctly.
3. Case Relationships do not change the reference Job selection.
4. Unknown and empty semantics are correct.
5. Verdict matrix and ordinal direction/distance are correct.
6. Close creates, Closed edit rebuilds, Reopen deletes, and re-close rebuilds.
7. Evaluation failures do not block Case business operations and can be repaired by a management command.
8. Historical Closed Cases are backfilled correctly and do not call the LLM.
9. Related Cases still enter their own eligible statistical samples separately.
10. Coverage denominator/numerator and Invalid count are correct.
11. The global page is Admin-only, while all roles can see the single-Case view.
12. Filtering uses the Evaluation snapshot and `closed_time`.
13. Adaptive trends and sample counts are correct.
14. The API does not expose report/input/provider/model/prompt metadata.
15. Live aggregation on the medium dataset meets the final acceptance threshold.

## 20. Known tradeoffs

- Without model/prompt metadata, version-driven trend changes cannot be explained.
- Human fields are reference labels, not absolute ground truth.
- Rebuilding after Close replaces the old quality result instead of preserving a closure version.
- Evaluation failures are isolated from Case closure, so statistics may temporarily miss samples until reconciliation runs.
- There is no report-text quality feedback, export, thresholding, or automatic learning.
