# Playbooks

Playbooks are dynamically discovered Python workflows that run against a Case. A Playbook definition describes available behavior; a Playbook run is a PostgreSQL record representing one execution of that definition.

## Where Playbooks appear in the UI

The main **Playbooks** page displays Playbook run history. It remains empty until at least one Playbook has been submitted, so it is not a catalog of the definitions available on disk.

To view and run the available definitions:

1. Open a Case detail page.
2. Select the **Run Playbook** action in the Case header.
3. Choose a definition, optionally enter user input, and submit it.

The resulting Pending run then appears on the main **Playbooks** page and is processed by the Playbook Worker.

Administrators can also open **Custom → Playbooks** to inspect all discovered definitions. Despite the menu name, this view includes both built-in definitions, labeled `official`, and locally supplied definitions, labeled `custom`. Non-admin users do not see the **Custom** menu.

## Built-in Playbooks

Built-in definitions are stored in `backend/playbooks/`.

| Definition | File | Behavior | Requirements |
| --- | --- | --- | --- |
| Investigation | `investigation.py` | Runs the Case Analysis workflow, retrieves relevant Knowledge, and saves a structured AI investigation report. | An enabled LLM provider tagged `structured_output`. |
| Knowledge Extraction | `knowledge_extraction.py` | Uses the analyst verdict and Case evidence to create, update, or remove reusable Knowledge linked to the Case. | A Case with an analyst verdict and an enabled LLM provider tagged `structured_output`. |
| Threat Intelligence Enrichment | `threat_intelligence_enrichment.py` | Queries configured threat-intelligence providers for unique Case Artifacts and saves Enrichment records. | A configured threat-intelligence provider and supported Artifact values. |

## Custom Playbooks

Repository-supplied custom definitions are stored in `backend/custom/playbooks/`.

| Definition | File | Behavior | Requirements |
| --- | --- | --- | --- |
| Case Summary | `case_summary.py` | Uses an LLM to generate and save a concise analyst-facing Case summary. | An enabled default LLM provider and the custom Case Summary prompt files. |
| CMDB Enrichment | `cmdb_enrichment.py` | Looks up CMDB context for unique Case Artifacts and saves Enrichment records. | A configured CMDB integration and supported Artifact values. |

The `official` and `custom` labels describe the definition's source directory. They do not change how a definition is submitted or executed.

## Discovery and overrides

The scanner reads both directories on every definition listing or lookup:

1. `backend/playbooks/`
2. `backend/custom/playbooks/`

It considers top-level `.py` files other than `__init__.py`. A valid file must define a top-level `Playbook` class that inherits from `BasePlaybook`; relative imports are rejected.

Definitions can declare:

- `NAME`: UI and execution name; the filename stem is used when omitted.
- `DESC`: description shown in definition lists.
- `TAGS`: UI classification tags.
- `RISK_LEVEL`: `Low`, `Medium`, `High`, or `Critical`; the default is `Low`.
- `PROMPT_SLUG`: optional directory name for custom prompt files.

The two directories are overlaid by filename. If a custom file has the same filename as a built-in file, the custom file replaces that built-in file during discovery. Names must remain unambiguous because a run stores the selected `NAME` and the Worker resolves that name again at execution time.

## Submission and execution

The Case dialog requests definitions from `GET /api/playbooks/definitions/` and submits a run to `POST /api/playbooks/run/`. Submission validates the definition name and creates a Pending PostgreSQL row; it does not execute the Playbook in the web request.

The `run_agentic_playbook_worker` process then:

1. Claims the oldest Pending run and marks it Running.
2. Discovers the current definition by name.
3. Instantiates it with the run, linked Case, and optional user input.
4. Calls its `run()` method.
5. Marks the run Success or Failed and records timestamps and a sanitized remark.

Some definitions add ordered progress messages to the run. On Worker startup, orphaned Running rows are marked Failed so they do not remain stuck indefinitely.

Start the Worker in continuous mode with:

```bash
cd backend
uv run python manage.py run_agentic_playbook_worker
```

For a single polling iteration, add `--once`. One iteration claims at most one Pending run.

## Troubleshooting missing definitions

If a definition does not appear in the Case dialog or **Custom → Playbooks**:

1. Confirm the file is directly inside `backend/playbooks/` or `backend/custom/playbooks/` and ends in `.py`.
2. Confirm it defines a top-level `Playbook(BasePlaybook)` class and does not use relative imports.
3. Confirm `RISK_LEVEL` is one of the supported values.
4. As an administrator, open **Custom → Playbooks** and check the definition errors shown above the table.
5. Check backend logs for `Failed to load playbook definition` and the affected path.

If definitions are visible but submitted runs remain Pending, confirm that `run_agentic_playbook_worker` is running and inspect its heartbeat and log as described in [Workers and Agentic Runtime](workers-and-runtime.md).
