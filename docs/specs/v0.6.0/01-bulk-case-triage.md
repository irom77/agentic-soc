# Bulk Case Triage

Status: Confirmed

## 1. Purpose

Allow analysts to explicitly select a group of Cases from the Case list and apply the same triage fields in one operation. This feature reduces repetitive manual work; it does not replace Case Relationships, suppression rules, AI analysis, or Playbooks.

## 2. Scope

### Included

- Bulk triage is supported for Cases only.
- Assignee, Status, Severity, and Verdict can be changed together in one request.
- Up to 100 explicit Case IDs.
- Supports cross-page selection.
- Executes synchronously and returns per-Case success or failure results.
- Partial success is allowed.

### Excluded

- Bulk triage for Alerts.
- Bulk changes to Priority or Tags.
- Applying the action to the entire current filter result set.
- Background bulk jobs.
- Server-side idempotency keys.
- updated_at optimistic locking.
- A batch-level AuditLog entity.

## 3. Permission matrix

| Action | Admin | User | Viewer |
| --- | --- | --- | --- |
| Select cases | Yes | Yes | No |
| Bulk update any case | Yes | Yes | No |
| Bulk assign to any valid user | Yes | Yes | No |
| Bulk close | Yes | Yes | No |

Permissions must be checked on the server. User is not restricted by assignee ownership.

## 4. Shared Case state machine

Single-Case PATCH and bulk triage must call the same domain service; state logic must not be maintained separately.

### Allowed transitions

| Current | Allowed next |
| --- | --- |
| New | In Progress, Closed |
| In Progress | On Hold, Resolved, Closed |
| On Hold | In Progress, Resolved, Closed |
| Resolved | In Progress, Closed |
| Closed | In Progress |

Writing the same state may be treated as a no-op and should not produce a state error.

### Transition side effects

- When a Case leaves `New` for the first time, set `acknowledged_time=now()`.
- Once set, `acknowledged_time` is permanent and is not reset by Reopen.
- When entering `Closed`, set `closed_time=now()`.
- Entering `Closed` requires a non-empty Verdict in the final state and requires this request to provide a disposition note.
- `Closed → In Progress` is Reopen:
  - Clear `closed_time`.
  - Clear `verdict`.
  - Keep Summary, `acknowledged_time`, and historical audit data.
- No other path out of Closed exists.

The state machine should be implemented as a reusable service, for example `apps.cases.services.transition_case()`, and both the serializer and the bulk endpoint must call it.

## 5. Editable field semantics

### Assignee

- Field omitted: leave unchanged.
- Valid user ID provided: set the new assignee.
- Explicit `null`: unassign.
- Do not allow a nonexistent or unavailable user.

### Status

- Field omitted: leave unchanged.
- Must be a `CaseStatus` enum value.
- Must satisfy the shared state machine.
- Status cannot be cleared or set to null.

### Severity

- Field omitted: leave unchanged.
- Must be a `CaseSeverity` enum value.
- Do not use an empty string to express clearing; use `Unknown`.

### Verdict

- Field omitted: leave unchanged.
- Must be a `CaseVerdict` enum value.
- A non-Closed Case may be explicitly set to null/empty to clear the Verdict.
- If the Case is Closed after the request, Verdict must be non-empty.
- Do not allow clearing the Verdict of a Closed Case only.

### Multi-field evaluation

Validation must be based on the final Case state after applying all fields from this request, not on JSON field order. For example, one request may set a New Case to Closed and provide a Verdict in the same payload.

## 6. Bulk close note

When entering Closed, `reason` is required. The text is used for both audit and Summary appending.

Summary append format:

```markdown

### Bulk disposition · 2026-07-28 10:44 UTC · alice

Confirmed as false positive after campaign review.
```

Rules:

- Preserve the existing Summary.
- Insert a blank line between the existing Summary and the new paragraph.
- The header timestamp uses a stable UTC format.
- `actor` uses the current username.
- Append the same note to every successfully closed Case.
- For ordinary assignee, Severity, Status, or Verdict changes, `reason` is optional; if provided, write it only to audit and do not append it to Summary.

## 7. API

### Endpoint

`POST /api/cases/bulk-triage/`

This is a Case-specific collection action; there is no generic bulk PATCH.

### Request

```json
{
  "case_ids": [
    "6387d62e-4ed6-45b4-b83a-522cd7b5e845",
    "b109ce5c-956a-42d5-b53c-bc883d19dbfc"
  ],
  "changes": {
    "assignee": "e0602519-1cd0-4750-80af-aac269a98722",
    "status": "In Progress",
    "severity": "High",
    "verdict": "Suspicious"
  },
  "reason": "Campaign triage"
}
```

Validation:

- `case_ids` must be a non-empty array.
- After deduplication, there must be at most 100 IDs.
- IDs must be valid UUIDs; an invalid UUID in the request structure is a request-level 400, while a valid UUID that does not exist fails per item.
- `changes` must contain at least one allowed field.
- Priority, Tags, and any other fields are rejected.
- `reason` is validated after trimming leading and trailing whitespace.
- If the request’s final target state is Closed, `reason` is required.

### Success and partial success response

If the request structure is valid, return HTTP 200:

```json
{
  "operation_id": "a143bc8b-df7b-40d8-b0ee-e5df4e7efdc4",
  "requested": 2,
  "succeeded_count": 1,
  "failed_count": 1,
  "succeeded": [
    {
      "id": "6387d62e-4ed6-45b4-b83a-522cd7b5e845",
      "case_id": "case_000123",
      "updated_at": "2026-07-28T02:44:00Z"
    }
  ],
  "failed": [
    {
      "id": "b109ce5c-956a-42d5-b53c-bc883d19dbfc",
      "case_id": "case_000124",
      "code": "invalid_transition",
      "detail": "Case cannot transition from New to Resolved."
    }
  ]
}
```

Allowed safe failure codes must include at least:

- `not_found`
- `permission_denied`
- `invalid_transition`
- `invalid_final_state`
- `invalid_assignee`
- `update_failed`

`detail` must not include tracebacks or database errors.

### Request-level errors

The following return 400 and do not process any Case:

- Empty `case_ids`.
- More than 100 IDs.
- Invalid UUIDs.
- Empty `changes`.
- Unknown fields.
- Invalid enum values.
- Target Closed but `reason` is missing.

Use the existing authentication and permission responses for 401/403.

## 8. Transaction and failure behavior

- The batch must not use one global atomic transaction.
- Each Case should be read, processed by the state machine, saved, and have AuditLog written in its own short transaction.
- Failure of one Case must not roll back already successful Cases.
- Use last-write-wins; do not compare the client’s observed `updated_at`.
- Read the latest Case inside the transaction and only overwrite fields explicitly included in the request.
- The frontend should disable the submit button while the request is in flight; the platform does not provide a server-side idempotency key.

## 9. Notifications

Only changes in the actual assignee generate assignment notifications.

- Group by the final assignee.
- Each recipient should receive at most one Inbox message per bulk request.
- The message includes the number of Cases successfully assigned to that user and a list of openable Case IDs.
- Failed Cases are not included in notifications.
- Unassigning does not send a notification.
- If the assignee does not change, do not send a notification.
- Notifications are generated after the corresponding Case transaction succeeds; notification failure must not make completed business updates look failed, and should instead be recorded according to the existing notification error policy.

## 10. Audit

Each successful Case writes one existing `updated` AuditLog entry:

```json
{
  "action": "updated",
  "changes": {
    "status": {"from": "New", "to": "In Progress"},
    "severity": {"from": "Medium", "to": "High"}
  },
  "metadata": {
    "source": "bulk_triage",
    "operation_id": "a143bc8b-df7b-40d8-b0ee-e5df4e7efdc4",
    "reason": "Campaign triage"
  }
}
```

- The backend generates one UUID `operation_id` per request.
- All successful Cases from the same request share the same `operation_id`.
- Do not create a separate batch AuditLog.
- A Case with no actual field changes may still be treated as success, but it must not write an empty `changes` audit entry; the response should include `unchanged: true`.
- Failed Cases do not write business-update audit records.

## 11. Frontend

### Selection

- Bulk triage is enabled only on the main Case list.
- Selection persists across pagination.
- Changing Search, normal Filter, or Advanced Filter clears the selection.
- “Select all filtered results” is not supported.
- Up to 100 items can be selected; once the limit is reached, other checkboxes become disabled and a limit message is shown.
- The toolbar always shows the selected count and a Clear selection action.

### Bulk triage modal

- The user clicks Bulk Triage to open the modal; nothing runs immediately.
- Each field has its own “edit this field” toggle; fields that are not enabled are not included in `changes`.
- Assignee supports selecting a user or Unassigned.
- Status, Severity, and Verdict use the existing options and Tag styling.
- `reason` is optional by default; after Closed is selected it becomes required immediately and the UI explains that it will be appended to Summary.
- Show the selected count, a field-change preview, and close side effects.
- Disable all actions while submitting.

### Result handling

- Successful items are removed from the selection.
- Failed items remain selected.
- Show a success/failure summary.
- The failure list shows Case ID and a user-readable explanation for the failure code.
- Do not auto-retry.
- Refresh the current list data, but do not clear failed selections because of the refresh.

## 12. Backend implementation surfaces

Expected touch points:

- `backend/apps/cases/services.py`: shared state machine and field application.
- `backend/apps/cases/serializers.py`: bulk request/response serializer.
- `backend/apps/cases/views.py`: collection action.
- `backend/apps/inbox/notifications.py`: aggregated assignment notification.
- `frontend/src/components/DataTable.tsx`: controlled cross-page selection and custom bulk action context.
- Case resource page: Bulk Triage modal and result presentation.

Do not put the Case business state machine into the generic DataTable.

## 13. Acceptance criteria

1. Admin/User can combine any of the four allowed fields across 1–100 Cases.
2. Viewer cannot see the action and the API returns 403.
3. Cross-page selection persists; filter changes clear it.
4. Invalid state transitions fail only the affected Case; the others succeed.
5. Closed requires a final Verdict and a reason.
6. Bulk close correctly appends Markdown Summary with time and actor.
7. Reopen clears `closed_time` and `verdict` while preserving `acknowledged_time` and Summary.
8. Assignment notifications are aggregated per user.
9. Every successful Case has `source`, `operation_id`, and `changes` in audit data.
10. Request-level errors do not update any Case.
11. On the medium dataset, a synchronous request for 100 items completes within the formal acceptance timeout.

## 14. Known tradeoffs

- Last-write-wins may overwrite concurrent edits; this is accepted behavior.
- There is no server-side idempotency, so client network retries may duplicate close notes; the frontend must avoid automatically retrying POST.
- Partial success means one `operation_id` does not imply total success; the response and per-Case audit records are the source of truth.
