# SLA Management

Status: Confirmed

## 1. Purpose

Create Severity-based TTD, TTA, and TTR deadlines for Cases created after upgrade, warn owners about impending and overdue work, and provide compliance statistics in Case and Dashboard views that are fully consistent with the existing average-time metrics.

## 2. Terminology and formulas

A single Case uses names without the Mean prefix:

| Per-Case | Formula | Dashboard aggregate |
| --- | --- | --- |
| TTD, Time to Detect | earliest valid Alert.first_seen_time → Case.created_at | MTTD |
| TTA, Time to Acknowledge | Case.created_at → Case.acknowledged_time | MTTA |
| TTR, Time to Resolve | Case.acknowledged_time → Case.closed_time | MTTR |

Rules:

- `M` only means Mean across multiple samples.
- The Dashboard’s existing MTTD/MTTA/MTTR formulas must match the table above.
- `created_at → closed_time` may be shown as total elapsed time, but there is no separate SLA target for it.
- Use 24×7 elapsed seconds only; do not use working hours, holidays, or paused clocks.

## 3. Policy

One global policy row per `CaseSeverity`:

| Severity | TTD | TTA | TTR |
| --- | ---: | ---: | ---: |
| Critical | 300s | 900s | 14,400s |
| High | 900s | 1,800s | 28,800s |
| Medium | 1,800s | 7,200s | 86,400s |
| Low | 7,200s | 28,800s | 259,200s |
| Informational | 28,800s | 86,400s | 604,800s |
| Unknown | 3,600s | 14,400s | 172,800s |

- SLA is always enabled in v0.6.0.
- All six rows and all three targets are required.
- Each target is an integer number of seconds, ranging from 60 seconds to 365 days.
- TTD ≤ TTA ≤ TTR is not required because the three targets cover different phases.
- No per-Category, per-Tag, per-Assignee, or per-business-group configuration.

### Policy model

Suggested `SlaPolicy`:

- `severity`, unique.
- `ttd_target_seconds`.
- `tta_target_seconds`.
- `ttr_target_seconds`.
- `created_at`/`updated_at`.

The Settings API submits all six rows together and saves them in a single transaction. Any invalid value rejects the entire request.

## 4. Snapshot semantics

At the start of each phase, snapshot the current Severity and target:

- TTD: when the Case is created.
- TTA: when the Case is created.
- TTR: when `acknowledged_time` is first set.

Changing the Case Severity later does not affect phases that have already started or completed.

Policy changes only affect future phase snapshots:

- New Cases use the new policy for TTD/TTA.
- Existing Cases that have not yet been acknowledged will use the new policy when their TTR starts in the future.
- Do not batch-recompute existing snapshots.

## 5. CaseSla model

Each Case that participates in SLA has one OneToOne `CaseSla`; do not use JSON or a generic metric child table.

Persist each metric explicitly:

- `severity_snapshot`.
- `target_seconds`.
- `started_at`.
- `ended_at`.
- `deadline_at`.
- `elapsed_seconds`.

Additional fields:

- `case` OneToOne.
- `created_at`/`updated_at`.

Suggested indexes:

- `tta_deadline_at`, paired with `acknowledged_time`/null or an equivalent active marker.
- `ttr_deadline_at`, paired with `closed_time`/null.
- unique `CaseSla.case`.

State is not written to the database periodically; it is computed dynamically from the snapshot, current time, and completion time.

## 6. Metric states

Shared states:

- Pending.
- Warning.
- Met.
- Breached.
- Not applicable.

Incomplete metrics:

- elapsed < 80% of target: Pending.
- 80% ≤ elapsed < 100%: Warning.
- elapsed ≥ target: Breached.

Completed metrics:

- elapsed ≤ target: Met.
- elapsed > target: Breached.
- If completion happens late, the state remains Breached; there is no separate Completed late state.

### TTD subset

TTD is already complete when observed, so it can only be:

- Met.
- Breached.
- Not applicable.

TTD never enters Pending or Warning.

### TTR before acknowledgement

Before acknowledgement:

- UI state shows Pending.
- `started_at`/`deadline_at`/`elapsed_seconds` are empty.
- Show the label `Starts after acknowledgement`.
- The SLA Worker does not scan for Warning/Breach here.

Do not compute a single overall Case SLA state. TTD, TTA, and TTR are always displayed and filtered independently.

## 7. TTD behavior

### Valid source

Use the earliest valid `Alert.first_seen_time` under the current Case, with the following requirements:

- Non-empty.
- `first_seen_time <= Case.created_at`.

If there is no valid time:

- TTD = Not applicable.
- Do not include it in compliance-rate denominators.
- Do not fall back to `Alert.created_at`, `Case.created_at`, or zero seconds.

### Recalculation

Recompute TTD start, elapsed, and result when:

- An Alert is created and linked to a Case.
- `Alert.first_seen_time` changes.
- An Alert moves to a different Case.

The TTD target and Severity snapshot do not change. An earlier Alert may change the result from Met to Breached.

## 8. TTA behavior

- Starts immediately when the Case is created.
- `deadline = created_at + snapshotted target`.
- Ends when the Case leaves New for the first time and `acknowledged_time` is set.
- `acknowledged_time` is permanent; Reopen does not reset it.
- On Hold does not pause the clock.

## 9. TTR behavior

- Starts when `acknowledged_time` is first set and snapshots the current Severity/target.
- `deadline = acknowledged_time + target`.
- Ends when `closed_time` is set.
- On Hold does not pause the clock.
- Closed→In Progress Reopen clears `closed_time`, then resumes the same clock from the original `acknowledged_time`.
- When the Case is Closed again, the new `closed_time` is used as the current final result.
- The original close history is preserved only through AuditLog.

### Direct New→Closed

The state machine sets both `acknowledged_time` and `closed_time`:

- TTA = `created_at → transition timestamp`.
- TTR = 0 seconds, Met.

## 10. Upgrade boundary

- Only Cases created after the SLA migration/feature is enabled get a `CaseSla`.
- Existing v0.5.2 Cases are not backfilled, do not show SLA state, cannot be filtered, do not generate notifications, and are excluded from compliance rates.
- Old Cases continue to contribute to existing MTTD/MTTA/MTTR means as long as they satisfy the original query conditions.
- The Dashboard must show separate sample counts for mean and compliance because the sample sets differ.

## 11. Case relationships

- Case Relationships do not change any Case SLA.
- Related Cases do not share targets, Severity snapshots, clocks, states, or notifications.
- Artifact suggestions and formal relationships are not included in SLA query conditions.

## 12. Notifications

### Recipient

- Notify only the current Assignee.
- Do not notify unassigned Cases.
- Admin is not a fallback recipient.
- Users cannot turn off SLA notifications.

### Events

- TTA Warning.
- TTA Breached.
- TTR Warning.
- TTR Breached.
- TTD Breached.
- Do not send TTD Warning.
- Do not send Met, recovery, or completion notifications.

Warning and Breached are notified separately. Each recipient gets at most one of each per metric. When the Worker first sees an already-Breached state, it sends only Breached and does not backfill Warning.

### Reassignment

Deduplicate by `CaseSla + metric + state + recipient`. If the current state is already Warning/Breached and the Case is reassigned, the new Assignee receives one notification for the current state on the next scan; the old Assignee receives no cancellation message.

### Notification storage

`CaseSlaNotification`:

- `case_sla` FK.
- `metric` enum TTD/TTA/TTR.
- `state` enum Warning/Breached.
- `recipient` nullable FK User; use SET_NULL when the user is deleted.
- `sent_at`.
- unique(`case_sla`, `metric`, `state`, `recipient`); nullable-recipient history handling must not break real deduplication.

Notification records do not store message secrets or the full Case content.

## 13. SLA Worker

Add a single-instance `run_sla_worker`:

- Scans every 60 seconds.
- Integrates with Worker Health and becomes the 6th Worker.
- Only finds states that need notification and deduplicates sends.
- API state remains computed dynamically and does not depend on Worker-updated status.
- Uses deadline-index scans for applicable and incomplete TTA/TTR metrics.
- Uses unnotified queries for TTD Breached and reassignment cases.
- A failed notification must not be swallowed; it increments `WorkerIterationResult.failure_count` and marks the iteration Degraded.
- Do not send external webhooks or email.

## 14. API

Case list/detail adds nested SLA:

```json
{
  "sla": {
    "applicable": true,
    "ttd": {
      "state": "Met",
      "severity": "High",
      "target_seconds": 900,
      "elapsed_seconds": 420,
      "started_at": "...",
      "ended_at": "...",
      "deadline_at": "..."
    },
    "tta": {},
    "ttr": {
      "state": "Pending",
      "started": false
    }
  }
}
```

Old Cases:

```json
{"sla": {"applicable": false}}
```

The Case list supports per-item state filtering and deadline ordering. Do not compute everything in Python and paginate after the fact; the query must be filterable at the database layer.

Settings SLA API:

- Admin GET.
- Admin atomic PUT/PATCH for all six rows.
- User/Viewer 403.
- Seconds are the only API unit.

## 15. Frontend

### Case list

- Show TTA state by default.
- Show TTR state by default.
- Hide TTD by default, but allow it to be enabled.
- Filter each of the three independently.
- Support deadline sorting for TTA/TTR.
- Do not show an overall tag.

### Case detail

The SLA block shows each of:

- TTD/TTA/TTR.
- State.
- Target.
- Elapsed.
- Start/end/deadline.
- Severity snapshot.
- A TTR-not-started hint.

### Settings

`System Settings → SLA`:

- Six Severity rows.
- Three target columns.
- The UI uses minute/hour-friendly inputs and converts them to exact seconds on submit.
- One Save submits everything atomically.
- Admin only.

## 16. Dashboard

Keep the existing:

- MTTD mean/sample.
- MTTA mean/sample.
- MTTR mean/sample.

Add:

- TTD compliance rate/sample.
- TTA compliance rate/sample.
- TTR compliance rate/sample.
- Current TTA Warning count.
- Current TTA Breached count.
- Current TTR Warning count.
- Current TTR Breached count.

Sampling:

- TTD compliance: `Case.created_at` is within the window.
- TTA compliance: `acknowledged_time` is within the window.
- TTR compliance: `closed_time` is within the window.
- Current Warning/Breached: all active Cases with a `CaseSla`, regardless of creation window.

TTD has no current Warning/Breach count.

## 17. Audit

- SLA policy changes write AuditLog entries containing before/after seconds for all six rows and three targets.
- Pending/Warning/Breached/Met caused by elapsed time do not write Case AuditLog.
- SLA Worker scans do not write AuditLog.
- `CaseSlaNotification` provides send history.

## 18. Acceptance criteria

1. Per-Case TTD/TTA/TTR and Dashboard MTTD/MTTA/MTTR formulas match.
2. Default values and ranges for the six Severities are correct, and Admin can save them atomically.
3. Each phase uses the Severity snapshot from its own time; later edits are not back-propagated.
4. Missing TTD data is NA, and Alert changes can trigger recalculation.
5. TTA ends on first exit from New, TTR starts on acknowledgement.
6. On Hold does not pause, and Reopen continues from the original acknowledgement.
7. Direct close yields TTR=0 and Met.
8. 80% is Warning, 100% is Breached, and late completion remains Breached.
9. Old Cases have no SLA; new Cases do.
10. Case Relationships do not change any Case SLA or compliance rate.
11. The SLA Worker runs every minute and appears as the 6th Worker in Worker Health.
12. Only the current Assignee receives deduplicated Warning/Breached notifications.
13. A new Assignee can receive the current state, and unassigned Cases do not notify.
14. Case list/detail, Dashboard, and Settings behave according to the spec.
15. On the medium dataset, active deadline scans use indexes and do not require full-table Python computation.

## 19. Known tradeoffs

- Old Cases do not count toward compliance rates, so the initial sample set after upgrade is smaller.
- On Hold continues to count time and does not reflect net working time.
- Reopened Cases continue to extend the same TTR.
- Severity changes are not back-propagated, so different phases of one Case may use different policy versions.
- TTD may move from Met to Breached because of a late Alert.
- Unassigned Cases do not generate SLA notifications.
