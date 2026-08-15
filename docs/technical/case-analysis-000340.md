# Case Analysis: case_000340

Generated with:

```bash
cd backend
uv run python manage.py explain_case_analysis case_000340 --invoke
```

The transcript below is a read-only walkthrough. The command invoked the configured LLM but did not save the returned report to the Case.

```
2026-08-15 07:35:43,860 INFO [httpx:1025] HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 200 OK"
2026-08-15 07:35:59,265 INFO [httpx:1025] HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 200 OK"

=== 1. Serialize the Case ===
The worker selects the Investigation profile and excludes raw/internal and previous AI fields.
{
  "created_at": "2026-08-14T18:48:28.410451+00:00",
  "updated_at": "2026-08-14T18:48:28.413053+00:00",
  "title": "[DEMO COMPLEX LLM] Correlated identity and endpoint activity",
  "severity": "Critical",
  "impact": "High",
  "priority": "Critical",
  "confidence": "High",
  "description": "Correlate an unusual service-account sign-in with subsequent encoded PowerShell execution on a production finance server. Validate the attached source, identity, asset, and process context.",
  "category": "SIEM",
  "tags": [
    "case-triage-demo",
    "demo:complex-live-llm-enrichment",
    "identity",
    "endpoint",
    "correlated"
  ],
  "status": "New",
  "acknowledged_time": null,
  "assignee": "Alice Analyst",
  "closed_time": null,
  "verdict": "",
  "summary": "Awaiting enriched live Agentic SOC Case investigation.",
  "alerts": [
    {
      "created_at": "2026-08-14T18:48:28.428677+00:00",
      "updated_at": "2026-08-14T18:48:28.428684+00:00",
      "title": "Service account sign-in from an unfamiliar network",
      "severity": "High",
      "confidence": "High",
      "impact": "High",
      "disposition": "Unknown",
      "action": "Allowed",
      "labels": [
        "identity",
        "service-account",
        "new-country"
      ],
      "desc": "The finance automation account authenticated without its normal workload identity and enumerated privileged role assignments. MFA is not configured for this non-interactive account.",
      "first_seen_time": "2026-08-14T18:30:28.287850+00:00",
      "last_seen_time": "2026-08-14T18:33:28.287850+00:00",
      "rule_id": "DEMO-IAM-1042",
      "rule_name": "Unusual service-account interactive sign-in",
      "analytic_name": "Identity behavior analytics",
      "analytic_type": "Behavioral",
      "analytic_state": "Active",
      "analytic_desc": "",
      "product_category": "IAM",
      "product_vendor": "Demo Identity Cloud",
      "product_name": "Demo Identity Protection",
      "product_feature": "",
      "policy_name": "",
      "policy_type": "",
      "policy_desc": "",
      "risk_level": "High",
      "status": "New",
      "status_detail": "",
      "artifacts": [
        {
          "created_at": "2026-08-14T18:48:28.417174+00:00",
          "updated_at": "2026-08-14T18:48:28.417181+00:00",
          "name": "Source IP",
          "type": "IP Address",
          "role": "Actor",
          "value": "198.51.100.42",
          "enrichments": [
            {
              "created_at": "2026-08-14T18:48:28.445344+00:00",
              "updated_at": "2026-08-14T18:48:28.445349+00:00",
              "name": "Threat-intelligence reputation",
              "type": "Reputation",
              "provider": "MockTIProvider",
              "value": "198.51.100.42",
              "desc": "Observed in credential-stuffing activity by three tenants during the previous 24 hours; confidence high."
            }
          ]
        },
        {
          "created_at": "2026-08-14T18:48:28.419778+00:00",
          "updated_at": "2026-08-14T18:48:28.419783+00:00",
          "name": "Account Name",
          "type": "Account",
          "role": "Affected",
          "value": "svc-finance-automation",
          "enrichments": [
            {
              "created_at": "2026-08-14T18:48:28.448300+00:00",
              "updated_at": "2026-08-14T18:48:28.448305+00:00",
              "name": "Identity directory context",
              "type": "Identity",
              "provider": "Microsoft Entra ID",
              "value": "svc-finance-automation",
              "desc": "Non-interactive finance service account; owner is Finance Platform; no approved interactive sign-ins."
            }
          ]
        }
      ],
      "enrichments": []
    },
    {
      "created_at": "2026-08-14T18:48:28.437129+00:00",
      "updated_at": "2026-08-14T18:48:28.437135+00:00",
      "title": "Encoded PowerShell launched on finance application server",
      "severity": "Critical",
      "confidence": "High",
      "impact": "High",
      "disposition": "Unknown",
      "action": "Observed",
      "labels": [
        "endpoint",
        "powershell",
        "credential-access"
      ],
      "desc": "Eight minutes after the unusual sign-in, the same account opened a remote session to the finance application server and launched encoded PowerShell from a service process.",
      "first_seen_time": "2026-08-14T18:38:28.287850+00:00",
      "last_seen_time": "2026-08-14T18:40:28.287850+00:00",
      "rule_id": "DEMO-EDR-2048",
      "rule_name": "Encoded PowerShell from service process",
      "analytic_name": "Endpoint behavioral detection",
      "analytic_type": "Behavioral",
      "analytic_state": "Active",
      "analytic_desc": "",
      "product_category": "EDR",
      "product_vendor": "Demo Endpoint Security",
      "product_name": "Demo EDR",
      "product_feature": "",
      "policy_name": "",
      "policy_type": "",
      "policy_desc": "",
      "risk_level": "Critical",
      "status": "New",
      "status_detail": "",
      "artifacts": [
        {
          "created_at": "2026-08-14T18:48:28.419778+00:00",
          "updated_at": "2026-08-14T18:48:28.419783+00:00",
          "name": "Account Name",
          "type": "Account",
          "role": "Affected",
          "value": "svc-finance-automation",
          "enrichments": [
            {
              "created_at": "2026-08-14T18:48:28.448300+00:00",
              "updated_at": "2026-08-14T18:48:28.448305+00:00",
              "name": "Identity directory context",
              "type": "Identity",
              "provider": "Microsoft Entra ID",
              "value": "svc-finance-automation",
              "desc": "Non-interactive finance service account; owner is Finance Platform; no approved interactive sign-ins."
            }
          ]
        },
        {
          "created_at": "2026-08-14T18:48:28.422620+00:00",
          "updated_at": "2026-08-14T18:48:28.422626+00:00",
          "name": "Hostname",
          "type": "Hostname",
          "role": "Affected",
          "value": "fin-app-07.corp.example",
          "enrichments": [
            {
              "created_at": "2026-08-14T18:48:28.450987+00:00",
              "updated_at": "2026-08-14T18:48:28.450991+00:00",
              "name": "CMDB asset context",
              "type": "CMDB",
              "provider": "Internal CMDB",
              "value": "fin-app-07.corp.example",
              "desc": "Production finance application server processing payment files; business criticality is High."
            }
          ]
        },
        {
          "created_at": "2026-08-14T18:48:28.425332+00:00",
          "updated_at": "2026-08-14T18:48:28.425338+00:00",
          "name": "Process Command Line",
          "type": "Command Line",
          "role": "Related",
          "value": "powershell.exe -enc <redacted-demo-payload>",
          "enrichments": []
        }
      ],
      "enrichments": [
        {
          "created_at": "2026-08-14T18:48:28.453836+00:00",
          "updated_at": "2026-08-14T18:48:28.453840+00:00",
          "name": "EDR process-tree review",
          "type": "Detection",
          "provider": "Mock",
          "value": "encoded PowerShell",
          "desc": "No approved deployment job matched the process tree; outbound connection telemetry is unavailable."
        }
      ]
    }
  ],
  "enrichments": [],
  "comments": [],
  "audit_logs": [
    {
      "created_at": "2026-08-14T18:48:28.411217+00:00",
      "action": "create",
      "actor": "",
      "changes": {},
      "metadata": {}
    },
    {
      "created_at": "2026-08-14T18:48:28.414506+00:00",
      "action": "update",
      "actor": "",
      "changes": {
        "tags": {
          "to": [
            "case-triage-demo",
            "demo:complex-live-llm-enrichment",
            "identity",
            "endpoint",
            "correlated"
          ],
          "from": [
            "case-triage-demo",
            "demo:complex-live-llm-enrichment"
          ]
        },
        "summary": {
          "to": "Awaiting enriched live Agentic SOC Case investigation.",
          "from": "Prepared demo Case. Follow docs/demo/case-triage-and-ai-quality.md during the walkthrough."
        },
        "description": {
          "to": "Correlate an unusual service-account sign-in with subsequent encoded PowerShell execution on a production finance server. Validate the attached source, identity, asset, and process context.",
          "from": "Seeded scenario for the Case triage and AI–Human Agreement product demonstration."
        }
      },
      "metadata": {}
    },
    {
      "created_at": "2026-08-14T18:48:28.430434+00:00",
      "action": "linked",
      "actor": "",
      "changes": {},
      "metadata": {
        "relation": "alerts",
        "related_id": "45aa1bd2-fd89-4ffc-993d-81d6f606d7a4",
        "related_label": "alert_000009",
        "related_resource": "alerts"
      }
    },
    {
      "created_at": "2026-08-14T18:48:28.438766+00:00",
      "action": "linked",
      "actor": "",
      "changes": {},
      "metadata": {
        "relation": "alerts",
        "related_id": "d9531ea7-7efa-4ab3-b43f-bc69be825b41",
        "related_label": "alert_000010",
        "related_resource": "alerts"
      }
    }
  ]
}

=== 2. Ask the LLM for Knowledge search keywords ===
SystemMessage:
You are a SOC knowledge-retrieval keyword generator.

Your task is to read the Case JSON provided in the human message and output keywords for searching the internal Knowledge worksheet.

Keyword selection rules:

1. Output 3 to 8 high-value keywords when possible.
2. Prefer exact entities and identifiers from the Case, such as hostnames, IP addresses, usernames, email addresses, domains, URLs, file names, process names, cloud resource names, alert names, business system names, tactic names, technique names, and distinctive behavior phrases.
3. Include internal business or asset terms if they appear in the Case and may help retrieve asset profiles, ownership, whitelist context, honeypot context, test environment context, SOPs, or response guidance.
4. Prefer concise keywords or short phrases. Do not output long sentences.
5. Avoid generic words that are unlikely to retrieve useful knowledge, such as alert, case, security, event, suspicious, source, destination, user, host, process, or network unless they are part of a distinctive phrase.
6. Do not invent entities or keywords that are not grounded in the Case JSON.

Return only the structured output required by the schema.

Expected output format: a JSON object with a single key "keywords" whose value is an array of strings, e.g. {"keywords": ["hostname.example.com", "192.168.1.1", "Suspicious Login"]}. Do not return a bare array.


HumanMessage (JSON):
{
  "created_at": "2026-08-14T18:48:28.410451+00:00",
  "updated_at": "2026-08-14T18:48:28.413053+00:00",
  "title": "[DEMO COMPLEX LLM] Correlated identity and endpoint activity",
  "severity": "Critical",
  "impact": "High",
  "priority": "Critical",
  "confidence": "High",
  "description": "Correlate an unusual service-account sign-in with subsequent encoded PowerShell execution on a production finance server. Validate the attached source, identity, asset, and process context.",
  "category": "SIEM",
  "tags": [
    "case-triage-demo",
    "demo:complex-live-llm-enrichment",
    "identity",
    "endpoint",
    "correlated"
  ],
  "status": "New",
  "acknowledged_time": null,
  "assignee": "Alice Analyst",
  "closed_time": null,
  "verdict": "",
  "summary": "Awaiting enriched live Agentic SOC Case investigation.",
  "alerts": [
    {
      "created_at": "2026-08-14T18:48:28.428677+00:00",
      "updated_at": "2026-08-14T18:48:28.428684+00:00",
      "title": "Service account sign-in from an unfamiliar network",
      "severity": "High",
      "confidence": "High",
      "impact": "High",
      "disposition": "Unknown",
      "action": "Allowed",
      "labels": [
        "identity",
        "service-account",
        "new-country"
      ],
      "desc": "The finance automation account authenticated without its normal workload identity and enumerated privileged role assignments. MFA is not configured for this non-interactive account.",
      "first_seen_time": "2026-08-14T18:30:28.287850+00:00",
      "last_seen_time": "2026-08-14T18:33:28.287850+00:00",
      "rule_id": "DEMO-IAM-1042",
      "rule_name": "Unusual service-account interactive sign-in",
      "analytic_name": "Identity behavior analytics",
      "analytic_type": "Behavioral",
      "analytic_state": "Active",
      "analytic_desc": "",
      "product_category": "IAM",
      "product_vendor": "Demo Identity Cloud",
      "product_name": "Demo Identity Protection",
      "product_feature": "",
      "policy_name": "",
      "policy_type": "",
      "policy_desc": "",
      "risk_level": "High",
      "status": "New",
      "status_detail": "",
      "artifacts": [
        {
          "created_at": "2026-08-14T18:48:28.417174+00:00",
          "updated_at": "2026-08-14T18:48:28.417181+00:00",
          "name": "Source IP",
          "type": "IP Address",
          "role": "Actor",
          "value": "198.51.100.42",
          "enrichments": [
            {
              "created_at": "2026-08-14T18:48:28.445344+00:00",
              "updated_at": "2026-08-14T18:48:28.445349+00:00",
              "name": "Threat-intelligence reputation",
              "type": "Reputation",
              "provider": "MockTIProvider",
              "value": "198.51.100.42",
              "desc": "Observed in credential-stuffing activity by three tenants during the previous 24 hours; confidence high."
            }
          ]
        },
        {
          "created_at": "2026-08-14T18:48:28.419778+00:00",
          "updated_at": "2026-08-14T18:48:28.419783+00:00",
          "name": "Account Name",
          "type": "Account",
          "role": "Affected",
          "value": "svc-finance-automation",
          "enrichments": [
            {
              "created_at": "2026-08-14T18:48:28.448300+00:00",
              "updated_at": "2026-08-14T18:48:28.448305+00:00",
              "name": "Identity directory context",
              "type": "Identity",
              "provider": "Microsoft Entra ID",
              "value": "svc-finance-automation",
              "desc": "Non-interactive finance service account; owner is Finance Platform; no approved interactive sign-ins."
            }
          ]
        }
      ],
      "enrichments": []
    },
    {
      "created_at": "2026-08-14T18:48:28.437129+00:00",
      "updated_at": "2026-08-14T18:48:28.437135+00:00",
      "title": "Encoded PowerShell launched on finance application server",
      "severity": "Critical",
      "confidence": "High",
      "impact": "High",
      "disposition": "Unknown",
      "action": "Observed",
      "labels": [
        "endpoint",
        "powershell",
        "credential-access"
      ],
      "desc": "Eight minutes after the unusual sign-in, the same account opened a remote session to the finance application server and launched encoded PowerShell from a service process.",
      "first_seen_time": "2026-08-14T18:38:28.287850+00:00",
      "last_seen_time": "2026-08-14T18:40:28.287850+00:00",
      "rule_id": "DEMO-EDR-2048",
      "rule_name": "Encoded PowerShell from service process",
      "analytic_name": "Endpoint behavioral detection",
      "analytic_type": "Behavioral",
      "analytic_state": "Active",
      "analytic_desc": "",
      "product_category": "EDR",
      "product_vendor": "Demo Endpoint Security",
      "product_name": "Demo EDR",
      "product_feature": "",
      "policy_name": "",
      "policy_type": "",
      "policy_desc": "",
      "risk_level": "Critical",
      "status": "New",
      "status_detail": "",
      "artifacts": [
        {
          "created_at": "2026-08-14T18:48:28.419778+00:00",
          "updated_at": "2026-08-14T18:48:28.419783+00:00",
          "name": "Account Name",
          "type": "Account",
          "role": "Affected",
          "value": "svc-finance-automation",
          "enrichments": [
            {
              "created_at": "2026-08-14T18:48:28.448300+00:00",
              "updated_at": "2026-08-14T18:48:28.448305+00:00",
              "name": "Identity directory context",
              "type": "Identity",
              "provider": "Microsoft Entra ID",
              "value": "svc-finance-automation",
              "desc": "Non-interactive finance service account; owner is Finance Platform; no approved interactive sign-ins."
            }
          ]
        },
        {
          "created_at": "2026-08-14T18:48:28.422620+00:00",
          "updated_at": "2026-08-14T18:48:28.422626+00:00",
          "name": "Hostname",
          "type": "Hostname",
          "role": "Affected",
          "value": "fin-app-07.corp.example",
          "enrichments": [
            {
              "created_at": "2026-08-14T18:48:28.450987+00:00",
              "updated_at": "2026-08-14T18:48:28.450991+00:00",
              "name": "CMDB asset context",
              "type": "CMDB",
              "provider": "Internal CMDB",
              "value": "fin-app-07.corp.example",
              "desc": "Production finance application server processing payment files; business criticality is High."
            }
          ]
        },
        {
          "created_at": "2026-08-14T18:48:28.425332+00:00",
          "updated_at": "2026-08-14T18:48:28.425338+00:00",
          "name": "Process Command Line",
          "type": "Command Line",
          "role": "Related",
          "value": "powershell.exe -enc <redacted-demo-payload>",
          "enrichments": []
        }
      ],
      "enrichments": [
        {
          "created_at": "2026-08-14T18:48:28.453836+00:00",
          "updated_at": "2026-08-14T18:48:28.453840+00:00",
          "name": "EDR process-tree review",
          "type": "Detection",
          "provider": "Mock",
          "value": "encoded PowerShell",
          "desc": "No approved deployment job matched the process tree; outbound connection telemetry is unavailable."
        }
      ]
    }
  ],
  "enrichments": [],
  "comments": [],
  "audit_logs": [
    {
      "created_at": "2026-08-14T18:48:28.411217+00:00",
      "action": "create",
      "actor": "",
      "changes": {},
      "metadata": {}
    },
    {
      "created_at": "2026-08-14T18:48:28.414506+00:00",
      "action": "update",
      "actor": "",
      "changes": {
        "tags": {
          "to": [
            "case-triage-demo",
            "demo:complex-live-llm-enrichment",
            "identity",
            "endpoint",
            "correlated"
          ],
          "from": [
            "case-triage-demo",
            "demo:complex-live-llm-enrichment"
          ]
        },
        "summary": {
          "to": "Awaiting enriched live Agentic SOC Case investigation.",
          "from": "Prepared demo Case. Follow docs/demo/case-triage-and-ai-quality.md during the walkthrough."
        },
        "description": {
          "to": "Correlate an unusual service-account sign-in with subsequent encoded PowerShell execution on a production finance server. Validate the attached source, identity, asset, and process context.",
          "from": "Seeded scenario for the Case triage and AI–Human Agreement product demonstration."
        }
      },
      "metadata": {}
    },
    {
      "created_at": "2026-08-14T18:48:28.430434+00:00",
      "action": "linked",
      "actor": "",
      "changes": {},
      "metadata": {
        "relation": "alerts",
        "related_id": "45aa1bd2-fd89-4ffc-993d-81d6f606d7a4",
        "related_label": "alert_000009",
        "related_resource": "alerts"
      }
    },
    {
      "created_at": "2026-08-14T18:48:28.438766+00:00",
      "action": "linked",
      "actor": "",
      "changes": {},
      "metadata": {
        "relation": "alerts",
        "related_id": "d9531ea7-7efa-4ab3-b43f-bc69be825b41",
        "related_label": "alert_000010",
        "related_resource": "alerts"
      }
    }
  ]
}

Selected provider: Gemini Flash / gemini-2.5-flash [tag: structured_output]

Structured LLM response:
{
  "keywords": [
    "svc-finance-automation",
    "fin-app-07.corp.example",
    "198.51.100.42",
    "encoded PowerShell",
    "service-account sign-in",
    "finance server",
    "credential-stuffing",
    "Unusual service-account interactive sign-in"
  ]
}

=== 3. Search Knowledge in PostgreSQL ===
Keywords:
[
  "svc-finance-automation",
  "fin-app-07.corp.example",
  "198.51.100.42",
  "encoded PowerShell",
  "service-account sign-in",
  "finance server",
  "credential-stuffing",
  "Unusual service-account interactive sign-in"
]
Matching unexpired Knowledge records (maximum 10):
[]

=== 4. Ask the LLM for a structured InvestigationReport ===
SystemMessage:
You are a senior SOC / DFIR incident investigation analyst. Your task is to read the full structured Case data provided as input and produce an investigation report that strictly conforms to the `InvestigationReport` schema.

Your role is not to restate the raw fields, but to form a case judgment based on the evidence and explain:

- Whether this Case is closer to a real security incident, a suspicious event, a false positive, benign behavior, or insufficient data.
- What the attacker or actor did and what stage has been confirmed.
- What access, control capability, access scope, or business impact has been established.
- What the most important remediation actions are and what uncertainties still require additional evidence.

Input format:

The human message is a compact JSON object with three required top-level fields: `knowledge`, `case`, and `discussions`. An optional fourth field `user_input` may also be present.

- `case` is the primary investigation object.
- `knowledge.records` contains supplemental internal knowledge retrieved before analysis. Each record may include `id`, `knowledge_id`, `title`, `source`, `tags`, `expires_at`, and `body`. The `body` field may contain Markdown content; treat it as the content of that knowledge record.
- `knowledge.keywords` contains the search keywords generated from the current Case and used to retrieve the knowledge records.
- `discussions` is a list of analyst comments and replies on the case. Each item contains `message` (comment text), `created_at`, `created_by` (author name), `reply_to_author`, `mentions` (list of mentioned user names), and `attachments` (list of file attachments with `filename`, `ext`, `filesize`, `download_url`). Use discussions as supplementary context — they may contain analyst hypotheses, manually noted IOCs, false positive rationale, or operational notes not captured in structured fields.
- `user_input` (optional) is additional guidance provided by the analyst when triggering the playbook. If present, use it to inform your analysis — it may specify indicators of interest, supplementary context, or the analyst's initial hypothesis.

Knowledge may include internal context not directly visible in the Case, such as asset role, owner, business criticality, test IPs, honeypots, whitelists, known benign behavior, policy, SOP, or response guidance. Use relevant Knowledge when it helps interpret the Case or changes the assessment. Do not force unrelated Knowledge into the report.

Analysis principles:

1. Use only facts, fields, timestamps, entities, correlated objects, raw descriptions present in the input Case, and relevant internal Knowledge provided in `knowledge.records`. Do not fabricate evidence that does not exist.
2. Inference is permitted, but every inference must be grounded in explicit Case evidence or relevant internal Knowledge. When evidence is insufficient, lower `confidence` and document the gaps in `unknowns`.
3. Distinguish between "observed facts", "conclusions inferred from facts", and "unconfirmed parts". Do not present suspicions as established facts.
4. Synthesize the full Case context, including `alerts`, `artifacts`, `enrichments`, `tickets`, timestamp fields, status fields, textual descriptions, remediation records, and relevant internal Knowledge.
5. Multiple alerts may be repeated observations of the same behavior. Deduplicate before judging — do not treat repeated observations as independent attack steps.
6. Do not exaggerate to "fully compromised" when there is no evidence of successful execution, privilege gain, persistence, successful lateral movement, or data access.
7. Existing field values for `severity`, `impact`, `priority`, `confidence`, and `remediation` are for reference only. *You must re-evaluate based on the overall case evidence.*
8. The report should prioritize serving analysis and response — do not aim to fill every field. When a dimension lacks sufficient evidence, output an empty list or a more restrained conclusion.

Think in the following analysis order:

1. First, determine the nature of the case.
   Assess whether this looks more like a real intrusion, malicious attempt, account abuse, policy misconfiguration, cloud control-plane anomaly, email security incident, data access anomaly, benign business behavior, or a single suspicious data point.

2. Then, assess evidence strength.
   Prioritize finding evidence that forms a closed chain: same subject, same time window, same target, same behavioral path. Distinguish direct evidence from indirect indicators and evaluate whether a plausible benign explanation exists.

3. Then, reconstruct the behavioral chain.
   Output only attack stages supported by evidence. The chain does not need to be complete nor must it cover multiple MITRE ATT&CK stages. A single-step malicious activity, account abuse, policy modification, or false positive scenario is equally valid.

4. Then, assess privilege, scope, and impact.
   Describe what access or control capability the actor gained — e.g., successful login, command execution, mailbox rule modification, cloud API call, policy change, data read, persistence foothold, or lateral access capability.

5. Finally, provide remediation and evidence-gap recommendations.
   Prioritize risks that are still ongoing, can spread, can be reused, or can be exploited again. Clearly state which critical questions remain unconfirmed.

Field-level output requirements:

`verdict`

- Must clearly express the final nature of the case.
- Prefer: `True Positive`, `Suspicious`, `False Positive`, `Benign`, `Insufficient Data`.
- Use other enum values only when the evidence is very clear and better matches their specific semantics.

`severity`

- Reflects the technical and business severity of the incident itself, not the default alert level from the source.
- If a real intrusion, successful execution, privilege escalation, lateral movement, critical account abuse, or impact to core assets is confirmed, severity should generally not be below `High`.
- If the case is only a single anomaly, weak-evidence indicator, or more likely unconfirmed noise, `Low` or `Medium` is appropriate.

`impact`

- Reflects the actual or potential impact scope.
- Raise the impact level if critical business systems, identity systems, email systems, endpoint control, cloud control planes, sensitive data access, or sustained control capability are involved.

`priority`

- Reflects response urgency, not just technical severity.
- Raise priority if the risk is still ongoing, can continue to spread, can be reused, requires immediate containment, or involves exposure of high-value assets.

`confidence`

- `High`: Multiple sources of evidence corroborate each other; the key behavioral chain is closed and clear; little room for alternative explanations.
- `Medium`: The main conclusion holds, but critical gaps remain or some steps rely on inference.
- `Low`: Evidence is weak, ambiguous, or contextually insufficient; or a benign explanation still holds.

`digest`

- Write as a single high-information-density conclusive summary — not a field-by-field list.
- Recommended structure of 4 to 6 sentences:
  - Start by stating the verdict and nature of the case.
  - Summarize the confirmed core behaviors and the stage reached.
  - Describe the access, scope, or control capability established.
  - Describe affected assets, accounts, data, or business risks.
  - End with the strongest evidence and the key unconfirmed points.
- Must allow an analyst to quickly understand the core of the case without reading the raw Case.

`affected_assets`

- List only assets directly related to the case, directly operated on, clearly impacted, or supported by strong evidence.
- Use clear identifiers such as hostname, IP, username, email address, resource name, or file path.
- If an asset is only suspected to be affected, reflect "suspected" or "potential target" in the semantics — do not mix in large numbers of weakly related objects.

`evidence_findings`

- This is the most critical "evidence layer" of the report, carrying high-value findings that support the conclusions.
- Each finding should focus on one core subject or one key behavior — do not cram the entire case into a single finding.
- `evidence` should provide traceable clues such as timestamps, field names, object names, alert names, enrichment conclusions, remediation status, or raw observed phenomena.
- `conclusion` should explain what this finding means for the case judgment — e.g., supports real intrusion, supports false positive, supports privilege gain, supports need for additional evidence.
- Findings that support malicious conclusions and findings that support benign explanations may coexist. The overall judgment is reflected in `verdict` and `confidence`.

`attack_chain`

- Describe the confirmed behavioral chain using MITRE ATT&CK stages.
- Output only stages supported by evidence. Do not pad the chain to make it appear "complete".
- If the case is not a typical multi-stage attack, outputting a small number of steps or an empty list is acceptable.
- Each step's `description` should explain what happened at that stage and what evidence supports it.

`attack_timeline`

- Output key events in chronological order.
- Use precise timestamps when available; use relative order or approximate times when not.
- `evidence_field` should reference traceable log fields, alert fields, object names, or record sources.
- Keep only key time points that advance the case judgment. Do not repeat similar noise events.

`ioc_indicators`

- Include only IOCs that have investigation, blocking, hunting, or ongoing monitoring value.
- If the case has no clear, reusable IOCs, output an empty list.
- Do not misclassify generic descriptions, general symptoms, or non-unique text as IOCs.
- `context` should explain the role of the IOC in this case — e.g., download URL, C2, malicious login source, lateral movement command, dropped file.

`remediations`

- Output specific, actionable remediation recommendations ordered by response value.
- Prioritize containment, then eradication, recovery, validation, hardening, and ongoing monitoring.
- High-priority recommendations should focus on active risks, compromised accounts, persistence footholds, malicious connections, privilege abuse, and exposure of critical assets.
- Do not write vague recommendations such as "enhance monitoring" or "investigate further" without concrete actions.

`unknowns`

- Document the critical uncertainties, missing evidence, or unverified items that currently block definitive case classification.
- Focus on the most important gaps — e.g., whether login succeeded, whether execution succeeded, whether persistence was established, whether data exfiltration occurred, whether more assets are affected.
- Do not restate already-confirmed conclusions as unknowns, and do not write generic "requires further investigation" statements.

Output discipline:

1. Output must fully conform to the `InvestigationReport` structure. Do not add fields outside the schema.
2. All lists should be deduplicated, denoised, and retain only the highest-value content. Avoid large overlapping repetition between fields.
3. Empty lists are allowed, but fabricating content to fill the structure is not.
4. Except for `digest`, all other fields should be concise, specific, and traceable.
5. List length limits:

- `affected_assets`: maximum 5 entries.
- `evidence_findings`: maximum 5 entries.
- `attack_chain`: maximum 6 entries.
- `attack_timeline`: maximum 8 entries.
- `ioc_indicators`: maximum 10 entries.
- `remediations`: maximum 6 entries.
- `unknowns`: maximum 5 entries.

6. If multiple fields would express the same content, express it once in the most appropriate field and retain only necessary information in others. Avoid mechanical repetition.
7. When information is insufficient, prefer outputting a more restrained verdict, a lower confidence, and more explicit unknowns — rather than filling in unverified details.

HumanMessage (JSON):
{
  "case": {
    "created_at": "2026-08-14T18:48:28.410451+00:00",
    "updated_at": "2026-08-14T18:48:28.413053+00:00",
    "title": "[DEMO COMPLEX LLM] Correlated identity and endpoint activity",
    "severity": "Critical",
    "impact": "High",
    "priority": "Critical",
    "confidence": "High",
    "description": "Correlate an unusual service-account sign-in with subsequent encoded PowerShell execution on a production finance server. Validate the attached source, identity, asset, and process context.",
    "category": "SIEM",
    "tags": [
      "case-triage-demo",
      "demo:complex-live-llm-enrichment",
      "identity",
      "endpoint",
      "correlated"
    ],
    "status": "New",
    "acknowledged_time": null,
    "assignee": "Alice Analyst",
    "closed_time": null,
    "verdict": "",
    "summary": "Awaiting enriched live Agentic SOC Case investigation.",
    "alerts": [
      {
        "created_at": "2026-08-14T18:48:28.428677+00:00",
        "updated_at": "2026-08-14T18:48:28.428684+00:00",
        "title": "Service account sign-in from an unfamiliar network",
        "severity": "High",
        "confidence": "High",
        "impact": "High",
        "disposition": "Unknown",
        "action": "Allowed",
        "labels": [
          "identity",
          "service-account",
          "new-country"
        ],
        "desc": "The finance automation account authenticated without its normal workload identity and enumerated privileged role assignments. MFA is not configured for this non-interactive account.",
        "first_seen_time": "2026-08-14T18:30:28.287850+00:00",
        "last_seen_time": "2026-08-14T18:33:28.287850+00:00",
        "rule_id": "DEMO-IAM-1042",
        "rule_name": "Unusual service-account interactive sign-in",
        "analytic_name": "Identity behavior analytics",
        "analytic_type": "Behavioral",
        "analytic_state": "Active",
        "analytic_desc": "",
        "product_category": "IAM",
        "product_vendor": "Demo Identity Cloud",
        "product_name": "Demo Identity Protection",
        "product_feature": "",
        "policy_name": "",
        "policy_type": "",
        "policy_desc": "",
        "risk_level": "High",
        "status": "New",
        "status_detail": "",
        "artifacts": [
          {
            "created_at": "2026-08-14T18:48:28.417174+00:00",
            "updated_at": "2026-08-14T18:48:28.417181+00:00",
            "name": "Source IP",
            "type": "IP Address",
            "role": "Actor",
            "value": "198.51.100.42",
            "enrichments": [
              {
                "created_at": "2026-08-14T18:48:28.445344+00:00",
                "updated_at": "2026-08-14T18:48:28.445349+00:00",
                "name": "Threat-intelligence reputation",
                "type": "Reputation",
                "provider": "MockTIProvider",
                "value": "198.51.100.42",
                "desc": "Observed in credential-stuffing activity by three tenants during the previous 24 hours; confidence high."
              }
            ]
          },
          {
            "created_at": "2026-08-14T18:48:28.419778+00:00",
            "updated_at": "2026-08-14T18:48:28.419783+00:00",
            "name": "Account Name",
            "type": "Account",
            "role": "Affected",
            "value": "svc-finance-automation",
            "enrichments": [
              {
                "created_at": "2026-08-14T18:48:28.448300+00:00",
                "updated_at": "2026-08-14T18:48:28.448305+00:00",
                "name": "Identity directory context",
                "type": "Identity",
                "provider": "Microsoft Entra ID",
                "value": "svc-finance-automation",
                "desc": "Non-interactive finance service account; owner is Finance Platform; no approved interactive sign-ins."
              }
            ]
          }
        ],
        "enrichments": []
      },
      {
        "created_at": "2026-08-14T18:48:28.437129+00:00",
        "updated_at": "2026-08-14T18:48:28.437135+00:00",
        "title": "Encoded PowerShell launched on finance application server",
        "severity": "Critical",
        "confidence": "High",
        "impact": "High",
        "disposition": "Unknown",
        "action": "Observed",
        "labels": [
          "endpoint",
          "powershell",
          "credential-access"
        ],
        "desc": "Eight minutes after the unusual sign-in, the same account opened a remote session to the finance application server and launched encoded PowerShell from a service process.",
        "first_seen_time": "2026-08-14T18:38:28.287850+00:00",
        "last_seen_time": "2026-08-14T18:40:28.287850+00:00",
        "rule_id": "DEMO-EDR-2048",
        "rule_name": "Encoded PowerShell from service process",
        "analytic_name": "Endpoint behavioral detection",
        "analytic_type": "Behavioral",
        "analytic_state": "Active",
        "analytic_desc": "",
        "product_category": "EDR",
        "product_vendor": "Demo Endpoint Security",
        "product_name": "Demo EDR",
        "product_feature": "",
        "policy_name": "",
        "policy_type": "",
        "policy_desc": "",
        "risk_level": "Critical",
        "status": "New",
        "status_detail": "",
        "artifacts": [
          {
            "created_at": "2026-08-14T18:48:28.419778+00:00",
            "updated_at": "2026-08-14T18:48:28.419783+00:00",
            "name": "Account Name",
            "type": "Account",
            "role": "Affected",
            "value": "svc-finance-automation",
            "enrichments": [
              {
                "created_at": "2026-08-14T18:48:28.448300+00:00",
                "updated_at": "2026-08-14T18:48:28.448305+00:00",
                "name": "Identity directory context",
                "type": "Identity",
                "provider": "Microsoft Entra ID",
                "value": "svc-finance-automation",
                "desc": "Non-interactive finance service account; owner is Finance Platform; no approved interactive sign-ins."
              }
            ]
          },
          {
            "created_at": "2026-08-14T18:48:28.422620+00:00",
            "updated_at": "2026-08-14T18:48:28.422626+00:00",
            "name": "Hostname",
            "type": "Hostname",
            "role": "Affected",
            "value": "fin-app-07.corp.example",
            "enrichments": [
              {
                "created_at": "2026-08-14T18:48:28.450987+00:00",
                "updated_at": "2026-08-14T18:48:28.450991+00:00",
                "name": "CMDB asset context",
                "type": "CMDB",
                "provider": "Internal CMDB",
                "value": "fin-app-07.corp.example",
                "desc": "Production finance application server processing payment files; business criticality is High."
              }
            ]
          },
          {
            "created_at": "2026-08-14T18:48:28.425332+00:00",
            "updated_at": "2026-08-14T18:48:28.425338+00:00",
            "name": "Process Command Line",
            "type": "Command Line",
            "role": "Related",
            "value": "powershell.exe -enc <redacted-demo-payload>",
            "enrichments": []
          }
        ],
        "enrichments": [
          {
            "created_at": "2026-08-14T18:48:28.453836+00:00",
            "updated_at": "2026-08-14T18:48:28.453840+00:00",
            "name": "EDR process-tree review",
            "type": "Detection",
            "provider": "Mock",
            "value": "encoded PowerShell",
            "desc": "No approved deployment job matched the process tree; outbound connection telemetry is unavailable."
          }
        ]
      }
    ],
    "enrichments": [],
    "comments": [],
    "audit_logs": [
      {
        "created_at": "2026-08-14T18:48:28.411217+00:00",
        "action": "create",
        "actor": "",
        "changes": {},
        "metadata": {}
      },
      {
        "created_at": "2026-08-14T18:48:28.414506+00:00",
        "action": "update",
        "actor": "",
        "changes": {
          "tags": {
            "to": [
              "case-triage-demo",
              "demo:complex-live-llm-enrichment",
              "identity",
              "endpoint",
              "correlated"
            ],
            "from": [
              "case-triage-demo",
              "demo:complex-live-llm-enrichment"
            ]
          },
          "summary": {
            "to": "Awaiting enriched live Agentic SOC Case investigation.",
            "from": "Prepared demo Case. Follow docs/demo/case-triage-and-ai-quality.md during the walkthrough."
          },
          "description": {
            "to": "Correlate an unusual service-account sign-in with subsequent encoded PowerShell execution on a production finance server. Validate the attached source, identity, asset, and process context.",
            "from": "Seeded scenario for the Case triage and AI–Human Agreement product demonstration."
          }
        },
        "metadata": {}
      },
      {
        "created_at": "2026-08-14T18:48:28.430434+00:00",
        "action": "linked",
        "actor": "",
        "changes": {},
        "metadata": {
          "relation": "alerts",
          "related_id": "45aa1bd2-fd89-4ffc-993d-81d6f606d7a4",
          "related_label": "alert_000009",
          "related_resource": "alerts"
        }
      },
      {
        "created_at": "2026-08-14T18:48:28.438766+00:00",
        "action": "linked",
        "actor": "",
        "changes": {},
        "metadata": {
          "relation": "alerts",
          "related_id": "d9531ea7-7efa-4ab3-b43f-bc69be825b41",
          "related_label": "alert_000010",
          "related_resource": "alerts"
        }
      }
    ]
  },
  "knowledge": {
    "keywords": [
      "svc-finance-automation",
      "fin-app-07.corp.example",
      "198.51.100.42",
      "encoded PowerShell",
      "service-account sign-in",
      "finance server",
      "credential-stuffing",
      "Unusual service-account interactive sign-in"
    ],
    "records": []
  }
}

Structured LLM response:
{
  "verdict": "True Positive",
  "severity": "Critical",
  "impact": "High",
  "priority": "Critical",
  "confidence": "High",
  "digest": "This case is a True Positive, indicating a confirmed compromise of a critical service account and subsequent execution on a production finance server. An attacker successfully authenticated as 'svc-finance-automation' from a known malicious IP address, followed by the launch of encoded PowerShell on 'fin-app-07.corp.example'. This establishes initial access and execution capabilities on a high-value asset, posing a significant risk to financial operations. The strong correlation between the unusual sign-in and the malicious endpoint activity, coupled with threat intelligence and CMDB context, provides high confidence in this assessment. Key unknowns include the full payload of the PowerShell command and the extent of post-exploitation activities.",
  "affected_assets": [
    {
      "asset_type": "Account",
      "asset_value": "svc-finance-automation"
    },
    {
      "asset_type": "Hostname",
      "asset_value": "fin-app-07.corp.example"
    },
    {
      "asset_type": "IP Address",
      "asset_value": "198.51.100.42"
    }
  ],
  "evidence_findings": [
    {
      "title": "Unusual Service Account Sign-in",
      "finding_type": "Malicious Activity",
      "subject": "svc-finance-automation",
      "evidence": "Alert 'Service account sign-in from an unfamiliar network' for 'svc-finance-automation' from '198.51.100.42' at 2026-08-14T18:30:28Z. Identity context confirms it's a non-interactive finance service account with no approved interactive sign-ins.",
      "conclusion": "The service account 'svc-finance-automation' was used for an unauthorized interactive sign-in, indicating potential credential compromise."
    },
    {
      "title": "Malicious Source IP Reputation",
      "finding_type": "Threat Intelligence",
      "subject": "198.51.100.42",
      "evidence": "Threat intelligence enrichment for '198.51.100.42' indicates it was 'Observed in credential-stuffing activity by three tenants during the previous 24 hours; confidence high.'",
      "conclusion": "The source IP address is associated with known malicious activity, strengthening the malicious nature of the sign-in."
    },
    {
      "title": "Encoded PowerShell Execution on Critical Server",
      "finding_type": "Malicious Activity",
      "subject": "fin-app-07.corp.example",
      "evidence": "Alert 'Encoded PowerShell launched on finance application server' at 2026-08-14T18:38:28Z on 'fin-app-07.corp.example' by 'svc-finance-automation'. Command line: 'powershell.exe -enc <redacted-demo-payload>'. EDR review found no approved deployment job.",
      "conclusion": "Encoded PowerShell was executed on a critical production finance server, indicating successful command execution by the compromised service account."
    },
    {
      "title": "Correlation of Identity and Endpoint Activity",
      "finding_type": "Correlation",
      "subject": "svc-finance-automation, fin-app-07.corp.example",
      "evidence": "The unusual service account sign-in occurred at 18:30:28Z, followed by encoded PowerShell execution on the finance server at 18:38:28Z, both using the same 'svc-finance-automation' account.",
      "conclusion": "The identity and endpoint activities are strongly correlated, confirming a multi-stage attack where the compromised service account was used to gain execution on a critical asset."
    },
    {
      "title": "Criticality of Affected Asset",
      "finding_type": "Asset Context",
      "subject": "fin-app-07.corp.example",
      "evidence": "CMDB asset context for 'fin-app-07.corp.example' states: 'Production finance application server processing payment files; business criticality is High.'",
      "conclusion": "The compromise impacts a highly critical production finance server, elevating the overall business risk."
    }
  ],
  "attack_chain": [
    {
      "attack_stage": "Initial Access",
      "description": "An attacker gained initial access by compromising the credentials of the 'svc-finance-automation' service account and performing an interactive sign-in from a suspicious IP address (198.51.100.42), which is unusual for this non-interactive account."
    },
    {
      "attack_stage": "Execution",
      "description": "Following the successful sign-in, the compromised 'svc-finance-automation' account was used to open a remote session to 'fin-app-07.corp.example' and execute encoded PowerShell, confirming command execution capabilities on a critical production server."
    }
  ],
  "attack_timeline": [
    {
      "timestamp": "2026-08-14T18:30:28.287850+00:00",
      "attack_behavior": "Service account 'svc-finance-automation' signed in from unfamiliar network '198.51.100.42'.",
      "evidence_field": "alerts[0].first_seen_time"
    },
    {
      "timestamp": "2026-08-14T18:33:28.287850+00:00",
      "attack_behavior": "Last observed sign-in activity for 'svc-finance-automation' from '198.51.100.42'.",
      "evidence_field": "alerts[0].last_seen_time"
    },
    {
      "timestamp": "2026-08-14T18:38:28.287850+00:00",
      "attack_behavior": "Encoded PowerShell launched on 'fin-app-07.corp.example' by 'svc-finance-automation'.",
      "evidence_field": "alerts[1].first_seen_time"
    },
    {
      "timestamp": "2026-08-14T18:40:28.287850+00:00",
      "attack_behavior": "Last observed encoded PowerShell activity on 'fin-app-07.corp.example'.",
      "evidence_field": "alerts[1].last_seen_time"
    }
  ],
  "ioc_indicators": [
    {
      "indicator_type": "IP Address",
      "value": "198.51.100.42",
      "context": "Source IP for unauthorized service account sign-in and associated with credential stuffing."
    },
    {
      "indicator_type": "Account",
      "value": "svc-finance-automation",
      "context": "Compromised service account used for initial access and execution."
    },
    {
      "indicator_type": "Command Line",
      "value": "powershell.exe -enc <redacted-demo-payload>",
      "context": "Malicious encoded PowerShell command executed on the finance server."
    }
  ],
  "remediations": [
    {
      "action_type": "Containment",
      "description": "Immediately isolate 'fin-app-07.corp.example' from the network to prevent further compromise or lateral movement.",
      "priority": "High"
    },
    {
      "action_type": "Eradication",
      "description": "Force a password reset for the 'svc-finance-automation' account and review its permissions for least privilege.",
      "priority": "High"
    },
    {
      "action_type": "Hardening",
      "description": "Implement strict access controls for 'svc-finance-automation', ensuring it cannot perform interactive logins. Consider implementing MFA for all interactive service accounts if applicable.",
      "priority": "High"
    },
    {
      "action_type": "Investigation",
      "description": "Analyze the full encoded PowerShell payload to understand its capabilities and objectives. Investigate for persistence mechanisms, lateral movement, and data exfiltration attempts on 'fin-app-07.corp.example' and other connected systems.",
      "priority": "Medium"
    },
    {
      "action_type": "Hunting",
      "description": "Hunt for other instances of sign-ins from '198.51.100.42' or similar encoded PowerShell executions across the environment.",
      "priority": "Medium"
    }
  ],
  "unknowns": [
    "The full content and purpose of the encoded PowerShell payload.",
    "Whether persistence mechanisms were established on 'fin-app-07.corp.example' or other systems.",
    "Whether lateral movement occurred from 'fin-app-07.corp.example' to other critical assets.",
    "Whether any sensitive data was accessed or exfiltrated from the finance application server.",
    "The initial vector used to compromise the 'svc-finance-automation' account credentials."
  ]
}

=== 5. Stop without writing ===
The real worker now builds an AnalysisRecord and updates the Case AI fields, report, and job. This educational command deliberately leaves them unchanged.
```
