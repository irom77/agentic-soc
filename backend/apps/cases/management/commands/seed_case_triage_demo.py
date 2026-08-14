import json
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command, get_commands
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.agentic.models import AgenticJobStatus, CaseAnalysisJob
from apps.alerts.models import (
    Alert,
    AlertAction,
    AlertAnalyticState,
    AlertAnalyticType,
    AlertRiskLevel,
    AlertStatus,
    Confidence,
    Impact,
    ProductCategory,
    Severity,
)
from apps.artifacts.models import Artifact, ArtifactName, ArtifactRole, ArtifactType
from apps.cases.models import (
    Case,
    CaseCategory,
    CaseConfidence,
    CaseImpact,
    CasePriority,
    CaseSeverity,
    CaseStatus,
    CaseVerdict,
)
from apps.enrichments.models import Enrichment, EnrichmentProvider, EnrichmentType

from .reset_case_triage_demo import DEMO_CORRELATION_PREFIX


DEMO_TAG = "case-triage-demo"
DEMO_PASSWORD = "demopass"


def create_complex_live_llm_context(case, now):
    source_ip = Artifact.objects.create(
        name=ArtifactName.SOURCE_IP,
        type=ArtifactType.IP_ADDRESS,
        role=ArtifactRole.ACTOR,
        value="198.51.100.42",
    )
    account = Artifact.objects.create(
        name=ArtifactName.ACCOUNT_NAME,
        type=ArtifactType.ACCOUNT,
        role=ArtifactRole.AFFECTED,
        value="svc-finance-automation",
    )
    host = Artifact.objects.create(
        name=ArtifactName.HOSTNAME,
        type=ArtifactType.HOSTNAME,
        role=ArtifactRole.AFFECTED,
        value="fin-app-07.corp.example",
    )
    command = Artifact.objects.create(
        name=ArtifactName.PROCESS_COMMAND_LINE,
        type=ArtifactType.COMMAND_LINE,
        role=ArtifactRole.RELATED,
        value="powershell.exe -enc <redacted-demo-payload>",
    )

    identity_alert = Alert.objects.create(
        case=case,
        title="Service account sign-in from an unfamiliar network",
        severity=Severity.HIGH,
        confidence=Confidence.HIGH,
        impact=Impact.HIGH,
        action=AlertAction.ALLOWED,
        labels=["identity", "service-account", "new-country"],
        desc=(
            "The finance automation account authenticated without its normal workload identity and "
            "enumerated privileged role assignments. MFA is not configured for this non-interactive account."
        ),
        first_seen_time=now - timedelta(minutes=18),
        last_seen_time=now - timedelta(minutes=15),
        rule_id="DEMO-IAM-1042",
        rule_name="Unusual service-account interactive sign-in",
        analytic_name="Identity behavior analytics",
        analytic_type=AlertAnalyticType.BEHAVIORAL,
        analytic_state=AlertAnalyticState.ACTIVE,
        product_category=ProductCategory.IAM,
        product_vendor="Demo Identity Cloud",
        product_name="Demo Identity Protection",
        risk_level=AlertRiskLevel.HIGH,
        status=AlertStatus.NEW,
        correlation_uid=case.correlation_uid,
    )
    identity_alert.artifacts.add(source_ip, account)

    endpoint_alert = Alert.objects.create(
        case=case,
        title="Encoded PowerShell launched on finance application server",
        severity=Severity.CRITICAL,
        confidence=Confidence.HIGH,
        impact=Impact.HIGH,
        action=AlertAction.OBSERVED,
        labels=["endpoint", "powershell", "credential-access"],
        desc=(
            "Eight minutes after the unusual sign-in, the same account opened a remote session to the "
            "finance application server and launched encoded PowerShell from a service process."
        ),
        first_seen_time=now - timedelta(minutes=10),
        last_seen_time=now - timedelta(minutes=8),
        rule_id="DEMO-EDR-2048",
        rule_name="Encoded PowerShell from service process",
        analytic_name="Endpoint behavioral detection",
        analytic_type=AlertAnalyticType.BEHAVIORAL,
        analytic_state=AlertAnalyticState.ACTIVE,
        product_category=ProductCategory.EDR,
        product_vendor="Demo Endpoint Security",
        product_name="Demo EDR",
        risk_level=AlertRiskLevel.CRITICAL,
        status=AlertStatus.NEW,
        correlation_uid=case.correlation_uid,
    )
    endpoint_alert.artifacts.add(account, host, command)

    Enrichment.objects.create(
        artifact=source_ip,
        name="Threat-intelligence reputation",
        type=EnrichmentType.REPUTATION,
        provider=EnrichmentProvider.MOCK_TI_PROVIDER,
        uid="demo-complex-live-llm:source-ip-reputation",
        value=source_ip.value,
        desc="Observed in credential-stuffing activity by three tenants during the previous 24 hours; confidence high.",
        data={"documentation_only": True, "risk_score": 92},
    )
    Enrichment.objects.create(
        artifact=account,
        name="Identity directory context",
        type=EnrichmentType.IDENTITY,
        provider=EnrichmentProvider.MICROSOFT_ENTRA_ID,
        uid="demo-complex-live-llm:account-context",
        value=account.value,
        desc="Non-interactive finance service account; owner is Finance Platform; no approved interactive sign-ins.",
        data={"privileged": True, "interactive_login_allowed": False},
    )
    Enrichment.objects.create(
        artifact=host,
        name="CMDB asset context",
        type=EnrichmentType.CMDB,
        provider=EnrichmentProvider.INTERNAL_CMDB,
        uid="demo-complex-live-llm:asset-context",
        value=host.value,
        desc="Production finance application server processing payment files; business criticality is High.",
        data={"environment": "production", "business_criticality": "High"},
    )
    Enrichment.objects.create(
        alert=endpoint_alert,
        name="EDR process-tree review",
        type=EnrichmentType.DETECTION,
        provider=EnrichmentProvider.MOCK,
        uid="demo-complex-live-llm:process-tree",
        value="encoded PowerShell",
        desc="No approved deployment job matched the process tree; outbound connection telemetry is unavailable.",
        data={"approved_change": False, "network_telemetry_available": False},
    )

ORDINAL_CASES = [
    {
        "slug": "agreement-ransomware",
        "title": "[DEMO QUALITY] Ransomware behavior confirmed",
        "category": CaseCategory.EDR,
        "human": (CaseVerdict.TRUE_POSITIVE, CaseSeverity.CRITICAL, CaseImpact.CRITICAL, CasePriority.CRITICAL, CaseConfidence.HIGH),
        "ai": (CaseVerdict.TRUE_POSITIVE, CaseSeverity.CRITICAL, CaseImpact.CRITICAL, CasePriority.CRITICAL, CaseConfidence.HIGH),
        "days_ago": 2,
        "assignee": "demo.alice",
    },
    {
        "slug": "overestimate-vpn",
        "title": "[DEMO QUALITY] Approved VPN created impossible travel",
        "category": CaseCategory.IAM,
        "human": (CaseVerdict.FALSE_POSITIVE, CaseSeverity.MEDIUM, CaseImpact.LOW, CasePriority.LOW, CaseConfidence.HIGH),
        "ai": (CaseVerdict.SUSPICIOUS, CaseSeverity.HIGH, CaseImpact.MEDIUM, CasePriority.HIGH, CaseConfidence.HIGH),
        "days_ago": 4,
        "assignee": "demo.bob",
    },
    {
        "slug": "underestimate-phishing",
        "title": "[DEMO QUALITY] Executive phishing campaign",
        "category": CaseCategory.EMAIL,
        "human": (CaseVerdict.TRUE_POSITIVE, CaseSeverity.HIGH, CaseImpact.HIGH, CasePriority.CRITICAL, CaseConfidence.HIGH),
        "ai": (CaseVerdict.SUSPICIOUS, CaseSeverity.MEDIUM, CaseImpact.MEDIUM, CasePriority.MEDIUM, CaseConfidence.MEDIUM),
        "days_ago": 8,
        "assignee": "demo.alice",
    },
    {
        "slug": "mixed-dns",
        "title": "[DEMO QUALITY] DNS tunneling investigation",
        "category": CaseCategory.NDR,
        "human": (CaseVerdict.SECURITY_RISK, CaseSeverity.HIGH, CaseImpact.MEDIUM, CasePriority.HIGH, CaseConfidence.MEDIUM),
        "ai": (CaseVerdict.SECURITY_RISK, CaseSeverity.HIGH, CaseImpact.HIGH, CasePriority.HIGH, CaseConfidence.MEDIUM),
        "days_ago": 13,
        "assignee": "demo.bob",
    },
    {
        "slug": "unknown-values",
        "title": "[DEMO QUALITY] Inconclusive cloud process activity",
        "category": CaseCategory.CLOUD,
        "human": (CaseVerdict.INSUFFICIENT_DATA, CaseSeverity.UNKNOWN, CaseImpact.UNKNOWN, CasePriority.MEDIUM, CaseConfidence.LOW),
        "ai": (CaseVerdict.INSUFFICIENT_DATA, CaseSeverity.UNKNOWN, CaseImpact.UNKNOWN, CasePriority.LOW, CaseConfidence.LOW),
        "days_ago": 20,
        "assignee": "demo.alice",
    },
]


def ensure_demo_users():
    user_model = get_user_model()
    users = {}
    for username, first_name, last_name, is_superuser in [
        ("demo.admin", "Demo", "Admin", True),
        ("demo.alice", "Alice", "Analyst", False),
        ("demo.bob", "Bob", "Analyst", False),
    ]:
        user, _ = user_model.objects.get_or_create(username=username)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.is_staff = is_superuser
        user.is_superuser = is_superuser
        user.set_password(DEMO_PASSWORD)
        user.save()
        users[username] = user
    return users


def analysis_record(case, ai_values, generated_at):
    verdict, severity, impact, priority, confidence = ai_values
    return {
        "trigger": "demo-seed",
        "source_type": "case",
        "source_id": str(case.pk),
        "profile_version": "demo-v1",
        "generated_at": generated_at.isoformat(),
        "knowledge_keywords": ["demo", case.category.lower()],
        "knowledge_records": [],
        "report": {
            "verdict": verdict,
            "severity": severity,
            "impact": impact,
            "priority": priority,
            "confidence": confidence,
            "digest": "Deterministic seeded analysis for the Case triage and AI quality demonstration.",
            "affected_assets": [],
            "evidence_findings": [],
            "attack_chain": [],
            "attack_timeline": [],
            "ioc_indicators": [],
            "remediations": [],
            "unknowns": [],
        },
    }


def create_case(*, slug, title, category, status, assignee, human, ai=None, closed_at=None):
    verdict, severity, impact, priority, confidence = human
    case = Case.objects.create(
        title=title,
        description="Seeded scenario for the Case triage and AI–Human Agreement product demonstration.",
        summary="Prepared demo Case. Follow docs/demo/case-triage-and-ai-quality.md during the walkthrough.",
        category=category,
        tags=[DEMO_TAG, f"demo:{slug}"],
        status=status,
        verdict=verdict,
        severity=severity,
        impact=impact,
        priority=priority,
        confidence=confidence,
        assignee=assignee,
        acknowledged_time=(closed_at - timedelta(hours=5)) if closed_at else None,
        closed_time=closed_at,
        correlation_uid=f"{DEMO_CORRELATION_PREFIX}{slug.upper()}",
        verdict_ai=ai[0] if ai else "",
        severity_ai=ai[1] if ai else "",
        impact_ai=ai[2] if ai else "",
        priority_ai=ai[3] if ai else "",
        confidence_ai=ai[4] if ai else "",
        investigation_report_ai_json="",
    )
    if ai:
        completed_at = closed_at - timedelta(hours=2) if closed_at else timezone.now() - timedelta(minutes=20)
        record = analysis_record(case, ai, completed_at)
        Case.objects.filter(pk=case.pk).update(investigation_report_ai_json=json.dumps(record))
        CaseAnalysisJob.objects.create(
            case=case,
            status=AgenticJobStatus.SUCCESS,
            trigger="demo-seed",
            scheduled_at=completed_at - timedelta(minutes=3),
            started_at=completed_at - timedelta(minutes=2),
            completed_at=completed_at,
            result_json=record,
        )
    return case


class Command(BaseCommand):
    help = "Seed Cases for the triage, Investigation, and future AI quality demo."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-reset",
            action="store_true",
            help="Keep an existing demo dataset instead of replacing it.",
        )
        parser.add_argument(
            "--include-live-llm",
            action="store_true",
            help="Also create an unprocessed Case for a before-and-after LLM investigation.",
        )
        parser.add_argument(
            "--include-complex-live-llm",
            action="store_true",
            help="Also create an unprocessed live-LLM Case with Alerts, artifacts, and enrichments.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        existing = Case.objects.filter(correlation_uid__startswith=DEMO_CORRELATION_PREFIX)
        if existing.exists() and options["no_reset"]:
            self.stdout.write(self.style.WARNING(f"Demo data already exists ({existing.count()} Cases); no changes made."))
            return
        existing_artifact_ids = list(
            Artifact.objects.filter(alerts__case__in=existing).values_list("id", flat=True).distinct()
        )
        existing.delete()
        Artifact.objects.filter(id__in=existing_artifact_ids, alerts__isnull=True).delete()

        users = ensure_demo_users()
        now = timezone.now()
        created = []

        statuses = [CaseStatus.NEW, CaseStatus.IN_PROGRESS, CaseStatus.ON_HOLD]
        categories = [CaseCategory.IAM, CaseCategory.CLOUD, CaseCategory.EMAIL]
        for index in range(1, 19):
            status = statuses[(index - 1) % len(statuses)]
            ai = (
                CaseVerdict.SUSPICIOUS,
                CaseSeverity.HIGH if index % 3 == 0 else CaseSeverity.MEDIUM,
                CaseImpact.MEDIUM,
                CasePriority.HIGH if index % 4 == 0 else CasePriority.MEDIUM,
                CaseConfidence.MEDIUM,
            )
            human = (
                CaseVerdict.SUSPICIOUS if status != CaseStatus.NEW else "",
                CaseSeverity.MEDIUM,
                CaseImpact.MEDIUM,
                CasePriority.MEDIUM,
                CaseConfidence.MEDIUM,
            )
            created.append(create_case(
                slug=f"campaign-{index:02d}",
                title=f"[DEMO TRIAGE] Identity campaign signal {index:02d}",
                category=categories[(index - 1) % len(categories)],
                status=status,
                assignee=users["demo.alice"] if index % 2 else users["demo.bob"],
                human=human,
                ai=ai,
            ))

        for spec in ORDINAL_CASES:
            created.append(create_case(
                slug=spec["slug"],
                title=spec["title"],
                category=spec["category"],
                status=CaseStatus.CLOSED,
                assignee=users[spec["assignee"]],
                human=spec["human"],
                ai=spec["ai"],
                closed_at=now - timedelta(days=spec["days_ago"]),
            ))

        no_prediction = create_case(
            slug="no-prediction",
            title="[DEMO QUALITY] Closed without an AI prediction",
            category=CaseCategory.OTHER,
            status=CaseStatus.CLOSED,
            assignee=users["demo.bob"],
            human=(CaseVerdict.BENIGN, CaseSeverity.LOW, CaseImpact.LOW, CasePriority.LOW, CaseConfidence.HIGH),
            closed_at=now - timedelta(days=6),
        )
        created.append(no_prediction)

        invalid_prediction = create_case(
            slug="invalid-prediction",
            title="[DEMO QUALITY] Closed with an invalid AI prediction",
            category=CaseCategory.SIEM,
            status=CaseStatus.CLOSED,
            assignee=users["demo.alice"],
            human=(CaseVerdict.TRUE_POSITIVE, CaseSeverity.HIGH, CaseImpact.MEDIUM, CasePriority.HIGH, CaseConfidence.HIGH),
            closed_at=now - timedelta(days=10),
        )
        CaseAnalysisJob.objects.create(
            case=invalid_prediction,
            status=AgenticJobStatus.SUCCESS,
            trigger="demo-seed-invalid",
            scheduled_at=invalid_prediction.closed_time - timedelta(hours=3),
            started_at=invalid_prediction.closed_time - timedelta(hours=2, minutes=59),
            completed_at=invalid_prediction.closed_time - timedelta(hours=2),
            result_json={"invalid_demo_payload": True},
        )
        created.append(invalid_prediction)

        if options["include_live_llm"]:
            live_case = create_case(
                slug="live-llm-investigation",
                title="[DEMO LIVE LLM] Suspicious privileged login investigation",
                category=CaseCategory.IAM,
                status=CaseStatus.NEW,
                assignee=users["demo.alice"],
                human=("", CaseSeverity.HIGH, CaseImpact.HIGH, CasePriority.HIGH, CaseConfidence.MEDIUM),
            )
            live_case.description = (
                "A privileged account signed in from a new country shortly after a successful login from its usual location. "
                "The source IP is not present in the approved VPN range, and the account accessed identity administration APIs."
            )
            live_case.summary = "Awaiting live Agentic SOC Case investigation."
            live_case.tags = [DEMO_TAG, "demo:live-llm-investigation", "identity", "privileged-access", "impossible-travel"]
            live_case.save(update_fields=["description", "summary", "tags", "updated_at"])
            created.append(live_case)

        if options["include_complex_live_llm"]:
            complex_case = create_case(
                slug="complex-live-llm-enrichment",
                title="[DEMO COMPLEX LLM] Correlated identity and endpoint activity",
                category=CaseCategory.SIEM,
                status=CaseStatus.NEW,
                assignee=users["demo.alice"],
                human=("", CaseSeverity.CRITICAL, CaseImpact.HIGH, CasePriority.CRITICAL, CaseConfidence.HIGH),
            )
            complex_case.description = (
                "Correlate an unusual service-account sign-in with subsequent encoded PowerShell execution "
                "on a production finance server. Validate the attached source, identity, asset, and process context."
            )
            complex_case.summary = "Awaiting enriched live Agentic SOC Case investigation."
            complex_case.tags = [DEMO_TAG, "demo:complex-live-llm-enrichment", "identity", "endpoint", "correlated"]
            complex_case.save(update_fields=["description", "summary", "tags", "updated_at"])
            create_complex_live_llm_context(complex_case, now)
            created.append(complex_case)

        live_count = int(options["include_live_llm"]) + int(options["include_complex_live_llm"])
        live_summary = f" and {live_count} live LLM Case(s)" if live_count else ""
        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(created)} demo Cases: 18 triage Cases, 7 closed AI quality Cases{live_summary}."
        ))
        self.stdout.write(f"Demo users: demo.admin, demo.alice, demo.bob (password: {DEMO_PASSWORD})")

        if "rebuild_ai_quality_evaluations" in get_commands():
            transaction.on_commit(lambda: call_command("rebuild_ai_quality_evaluations"))
            self.stdout.write("AI quality evaluation rebuild scheduled after commit.")
        else:
            self.stdout.write(self.style.WARNING(
                "AI quality evaluation is not implemented on this branch; source Jobs and Case AI fields were seeded."
            ))

        if live_count:
            self.stdout.write(
                "Live LLM Case(s) are ready but not queued. Use the matching queue command after showing the empty Investigation tab."
            )
