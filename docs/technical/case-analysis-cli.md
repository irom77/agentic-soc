# Case Analysis CLI walkthrough

`explain_case_analysis` is a read-only educational command that exposes the main steps performed by the Case Analysis Worker. It uses the production Case serializer, prompt files, Knowledge search, LLM configuration, LangChain adapter, and structured output schemas, but it does not queue a job or save an analysis.

## Preview without calling an LLM

Run the command from the backend directory with a readable Case ID:

```bash
cd backend
uv run python manage.py explain_case_analysis case_000001
```

A Case UUID can be used instead. Preview mode makes no LLM requests. Because there is no model-generated keyword response, it uses the worker's deterministic fallback keywords to demonstrate the remaining flow.

The command prints five stages:

1. The Case serialized with the Investigation profile.
2. The system and human messages for Knowledge keyword generation.
3. The fallback keywords and matching Knowledge records from PostgreSQL.
4. The system and human messages for the structured investigation.
5. Confirmation that nothing was written.

The output can contain Case evidence, comments, audit history, Alerts, Artifacts, and Enrichments. Treat captured terminal output as potentially sensitive.

## Invoke the configured LLM

Add `--invoke` to perform the same two structured LLM calls as the worker:

```bash
uv run python manage.py explain_case_analysis case_000001 --invoke
```

The first call asks for up to eight Knowledge search keywords. Django uses those terms to retrieve up to ten unexpired Knowledge records. The second call receives the serialized Case and Knowledge context and returns an `InvestigationReport`.

The command prints the selected provider name and model, but never prints its API key. A provider with the `structured_output` tag must be enabled in Runtime settings. Running with `--invoke` can incur provider usage charges.

An optional analyst instruction can be added to the second request:

```bash
uv run python manage.py explain_case_analysis case_000001 \
  --invoke \
  --user-input "Focus on lateral movement"
```

## Example transcripts

The following captured `--invoke` runs show the complete serialized input, both prompts, generated Knowledge keywords, Knowledge search results, and final structured report:

- [`case_000339`: suspicious privileged login](case-analysis-000339.md)
- [`case_000340`: correlated identity and endpoint activity](case-analysis-000340.md)
- [`case_000341`: external indicator enrichment](case-analysis-000341.md)

These are snapshots of real model runs. Re-running the command may produce different wording or conclusions, and the transcripts may contain Case evidence that should be handled as potentially sensitive data.

## How it differs from the worker

| Behavior | Educational command | Case Analysis Worker |
| --- | --- | --- |
| Started directly from the CLI | Yes | Normally runs continuously |
| Requires a queued job | No | Yes |
| Uses production Case serialization and prompts | Yes | Yes |
| Searches production Knowledge records | Yes | Yes |
| Calls the LLM | Only with `--invoke` | Yes |
| Saves Case AI fields and investigation report | No | Yes |
| Updates Case-analysis job status and result | No | Yes |

If keyword generation fails in live mode, the command displays the failure and continues with the same deterministic fallback used by the worker. If investigation generation fails, it exits with a `CommandError`. In either case, it does not modify the Case.

## Useful commands

Show all arguments:

```bash
uv run python manage.py explain_case_analysis --help
```

Capture a preview for inspection:

```bash
uv run python manage.py explain_case_analysis case_000001 > case-analysis-preview.txt
```

The captured file is intentionally not a supported input to the worker; it is only a readable representation of the messages and intermediate data.

## Source mapping

The walkthrough command is implemented in `backend/apps/agentic/management/commands/explain_case_analysis.py`. Its production counterparts are:

- `backend/apps/agentic/analysis/profiles.py` for Case serialization.
- `backend/apps/agentic/analysis/knowledge.py` for keyword normalization, fallback, and Knowledge search.
- `backend/apps/agentic/analysis/prompts.py` for prompt loading and structured LLM invocation.
- `backend/integrations/llm/llmapi.py` for LangChain `ChatOpenAI` construction and provider selection.
- `backend/apps/agentic/analysis/analysis.py` for orchestration and persistence performed by the worker.

For the full production flow, see [LLM investigation and enrichment](llm-and-enrichment.md) and [Workers and Agentic Runtime](workers-and-runtime.md).
