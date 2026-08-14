from django.core.management.base import BaseCommand, CommandError

from apps.agentic.services.cases import request_case_analysis
from apps.cases.models import Case
from apps.enrichments.models import EnrichmentProvider

from .queue_live_otx_enrichment_demo import LIVE_OTX_CORRELATION_UID


class Command(BaseCommand):
    help = "Queue the live-OTX demo Case for LLM investigation after enrichment."

    def handle(self, *args, **options):
        case = Case.objects.filter(correlation_uid=LIVE_OTX_CORRELATION_UID).first()
        if case is None:
            raise CommandError(
                "Live OTX demo Case not found. Run seed_case_triage_demo --include-live-otx first."
            )
        if not case.alerts.filter(
            artifacts__enrichments__provider=EnrichmentProvider.ALIENVAULT_OTX
        ).exists():
            raise CommandError(
                "No AlienVault OTX enrichment exists for this Case. Queue the enrichment and wait for its "
                "playbook run to succeed before requesting LLM investigation."
            )

        job = request_case_analysis(case=case, trigger="demo_live_otx")
        self.stdout.write(self.style.SUCCESS(
            f"Queued [DEMO LIVE OTX] Case {case.case_id} as analysis job {job.pk}."
        ))
        self.stdout.write(
            "The case-analysis worker will send the Alerts, artifacts, and saved OTX enrichment summaries to the LLM."
        )
