# Demo management command reference

## Location and syntax

Run all commands from `backend/`:

```bash
cd backend
uv run python manage.py COMMAND [OPTIONS]
```

`uv run` selects the locked project environment. `manage.py` initializes Django settings, apps, and ORM. Run `uv run python manage.py help COMMAND` for exact help from the checked-out code.

## Seed

```bash
uv run python manage.py seed_case_triage_demo [--no-reset] \
  [--include-live-llm] [--include-complex-live-llm] [--include-live-otx]
```

By default it removes scoped Cases whose correlation UID starts with `DEMO-CASE-TRIAGE-`, then creates 25 Cases without external calls (18 triage and 7 quality) plus three demo users.

| Option | Effect |
| --- | --- |
| `--no-reset` | Preserve the existing scoped dataset; do not combine with live options after those Cases exist because duplicates are not added |
| `--include-live-llm` | Add one text-only Case with no job/report |
| `--include-complex-live-llm` | Add one Case with Alerts, Artifacts, deterministic Enrichments, and no job/report |
| `--include-live-otx` | Add one Case awaiting a real OTX Playbook |

To include every optional Case:

```bash
uv run python manage.py seed_case_triage_demo \
  --include-live-llm --include-complex-live-llm --include-live-otx
```

Seeding writes normal ORM records. It does not queue OTX or LLM calls, and viewing the UI does not invoke them.

## Queue

These commands have no custom options; they accept the Django common options below.

| Command | Prerequisite | Work created |
| --- | --- | --- |
| `queue_live_llm_case_demo` | Seed with `--include-live-llm` | Pending analysis job for the text-only Case; reuses an existing Pending job |
| `queue_complex_llm_case_demo` | Seed with `--include-complex-live-llm` | Analysis job for the deterministically enriched Case |
| `queue_live_otx_enrichment_demo` | Seed with `--include-live-otx`; enable OTX | Pending Threat Intelligence Enrichment Playbook |
| `queue_live_otx_case_demo` | OTX Playbook succeeded and at least one OTX Enrichment exists | Analysis job using real enrichment; refuses otherwise |

Recommended OTX order:

```bash
uv run python manage.py queue_live_otx_enrichment_demo
# Wait for Playbook Success.
uv run python manage.py queue_live_otx_case_demo
```

## Shell

```bash
uv run python manage.py shell [--no-startup] [--no-imports] \
  [-i {ipython,bpython,python}] [-c COMMAND]
```

| Option | Purpose |
| --- | --- |
| `--no-startup` | Ignore `PYTHONSTARTUP` and `~/.pythonrc.py` with plain Python |
| `--no-imports` | Disable automatic model imports |
| `-i`, `--interface` | Force ipython, bpython, or python |
| `-c`, `--command` | Execute Python in Django context and exit |

Read-only examples:

```bash
uv run python manage.py shell -c "from apps.cases.models import Case; q=Case.objects.filter(correlation_uid__startswith='DEMO-CASE-TRIAGE-'); print(q.count())"
uv run python manage.py shell -c "from apps.agentic.models import CaseAnalysisJob; j=CaseAnalysisJob.objects.latest('created_at'); print(j.status, j.error)"
```

The shell has full application privileges. Writes bypass UI workflows; use them only when their transaction, signal, and cascade effects are understood.

## Enrich

The live demo enrichment entry point is `queue_live_otx_enrichment_demo`; there is no generic command named `enrich`. A continuous Playbook worker must then run, or process one Pending run manually:

```bash
uv run python manage.py run_agentic_playbook_worker --once
```

One iteration claims at most one Pending Playbook. Credentials, network access, and provider Artifact support determine the result. The complex LLM demo uses deterministic seeded enrichments and does not call a provider.

## Reset

```bash
uv run python manage.py reset_case_triage_demo [--confirm]
```

Without `--confirm`, it is a dry run that prints the scoped Case count. With `--confirm`, it deletes Cases whose correlation UID has the demo prefix. Database cascades remove dependent Alerts, direct and child Enrichments, Playbooks, relationships, and analysis jobs. Because shared Artifacts do not have a Case FK, do not assume that resetting Cases deletes every Artifact. The three demo users remain.

## Common Django options

Seed, Queue, Reset, and Worker commands inherit these options. `shell` does not support `--skip-checks`.

| Option | Meaning |
| --- | --- |
| `-h`, `--help` | Show help |
| `--version` | Show the Django version |
| `-v {0,1,2,3}`, `--verbosity` | Output verbosity |
| `--settings MODULE` | Override the settings module |
| `--pythonpath PATH` | Add a directory to Python's import path |
| `--traceback` | Show a full traceback for `CommandError` |
| `--no-color` / `--force-color` | Disable or force terminal color |
| `--skip-checks` | Skip Django system checks (not accepted by `shell`) |

See [Setup and reset](../demo/setup-and-reset.md) for the full demo workflow and troubleshooting.
