# Playbook Execution

Status: Confirmed

## 1. Purpose

Keep the low-cognitive-load Python `run()` authoring model, while adding optional UI-visible run messages, explicit timing, crash recovery, and read-only run history.

This design is not a workflow engine and does not require developers to split or declare execution stages.

## 2. Authoring model

Playbooks continue to be defined in Python:

```python
class Playbook(BasePlaybook):
    NAME = "Contain Endpoint"
    DESC = "Contain the endpoint associated with the case."
    TAGS = ["EDR", "Response"]
    RISK_LEVEL = "High"

    def run(self):
        self.add_run_message("Collecting endpoint context.")
        endpoints = collect_endpoints(self.case)
        self.add_run_message(f"Collected {len(endpoints)} endpoint(s).")

        for endpoint in endpoints:
            contain(endpoint)

        self.add_run_message("Containment requests submitted.")
        return f"Contained {len(endpoints)} endpoint(s)."
```

Rules:

- `run()` remains the only execution entry point.
- `add_run_message(message)` is fully optional; existing v0.5.2 Playbooks do not need changes to run.
- A Run Message is only UI-visible text for the current Run; it does not store Python return values or execution context.
- The platform does not capture `print()` or Python `logging` output; server logs and UI-visible messages stay separate.
- An uncaught exception from `run()` makes the entire Run fail.
- Developers may catch tolerable errors and write safe notes through `add_run_message()`.
- Playbooks may call `httpx` or vendor SDKs directly; the platform does not provide a generic connector.

## 3. Explicit exclusions

- Visual/form-based orchestrator.
- DAGs, branches, and parallel steps.
- Mid-run human approval; clicking Run authorizes the entire Playbook.
- Pending or Running cancellation.
- Dedicated Retry, retry lineage, or single-step resume.
- Structured Stage or execution steps.
- Automatic capture of `print()` or Python `logging`.
- Source hashing or definition version locking.
- Structured input schema.
- HTTP/Webhook connection profiles.
- Automatic polling or WebSocket progress.

## 4. Definition metadata

Definition scanning continues to read:

- `NAME`
- `DESC`
- `TAGS`
- New `RISK_LEVEL`

Risk levels:

- Low
- Medium
- High
- Critical

Default is Low. Risk is for UI display only and does not change permissions, confirmation, or execution flow.

The definition selection screen shows the metadata found during the scan. The Run does not store a metadata snapshot; the history list and detail view only show the saved Run name and do not re-interpret the current definition.

Pending execution always loads the latest current Python code.

## 5. Run model

The existing `Playbook` record continues to represent the Run. The Python class may be renamed, but the database table does not need to change.

Add or adjust these fields:

| Field | Type | Semantics |
| --- | --- | --- |
| job_status | enum | Pending/Running/Success/Failed |
| job_id | string/UUID | Current execution identifier |
| started_at | nullable datetime | Claim success time |
| finished_at | nullable datetime | Terminal time |
| remark | text | Safe terminal summary |

Keep:

- case
- name
- user
- user_input
- created_at/updated_at

### Status transitions

| Current | Allowed next |
| --- | --- |
| Pending | Running |
| Running | Success, Failed |
| Success | none |
| Failed | none |

Do not allow direct modification of `job_status`. All status changes must go through a domain service.

### Timing

- When a Pending Run is created, `started_at` and `finished_at` are empty.
- Pending→Running sets `started_at`.
- Running→Success/Failed sets `finished_at`.
- `duration_seconds` is computed from `started_at` and `finished_at`; while Running, it uses `now - started_at`.

## 6. Run Message model

Suggested model: `PlaybookRunMessage`

| Field | Type | Notes |
| --- | --- | --- |
| id | UUID | primary key |
| playbook_run | FK | CASCADE at DB level, though the Run API cannot delete |
| sequence | positive bigint | append order within a Run |
| message | text | UI-visible safe message |
| created_at | datetime | append time |

Constraints/indexes:

- unique `(playbook_run, sequence)`.
- index `(playbook_run, sequence)`.
- `message` is length-limited.

### `add_run_message()` behavior

Calling `self.add_run_message(message)`:

1. Accepts only a non-empty string.
2. Applies sensitive-field filtering and length limits.
3. Atomically assigns the next sequence for the current Run.
4. Persists the message for display in Run detail UI in sequence order.

The method returns `None` and does not provide levels, structured fields, progress percentages, or message update capability. Developers should record a small number of meaningful execution events rather than emitting every loop iteration.

### Output safety

- Do not automatically `str()` or JSON-serialize arbitrary function output.
- Do not automatically save HTTP responses, LLM output, SIEM records, or variable values.
- Messages are explicitly provided by custom code and are treated as final user-visible content.
- Messages use a shared sanitizer that masks at least password/token/api_key/secret/authorization values.
- The API does not return tracebacks.

## 7. Queue and Worker behavior

### Supported topology

- One Playbook Worker is officially supported.
- Global FIFO, claimed by `created_at/id`.
- Do not sort by Case Severity or user priority.

### Duplicate launch

The Run endpoint does not provide idempotency. Repeated requests may create multiple Pending Runs, and that is accepted behavior.

### Worker loss

Playbook Worker uses Worker Health heartbeats. When the previous instance is detected as lost:

- Mark any orphaned Running Runs as Failed.
- Use a fixed safe remark stating that the Worker stopped before completion.
- Do not automatically reset Pending or rerun.
- After inspection, the user may start the Run again.

Implementation may perform orphan recovery after the Worker successfully acquires the singleton lease. Do not mark a legitimate long-running task as failed based only on runtime duration.

## 8. Launch

`POST /api/playbooks/run/`

- Admin/User can run; Viewer receives 403.
- Any Case can be run, including Closed Cases.
- Case Relationships do not affect run eligibility.
- `name` must exist in the current definition scan.
- `user_input` is optional free text.
- Clicking Run creates a Pending Run directly, with no extra confirmation.
- Risk level is display only.

## 9. API shape

The Playbook Run resource becomes read-only:

- GET list.
- GET retrieve.
- GET definitions.
- POST run.
- GET messages (detail action or a separate nested endpoint).

Forbidden:

- Normal POST create.
- PUT/PATCH.
- DELETE.

Run Message API:

- Read-only.
- Must paginate by sequence.
- Must not return an unlimited number of messages in one response.

### Run response additions

```json
{
  "id": "...",
  "playbook_id": "playbook_000123",
  "job_status": "Running",
  "started_at": "2026-07-30T08:00:00Z",
  "finished_at": null,
  "duration_seconds": 42
}
```

## 10. Remark semantics

| Terminal state | Remark |
| --- | --- |
| Success | `str(run() return value)`, after length limiting and safety filtering |
| Failed | Fixed safe summary |

Run Messages must not be concatenated into `remark`. Raw exceptions go only to server logs.

## 11. Notifications

Follow the initiating user’s existing `notify_on_playbook_completion` preference:

- Success notification.
- Failed notification.
- No notification for Run Messages.

## 12. Audit

Only record user actions:

- launch

Automatic Worker status changes are not written to the global AuditLog because the Run and Run Messages already represent the state facts.

Audit metadata must not include full `user_input`, Run Message text, or any secret.

## 13. Frontend

### Definition selection

- Show name, description, tags, and risk level.
- Clicking Run queues immediately.
- Keep free-text `user_input`.
