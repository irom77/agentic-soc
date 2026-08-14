# v0.6.0 release scope

Status: Confirmed

## 1. Release objective

v0.6.0 is for single-organization private deployment. The goal is to let a small SOC team reliably handle alert triage, case investigation, response execution, and day-to-day operations. This release prioritizes a complete core loop; it is not targeting SaaS, multi-tenancy, or large-scale clusters.

## 2. Supported deployment

- The only officially supported deployment topology is single-host Docker Compose.
- Kubernetes, horizontal scaling, multi-node high availability, and automatic failover are not supported.
- Each backend Worker officially supports a single instance; duplicate instances are not supported and will overwrite each other’s Worker Health state.
- Database downgrades are not supported. Rollback depends on restoring a backup taken before upgrade.

## 3. Upgrade contract

- Direct upgrade from v0.5.2 to v0.6.0 must be supported.
- The upgrade must preserve all business data, users, LDAP configuration, integration configuration, API keys, attachments, and custom scripts.
- All database changes must be delivered through Django migrations.
- Migrations must work on existing data and must not require clearing the database.
- The upgrade flow remains: run migrations first, then start application services and Workers.
- Direct upgrade from v0.5.1 or earlier is not promised, and no database downgrade from v0.6.0 to v0.5.2 is provided.

## 4. Capacity baseline

Formal acceptance uses the existing `generate_perf_data --scale medium` dataset size:

| Resource | Baseline |
| --- | ---: |
| Users | 20 |
| Cases | 10,000 |
| Alerts | 100,000 |
| Artifacts | 50,000 |
| Alert-artifact links | 300,000 |
| Enrichments | 30,000 |
| Playbook runs | 10,000 |
| Knowledge records | 2,000 |
| Audit logs | 100,000 |

The `large` and `extreme` dataset sizes may be used for development load testing, but they are not part of the v0.6.0 response-time commitment.

## 5. Official compatibility matrix

| Area | Officially supported |
| --- | --- |
| SIEM | Splunk, ELK |
| LLM | OpenAI-compatible Chat Completions endpoints |
| Threat intelligence | AlienVault OTX, OpenCTI |
| Authentication | Local account, LDAP |
| Object storage | S3-compatible storage configured by the current Compose distribution |
| Cache/stream | Redis configured by the current Compose distribution |

Vendor names that appear in code enums or UI examples do not imply official connectors or compatibility commitments.

## 6. Roles

v0.6.0 keeps three fixed roles:

| Role | Meaning |
| --- | --- |
| Admin | System administration and all business write operations |
| User / Analyst | Analyst business write operations |
| Viewer | Read-only access |

Custom roles, a permissions editor, and team-level data isolation are not implemented. Each new feature must define the exact permissions for the three roles in its own spec.

## 7. Language

- The official UI supports English only.
- User-facing project documentation keeps both Chinese and English versions; Chinese is written first, then English is synced afterward.
- v0.6.0 does not introduce a frontend i18n framework.

## 8. API compatibility

- v0.6.0 allows breaking changes to the existing frontend API and `/api/agent/v1/`.
- Do not create Agent API v2 as a compatibility layer.
- Do not require old CLI clients or old plugins to reject connections, and do not maintain compatibility for them.
- The new API should still have a clear DRF schema to avoid accidental response drift.

## 9. Confirmed functional domains

1. Bulk Case triage.
2. Case Relationships.
3. Playbook execution observability and control.
4. Custom Variables.
5. Worker Health.
6. SLA management.
7. AI quality evaluation.

SLA and AI quality evaluation are release blockers for v0.6.0.

## 10. Explicit exclusions

- Multi-tenancy and organization/Workspace isolation.
- Kubernetes and high-availability deployments.
- OIDC, SAML, or other SSO.
- Custom roles.
- Dedicated connectors such as Jira or ServiceNow.
- Visual or form-based Playbook orchestrators.
- Mid-run human approval for Playbooks.
- A generic HTTP/Webhook Connector or a unified vendor-action abstraction.
- UI/database-driven Suppression Rules; suppression logic is handled by custom Module Python code.
- Scheduled Integration Health probing and a unified status page; keep manual Test actions on each Settings page.
- A shared Worker/Integration Operations Center; Worker Health uses a separate implementation.
- Global UI internationalization.
- Legacy CLI/plugin compatibility layers.

## 11. Cross-domain invariants

- Case Relationships are weak links and do not affect the Dashboard, SLA, case counts, routing, or Case lifecycle.
- Single-Case edits and bulk edits must call the same server-side state machine.
- Playbook, Module, and Worker errors must not expose raw credentials, response bodies, or tracebacks through the API.
- Admin actions are written to AuditLog according to each spec; high-frequency health telemetry is not written to AuditLog.
- All times are stored as timezone-aware UTC and displayed in the browser’s local timezone.
- All list APIs must paginate; dynamic Stage counts are unbounded, so the Stage API must especially avoid returning everything at once.
- Business write operations must not rely on frontend restrictions instead of server-side permission and state checks.
