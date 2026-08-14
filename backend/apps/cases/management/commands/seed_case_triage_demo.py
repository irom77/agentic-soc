import json
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command, get_commands
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.agentic.models import AgenticJobStatus, CaseAnalysisJob
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

from .reset_case_triage_demo import DEMO_CORRELATION_PREFIX


DEMO_TAG = "case-triage-demo"
DEMO_PASSWORD = "demopass"

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
    help = "Seed deterministic Cases for the bulk triage and AI quality demo."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-reset",
            action="store_true",
            help="Keep an existing demo dataset instead of replacing it.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        existing = Case.objects.filter(correlation_uid__startswith=DEMO_CORRELATION_PREFIX)
        if existing.exists() and options["no_reset"]:
            self.stdout.write(self.style.WARNING(f"Demo data already exists ({existing.count()} Cases); no changes made."))
            return
        existing.delete()

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

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(created)} demo Cases: 18 triage Cases and 7 closed AI quality Cases."
        ))
        self.stdout.write(f"Demo users: demo.admin, demo.alice, demo.bob (password: {DEMO_PASSWORD})")

        if "rebuild_ai_quality_evaluations" in get_commands():
            transaction.on_commit(lambda: call_command("rebuild_ai_quality_evaluations"))
            self.stdout.write("AI quality evaluation rebuild scheduled after commit.")
        else:
            self.stdout.write(self.style.WARNING(
                "AI quality evaluation is not implemented on this branch; source Jobs and Case AI fields were seeded."
            ))
