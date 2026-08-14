from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.agentic.services.playbooks import create_pending_playbook_run
from apps.cases.models import Case
from apps.settings.runtime_config import get_otx_config

from .reset_case_triage_demo import DEMO_CORRELATION_PREFIX


LIVE_OTX_CORRELATION_UID = f"{DEMO_CORRELATION_PREFIX}LIVE-OTX-ENRICHMENT"
PLAYBOOK_NAME = "Threat Intelligence Enrichment"


class Command(BaseCommand):
    help = "Queue live AlienVault OTX enrichment for the OTX demo Case."

    def handle(self, *args, **options):
        case = Case.objects.filter(correlation_uid=LIVE_OTX_CORRELATION_UID).first()
        if case is None:
            raise CommandError(
                "Live OTX demo Case not found. Run seed_case_triage_demo --include-live-otx first."
            )

        config = get_otx_config()
        if not config["enabled"] or not config["api_key"]:
            raise CommandError(
                "AlienVault OTX is not enabled with an API key. Configure and test it in "
                "System Settings > Threat Intelligence first."
            )

        user = get_user_model().objects.filter(username="demo.admin").first()
        playbook = create_pending_playbook_run(
            name=PLAYBOOK_NAME,
            case=case,
            user=user,
            user_input="Live OTX enrichment demo",
        )
        self.stdout.write(self.style.SUCCESS(
            f"Queued {PLAYBOOK_NAME} for Case {case.case_id} as {playbook.playbook_id}."
        ))
        self.stdout.write(
            "The playbook worker will query AlienVault OTX and save Artifact-level Enrichment records."
        )
