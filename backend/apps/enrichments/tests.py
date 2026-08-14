from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.alerts.models import Alert
from apps.artifacts.models import Artifact
from apps.cases.models import Case

from .models import Enrichment


class EnrichmentCaseScopeTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username="analyst", password="password")
        self.client = APIClient()
        self.client.force_authenticate(user)

        self.case = Case.objects.create(title="Scoped case")
        other_case = Case.objects.create(title="Other case")
        alert = Alert.objects.create(case=self.case, title="Scoped alert")
        artifact = Artifact.objects.create(value="scoped.example")
        alert.artifacts.add(artifact)

        self.expected_enrichments = {
            str(Enrichment.objects.create(case=self.case, name="Case enrichment").id),
            str(Enrichment.objects.create(alert=alert, name="Alert enrichment").id),
            str(Enrichment.objects.create(artifact=artifact, name="Artifact enrichment").id),
        }
        Enrichment.objects.create(case=other_case, name="Unrelated enrichment")

    def test_case_scope_includes_case_alert_and_artifact_enrichments(self):
        response = self.client.get("/api/enrichments/", {"case_scope": self.case.id})

        self.assertEqual(response.status_code, 200)
        returned_ids = {item["id"] for item in response.data["results"]}
        self.assertEqual(returned_ids, self.expected_enrichments)

    def test_case_scope_does_not_duplicate_artifact_enrichment_shared_by_alerts(self):
        second_alert = Alert.objects.create(case=self.case, title="Second scoped alert")
        artifact_enrichment = Enrichment.objects.get(name="Artifact enrichment")
        second_alert.artifacts.add(artifact_enrichment.artifact)

        response = self.client.get("/api/enrichments/", {"case_scope": self.case.id})

        self.assertEqual(response.status_code, 200)
        returned_ids = [item["id"] for item in response.data["results"]]
        self.assertEqual(returned_ids.count(str(artifact_enrichment.id)), 1)
