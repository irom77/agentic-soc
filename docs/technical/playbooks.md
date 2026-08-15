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

### How the built-in code works

#### Investigation

`backend/playbooks/investigation.py` is deliberately thin. Its `run()` method validates that the run has a Case, writes progress messages, and delegates the actual work to `run_case_analysis()`:

```python
result = run_case_analysis(
    case=self.case,
    trigger="playbook",
    user_input=self.user_input,
    source=self.playbook_run,
)
return f"Investigation completed: {result.report.digest}"
```

The analysis service serializes the Case and its evidence, retrieves relevant Knowledge, calls the structured-output LLM, and persists the report on the Case. Passing `source=self.playbook_run` links the generated analysis to the Playbook run. The returned string becomes the run's final `remark`; the messages added with `add_run_message()` are stored separately as ordered progress records.

#### Knowledge Extraction

`backend/playbooks/knowledge_extraction.py` delegates to `extract_knowledge_from_case()` and returns that service's remark. The service locks the Case and requires an analyst verdict. If no verdict exists, it succeeds with a “skipping knowledge extraction” remark without calling the LLM. Otherwise it sends the serialized Case and optional `user_input` to the structured-output LLM.

The model result drives one of three database outcomes:

- Create Case-sourced Knowledge when reusable knowledge is found and none exists.
- Update the existing Case-sourced Knowledge when one already exists.
- Delete the existing extracted Knowledge when the model says the Case no longer contains reusable knowledge.

The service validates that a positive result contains both a title and body, normalizes its tags, and saves all changes in one transaction.

#### Threat Intelligence Enrichment

`backend/playbooks/threat_intelligence_enrichment.py` demonstrates a provider-backed Playbook. It collects Artifacts from every Alert on the Case and de-duplicates them by database ID. For each non-empty value it calls:

```python
output = query_indicator(artifact.value, artifact_type=artifact.type)
```

Each successful provider result is persisted as an Artifact-level `THREAT_INTELLIGENCE` Enrichment. `_upsert_artifact_enrichment()` uses a stable UID, `ti:{provider}:{artifact_id}`, and a transaction plus `select_for_update()` so rerunning the Playbook updates the same provider/Artifact result instead of intentionally creating duplicates. Provider errors and unsupported indicators are counted rather than aborting the entire Case. The final remark reports Alert, Artifact, unique, enriched, unsupported, and error counts.

## Custom Playbooks

Repository-supplied custom definitions are stored in `backend/custom/playbooks/`.

| Definition | File | Behavior | Requirements |
| --- | --- | --- | --- |
| Case Summary | `case_summary.py` | Uses an LLM to generate and save a concise analyst-facing Case summary. | An enabled default LLM provider and the custom Case Summary prompt files. |
| CMDB Enrichment | `cmdb_enrichment.py` | Looks up CMDB context for unique Case Artifacts and saves Enrichment records. | A configured CMDB integration and supported Artifact values. |

The `official` and `custom` labels describe the definition's source directory. They do not change how a definition is submitted or executed.

### How the custom code works

#### Case Summary

`backend/custom/playbooks/case_summary.py` is the prompt-driven example. It serializes the linked Case with the same investigation profile used elsewhere, adds the optional analyst input, and invokes the default configured LLM at temperature `0.0`:

```python
payload = {
    "case": serialize_case_for_investigation(self.case),
    "user_input": self.user_input,
}
result = LLMAPI(temperature=0.0).get_model().invoke(
    [
        SystemMessage(content=self.read_prompt("System")),
        HumanMessage(content=json.dumps(payload, ensure_ascii=False)),
    ]
)
```

`PROMPT_SLUG = "case_summary"` makes `read_prompt("System")` load `backend/custom/data/playbooks/case_summary/System_<language>.md`. Prompt language comes from the runtime setting and falls back to `System_en.md` when the selected language file is absent. After rejecting an empty model response, the Playbook locks the Case and updates `Case.summary` transactionally. Its return value becomes the final run remark.

#### CMDB Enrichment

`backend/custom/playbooks/cmdb_enrichment.py` follows the same collect, de-duplicate, query, and upsert shape as the built-in threat-intelligence Playbook. It calls `lookup_artifact_context(artifact.type, artifact.value)` and skips results whose `supported` flag is false. Successful results become `CMDB` Enrichments with a stable UID, `cmdb:{provider}:{artifact_id}`, normalized provider data, and a short business-context description. Query and persistence failures are counted in the final remark so one failed Artifact does not discard successful results for the others.

## How to create a new Playbook

Put local Playbooks in `backend/custom/playbooks/`. A new file is discovered dynamically; there is no registry to edit and no database migration is required.

For example, create `backend/custom/playbooks/case_evidence_count.py`:

```python
from apps.agentic.runtime.base import BasePlaybook


class Playbook(BasePlaybook):
    NAME = "Case Evidence Count"
    DESC = "Count Alerts and unique Artifacts linked to a Case."
    TAGS = ["Custom", "Case"]
    RISK_LEVEL = "Low"

    def run(self):
        if self.case is None:
            raise ValueError("Case Evidence Count playbook requires a linked case.")

        self.add_run_message("Collecting Case evidence.")
        alert_count = self.case.alerts.count()
        artifact_count = (
            self.case.alerts.values("artifacts__id")
            .exclude(artifacts__id=None)
            .distinct()
            .count()
        )
        return f"Case evidence counted: alerts={alert_count}, unique_artifacts={artifact_count}"
```

The required contract is small:

1. Use a top-level `.py` file and absolute imports. Relative imports such as `from .helpers import ...` are rejected by the loader.
2. Define a top-level class named exactly `Playbook` that inherits `BasePlaybook`.
3. Implement `run(self)`. An uncaught exception fails the run; the returned value is converted to text and saved as the success remark.
4. Set `NAME` to the stable name users select. `DESC`, `TAGS`, and `RISK_LEVEL` supply definition metadata. Valid risk levels are `Low`, `Medium`, `High`, and `Critical`.
5. Use `self.case`, `self.user_input`, and `self.playbook_run` for the execution context. Use `self.add_run_message(text)` for progress that should appear while the run is Running.

Keep `NAME` unique across all definitions. The queued row stores this name, and the Worker looks the class up by name when it executes. Renaming or removing a definition while one of its runs is Pending makes that run fail when the Worker can no longer resolve it.

### Add prompts to a custom Playbook

Set `PROMPT_SLUG` and place language-specific Markdown prompts under the matching custom data directory:

```text
backend/custom/playbooks/my_playbook.py
backend/custom/data/playbooks/my_playbook/System_en.md
backend/custom/data/playbooks/my_playbook/System_zh.md
```

Then load a prompt inside `run()` with `self.read_prompt("System")`. When `PROMPT_SLUG` is omitted, the loader uses the Python filename stem. Explicitly setting it is useful when a file is renamed or several scripts share a prompt directory.

### Read custom configuration

Use `self.get_variable("key")` to read the value of an enabled Custom Variable from the database. It returns the stored JSON value, or `None` when the key is missing or disabled. This is appropriate for local endpoints and other Playbook configuration; do not include secrets in progress messages or return remarks.

### Verify and run the new definition

After saving the file:

1. Open **Custom → Playbooks** as an administrator and confirm the definition is listed without a scan error, or request `GET /api/playbooks/definitions/`.
2. Open a Case, choose **Run Playbook**, select the new `NAME`, and submit it with optional user input.
3. Ensure the Playbook Worker is running and watch the run move from Pending to Running and then Success or Failed.

The CLI exposes the same workflow through the agent API:

```bash
asp playbook template list
asp playbook run "Case Evidence Count" case_000001 --user-input "Optional analyst guidance"
```

Restarting the web application is normally unnecessary because discovery imports the files on each definition scan. A long-running Worker also resolves the current file immediately before each execution.

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
