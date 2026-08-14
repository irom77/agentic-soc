from django.core.management.base import BaseCommand, CommandError

from apps.agentic.services.cases import request_case_analysis
from apps.cases.models import Case

from .reset_case_triage_demo import DEMO_CORRELATION_PREFIX


LIVE_LLM_CORRELATION_UID = f"{DEMO_CORRELATION_PREFIX}LIVE-LLM-INVESTIGATION"


class Command(BaseCommand):
    help = "Queue the seeded live-LLM Case for Agentic SOC investigation."

    def handle(self, *args, **options):
        case = Case.objects.filter(correlation_uid=LIVE_LLM_CORRELATION_UID).first()
        if case is None:
            raise CommandError(
                "Live LLM demo Case not found. Run seed_case_triage_demo --include-live-llm first."
            )

        job = request_case_analysis(case=case, trigger="demo_live_llm")
        self.stdout.write(self.style.SUCCESS(
            f"Queued [DEMO LIVE LLM] Case {case.pk} as job {job.pk}."
        ))
        self.stdout.write(
            "The case-analysis worker will send it to the enabled structured_output provider."
        )
