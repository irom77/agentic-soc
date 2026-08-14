# Demo Setup and Reset

Run lifecycle scripts from the repository root and Django commands from `backend`.

## 1. Configure the local services

Confirm `backend/.env` contains the development PostgreSQL connection used by the Docker Compose stack. For the standard local stack:

```dotenv
POSTGRES_DB=asp
POSTGRES_USER=postgres
POSTGRES_PASSWORD=asp-dev-postgres-password
POSTGRES_HOST=localhost
POSTGRES_PORT=15432
```

Do not commit `backend/.env`.

## 2. Start ASP

```bash
./start.sh
```

The script starts the development containers plus these processes:

- Backend at `http://127.0.0.1:8001`.
- Frontend at `http://localhost:5173`.
- Agentic Case analysis worker.

Logs and PID files are stored in `.asp-runtime/`. Use `./restart.sh` after changing backend environment variables or provider-related configuration.

## 3. Confirm migrations

The demo changes do not add or alter database tables. Confirm the existing migrations are applied:

```bash
cd backend
uv run python manage.py migrate
uv run python manage.py showmigrations cases agentic settings
```

## 4. Configure an LLM provider for the live module

This step is required only for a real investigation run. Seeded Investigation reports work without provider credentials.

1. Browse to `http://localhost:5173`.
2. Choose **Platform** login.
3. Sign in as `demo.admin` / `demopass` after completing the seed step below, or use an existing administrator first.
4. Open **System Settings → LLM Providers**.
5. Add or edit an OpenAI-compatible provider.
6. Supply Name, Base URL, Model, and API Key as required by that provider.
7. Add the `structured_output` tag. This tag is required by Case investigation provider selection.
8. Set Enabled on and assign the desired priority. Lower-priority-number enabled providers are considered first.
9. Click **Test**, then save. Do not proceed with the live demo until the test succeeds.

## 5. Seed the dataset

For deterministic Cases only:

```bash
uv run python manage.py seed_case_triage_demo
```

Expected count: 25 Cases.

For the complete demo including one real LLM investigation:

```bash
uv run python manage.py seed_case_triage_demo --include-live-llm
```

Expected count: 26 Cases. The additional `[DEMO LIVE LLM]` Case is created with a pending `CaseAnalysisJob`. The seed code does not call the model directly; the running worker claims the job and calls the configured provider.

Both forms replace the previous scoped dataset. To leave an existing dataset unchanged:

```bash
uv run python manage.py seed_case_triage_demo --no-reset
```

Do not combine `--no-reset` with `--include-live-llm` when the dataset already exists: no new Case will be added.

## 6. Verify the seed and worker

```bash
uv run python manage.py shell -c "from apps.cases.models import Case; q=Case.objects.filter(correlation_uid__startswith='DEMO-CASE-TRIAGE-'); print('total=', q.count(), 'closed=', q.filter(status='Closed').count())"
```

Expected results are `total=25 closed=7`, or `total=26 closed=7` with the live option.

For the live job:

```bash
uv run python manage.py shell -c "from apps.agentic.models import CaseAnalysisJob; j=CaseAnalysisJob.objects.filter(trigger='demo_live_llm').latest('created_at'); print(j.status, j.error)"
```

The normal progression is Pending → Running → Success. Refresh after a few seconds if it is still Pending or Running.

## 7. Reset safely

Preview the deletion scope:

```bash
uv run python manage.py reset_case_triage_demo
```

Delete only the scoped demo Cases and their related analysis jobs:

```bash
uv run python manage.py reset_case_triage_demo --confirm
```

The reset matches `correlation_uid` values beginning with `DEMO-CASE-TRIAGE-`. It keeps the three demo users.

## Troubleshooting

### The first command cannot find `manage.py`

Run Django commands inside `backend`:

```bash
cd /home/irom/PythonProjects/agentic-soc-platform/backend
```

### PostgreSQL reports “no password supplied”

Check `backend/.env`, confirm port `15432` for the standard development container, and run `../restart.sh`.

### Login fails

Rerun the seed command to refresh the demo users and passwords. Select **Platform**, not LDAP, on the login page.

### The live Case remains Pending

Confirm the worker is running and inspect its log:

```bash
kill -0 "$(cat ../.asp-runtime/case-analysis-worker.pid)"
tail -n 100 ../.asp-runtime/case-analysis-worker.log
```

If necessary, process one queued job in the foreground:

```bash
uv run python manage.py run_agentic_case_analysis_worker --once
```

### The live Case fails

Read the saved job error and the worker log. Common causes are a missing enabled provider, a missing `structured_output` tag, an invalid API key/base URL/model, or a provider that cannot produce the required structured response. Fix the provider, test it in System Settings, and reseed with `--include-live-llm`; failed jobs are not retried automatically.

### Bulk Triage or AI Quality is missing

That is expected on this branch. Neither UI is implemented. The detailed guide labels those sections as planned and uses the current Case and Investigation features for the runnable demo.

### Restore the rehearsal state

Rerun the desired seed command. It replaces only the scoped demo dataset and recreates its relative timestamps and initial values.
