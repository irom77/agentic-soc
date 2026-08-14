import json
from uuid import UUID

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from apps.agentic.analysis.knowledge import (
    fallback_knowledge_keywords,
    normalize_knowledge_keywords,
    search_knowledge_records,
)
from apps.agentic.analysis.profiles import serialize_case_for_investigation
from apps.agentic.analysis.prompts import (
    INVESTIGATION_KNOWLEDGE_KEYWORD_PROMPT,
    INVESTIGATION_SYSTEM_PROMPT,
    invoke_structured_llm,
    read_prompt,
)
from apps.agentic.analysis.schemas import InvestigationReport, KnowledgeSearchKeywords
from apps.cases.models import Case
from integrations.llm.llmapi import LLMAPI


class Command(BaseCommand):
    help = "Show, and optionally run, the LLM workflow used by the Case Analysis Worker."

    def add_arguments(self, parser):
        parser.add_argument("case", help="Readable Case ID (case_000001) or UUID.")
        parser.add_argument(
            "--invoke",
            action="store_true",
            help="Call the configured LLM. Without this flag, no LLM request is made.",
        )
        parser.add_argument(
            "--user-input",
            default="",
            help="Optional analyst instruction included in the investigation request.",
        )

    def handle(self, *args, **options):
        case = self._find_case(options["case"])
        case_payload = serialize_case_for_investigation(case)

        self._heading("1. Serialize the Case")
        self.stdout.write(
            "The worker selects the Investigation profile and excludes raw/internal and previous AI fields."
        )
        self._json(case_payload)

        self._heading("2. Ask the LLM for Knowledge search keywords")
        self._messages(INVESTIGATION_KNOWLEDGE_KEYWORD_PROMPT, case_payload)

        if options["invoke"]:
            self._provider()
            try:
                keyword_result = invoke_structured_llm(
                    prompt_id=INVESTIGATION_KNOWLEDGE_KEYWORD_PROMPT,
                    payload=case_payload,
                    output_schema=KnowledgeSearchKeywords,
                )
                keywords = normalize_knowledge_keywords(keyword_result.keywords)
                self.stdout.write("\nStructured LLM response:")
                self._json(keyword_result.model_dump())
            except Exception as exc:
                keywords = fallback_knowledge_keywords(case_payload)
                self.stderr.write(
                    self.style.WARNING(
                        f"Keyword LLM call failed ({type(exc).__name__}: {exc}). "
                        "The production worker continues with deterministic fallback keywords."
                    )
                )
        else:
            keywords = fallback_knowledge_keywords(case_payload)
            self.stdout.write(
                "\nPreview mode: using the production fallback keywords because --invoke was not supplied."
            )

        self._heading("3. Search Knowledge in PostgreSQL")
        self.stdout.write("Keywords:")
        self._json(keywords)
        knowledge_records = search_knowledge_records(keywords)
        self.stdout.write("Matching unexpired Knowledge records (maximum 10):")
        self._json(knowledge_records)

        analysis_input = {
            "case": case_payload,
            "knowledge": {"keywords": keywords, "records": knowledge_records},
        }
        if options["user_input"]:
            analysis_input["user_input"] = options["user_input"]

        self._heading("4. Ask the LLM for a structured InvestigationReport")
        self._messages(INVESTIGATION_SYSTEM_PROMPT, analysis_input)

        if not options["invoke"]:
            self._heading("5. Stop without writing")
            self.stdout.write(
                "Preview complete. Re-run with --invoke to make both LLM calls. "
                "This command never saves the returned report to the Case."
            )
            return

        try:
            report = invoke_structured_llm(
                prompt_id=INVESTIGATION_SYSTEM_PROMPT,
                payload=analysis_input,
                output_schema=InvestigationReport,
            )
        except Exception as exc:
            raise CommandError(f"Investigation LLM call failed: {type(exc).__name__}: {exc}") from exc

        self.stdout.write("\nStructured LLM response:")
        self._json(report.model_dump())
        self._heading("5. Stop without writing")
        self.stdout.write(
            "The real worker now builds an AnalysisRecord and updates the Case AI fields, report, and job. "
            "This educational command deliberately leaves them unchanged."
        )

    def _find_case(self, value):
        query = Q(case_id=value)
        try:
            query |= Q(pk=UUID(value))
        except ValueError:
            pass
        try:
            return Case.objects.get(query)
        except Case.DoesNotExist as exc:
            raise CommandError(f"Case not found: {value}") from exc

    def _provider(self):
        config = LLMAPI().select_config(tag="structured_output")
        self.stdout.write(
            "\nSelected provider: "
            f"{config.get('name', '(unnamed)')} / {config.get('model', '(model not set)')} "
            "[tag: structured_output]"
        )

    def _messages(self, prompt_id, payload):
        self.stdout.write("SystemMessage:")
        self.stdout.write(read_prompt(prompt_id))
        self.stdout.write("\nHumanMessage (JSON):")
        self._json(payload)

    def _heading(self, text):
        self.stdout.write(f"\n=== {text} ===")

    def _json(self, value):
        self.stdout.write(json.dumps(value, ensure_ascii=False, indent=2, default=str))
