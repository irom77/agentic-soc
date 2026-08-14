from django.core.management.base import BaseCommand, CommandError

from apps.agentic.services.cases import request_case_analysis
from apps.cases.models import Case

from .reset_case_triage_demo import DEMO_CORRELATION_PREFIX


COMPLEX_LLM_CORRELATION_UID = f"{DEMO_CORRELATION_PREFIX}COMPLEX-LIVE-LLM-ENRICHMENT"


class Command(BaseCommand):
    help = "Queue the enriched live-LLM Case for Agentic SOC investigation."

    def handle(self, *args, **options):
        case = Case.objects.filter(correlation_uid=COMPLEX_LLM_CORRELATION_UID).first()
        if case is None:
            raise CommandError(
                "Complex live LLM demo Case not found. Run "
                "seed_case_triage_demo --include-complex-live-llm first."
            )

        job = request_case_analysis(case=case, trigger="demo_complex_live_llm")
        self.stdout.write(self.style.SUCCESS(
            f"Queued [DEMO COMPLEX LLM] Case {case.pk} as job {job.pk}."
        ))
        self.stdout.write(
            "The case-analysis worker will send its Alerts, artifacts, and enrichments to the enabled structured_output provider."
        )
