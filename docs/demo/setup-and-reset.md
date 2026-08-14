# Demo Setup and Reset

Run all commands from the repository's `backend` directory with the development environment configured.

## 1. Confirm migrations

The demo commands do not introduce database schema changes. Before seeding, confirm that the migrations already present on the branch are applied:

```bash
cd backend
uv run python manage.py migrate
uv run python manage.py showmigrations cases agentic
```

When AI Quality is implemented, its ORM migration must also be applied before running the seed command.

## 2. Seed or refresh the dataset

```bash
uv run python manage.py seed_case_triage_demo
```

The default behavior is repeatable: it deletes the previous scoped demo Cases and creates a fresh dataset with dates relative to the current time. It does not touch ordinary Cases.

Expected output includes:

```text
Seeded 25 demo Cases: 18 triage Cases and 7 closed AI quality Cases.
Demo users: demo.admin, demo.alice, demo.bob (password: demopass)
```

On a branch without AI Quality implementation, the command also reports that the source jobs and Case AI fields were seeded. On a completed branch, it runs `rebuild_ai_quality_evaluations` after committing the Cases.

To leave an existing demo dataset unchanged:

```bash
uv run python manage.py seed_case_triage_demo --no-reset
```

## 3. Verify the seed

```bash
uv run python manage.py shell -c "from apps.cases.models import Case; q=Case.objects.filter(correlation_uid__startswith='DEMO-CASE-TRIAGE-'); print(q.count(), q.filter(status='Closed').count())"
```

Expected result:

```text
25 7
```

Sign in as `demo.admin`, open **Cases**, and search for `[DEMO`. Both demo groups should be visible. Searching for `[DEMO TRIAGE]` should return 18 Cases, which is enough to demonstrate selection across pages when the table page size is 10.

## 4. Reset the dataset

Preview the reset scope by omitting confirmation:

```bash
uv run python manage.py reset_case_triage_demo
```

The command refuses to delete and prints the number of matching Cases. Perform the scoped deletion with:

```bash
uv run python manage.py reset_case_triage_demo --confirm
```

The reset removes only Cases whose `correlation_uid` begins with `DEMO-CASE-TRIAGE-`. It deliberately keeps the three demo users so references from other manually created records are not disturbed.

## Troubleshooting

### Bulk Triage or AI Quality is missing

Those surfaces are not implemented on the current branch. Confirm that the v0.6.0 feature branch includes:

- `POST /api/cases/bulk-triage/`.
- The `AiQualityEvaluation` model and migration.
- `rebuild_ai_quality_evaluations`.
- **System Settings → AI Quality**.
- The per-Case comparison at the top of **Investigation**.

Then apply migrations and rerun the seed command.

### The AI Quality page has no samples

Run the repair command after seeding:

```bash
uv run python manage.py rebuild_ai_quality_evaluations
```

Use a closed-time filter covering the last 30 days. All seven seeded quality Cases are inside that window.

### Demo Cases were changed during rehearsal

Run `seed_case_triage_demo` again. Its default behavior restores the complete deterministic scenario.
