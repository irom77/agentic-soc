from django.core.management.base import BaseCommand, CommandError

from apps.cases.models import Case


DEMO_CORRELATION_PREFIX = "DEMO-CASE-TRIAGE-"


class Command(BaseCommand):
    help = "Delete only the Cases created by seed_case_triage_demo."

    def add_arguments(self, parser):
        parser.add_argument(
            "--confirm",
            action="store_true",
            help="Confirm deletion of the scoped demo Cases.",
        )

    def handle(self, *args, **options):
        cases = Case.objects.filter(correlation_uid__startswith=DEMO_CORRELATION_PREFIX)
        count = cases.count()
        if not options["confirm"]:
            raise CommandError(
                f"Refusing to delete {count} demo Case(s) without --confirm. "
                "Only Cases whose correlation_uid starts with "
                f"{DEMO_CORRELATION_PREFIX!r} are in scope."
            )

        cases.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} demo Case(s)."))
