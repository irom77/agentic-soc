# Case Analysis: case_000341

Generated with:

```bash
cd backend
uv run python manage.py explain_case_analysis case_000341 --invoke
```

The transcript below is a read-only walkthrough. The command invoked the configured LLM but did not save the returned report to the Case.

```
2026-08-15 07:36:18,545 INFO [httpx:1025] HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 200 OK"
2026-08-15 07:36:33,665 INFO [httpx:1025] HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 200 OK"

=== 1. Serialize the Case ===
The worker selects the Investigation profile and excludes raw/internal and previous AI fields.
{
  "created_at": "2026-08-14T18:48:28.456518+00:00",
  "updated_at": "2026-08-14T19:14:32.372467+00:00",
  "title": "[DEMO LIVE OTX] External indicator enrichment",
  "severity": "High",
  "impact": "High",
  "priority": "High",
  "confidence": "Medium",
  "description": "Investigate an unknown executable observed after external network activity. Collect current AlienVault OTX intelligence for the related indicators before requesting LLM analysis.",
  "category": "EDR",
  "tags": [
    "case-triage-demo",
    "demo:live-otx-enrichment",
    "endpoint",
    "threat-intel",
    "live-enrichment"
  ],
  "status": "New",
  "acknowledged_time": null,
  "assignee": "Alice Analyst",
  "closed_time": null,
  "verdict": "",
  "summary": "Awaiting live AlienVault OTX enrichment and subsequent LLM investigation.",
  "alerts": [
    {
      "created_at": "2026-08-14T18:48:28.466749+00:00",
      "updated_at": "2026-08-14T18:48:28.466754+00:00",
      "title": "Unknown executable observed after an external download",
      "severity": "High",
      "confidence": "Medium",
      "impact": "High",
      "disposition": "Unknown",
      "action": "Observed",
      "labels": [
        "endpoint",
        "download",
        "live-otx"
      ],
      "desc": "An endpoint observed an executable with an unknown local reputation after outbound activity. The indicators have not yet been checked against external threat intelligence.",
      "first_seen_time": "2026-08-14T18:36:28.287850+00:00",
      "last_seen_time": "2026-08-14T18:39:28.287850+00:00",
      "rule_id": "DEMO-OTX-3001",
      "rule_name": "Unknown executable following external download",
      "analytic_name": "Endpoint file and network correlation",
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
      "risk_level": "High",
      "status": "New",
      "status_detail": "",
      "artifacts": [
        {
          "created_at": "2026-08-14T18:48:28.461153+00:00",
          "updated_at": "2026-08-14T18:48:28.461158+00:00",
          "name": "Source IP",
          "type": "IP Address",
          "role": "Actor",
          "value": "8.8.8.8",
          "enrichments": [
            {
              "created_at": "2026-08-14T19:02:14.443173+00:00",
              "updated_at": "2026-08-14T19:04:58.956472+00:00",
              "name": "Threat Intelligence",
              "type": "Threat Intelligence",
              "provider": "AlienVaultOTX",
              "value": "8.8.8.8",
              "desc": "AlienVaultOTX assessed indicator as not malicious with low risk."
            }
          ]
        },
        {
          "created_at": "2026-08-14T18:48:28.462868+00:00",
          "updated_at": "2026-08-14T18:48:28.462872+00:00",
          "name": "Destination Domain",
          "type": "Hostname",
          "role": "Related",
          "value": "example.com",
          "enrichments": []
        },
        {
          "created_at": "2026-08-14T18:48:28.464568+00:00",
          "updated_at": "2026-08-14T18:48:28.464573+00:00",
          "name": "File Hash",
          "type": "Hash",
          "role": "Related",
          "value": "84c82835a5d21bbcf75a61706d8ab549",
          "enrichments": [
            {
              "created_at": "2026-08-14T19:02:13.787599+00:00",
              "updated_at": "2026-08-14T19:04:58.372336+00:00",
              "name": "Threat Intelligence",
              "type": "Threat Intelligence",
              "provider": "AlienVaultOTX",
              "value": "84c82835a5d21bbcf75a61706d8ab549",
              "desc": "AlienVaultOTX assessed indicator as malicious with high risk."
            }
          ]
        }
      ],
      "enrichments": []
    }
  ],
  "enrichments": [],
  "comments": [],
  "audit_logs": [
    {
      "created_at": "2026-08-14T18:48:28.457060+00:00",
      "action": "create",
      "actor": "",
      "changes": {},
      "metadata": {}
    },
    {
      "created_at": "2026-08-14T18:48:28.459699+00:00",
      "action": "update",
      "actor": "",
      "changes": {
        "tags": {
          "to": [
            "case-triage-demo",
            "demo:live-otx-enrichment",
            "endpoint",
            "threat-intel",
            "live-enrichment"
          ],
          "from": [
            "case-triage-demo",
            "demo:live-otx-enrichment"
          ]
        },
        "summary": {
          "to": "Awaiting live AlienVault OTX enrichment and subsequent LLM investigation.",
          "from": "Prepared demo Case. Follow docs/demo/case-triage-and-ai-quality.md during the walkthrough."
        },
        "description": {
          "to": "Investigate an unknown executable observed after external network activity. Collect current AlienVault OTX intelligence for the related indicators before requesting LLM analysis.",
          "from": "Seeded scenario for the Case triage and AI–Human Agreement product demonstration."
        }
      },
      "metadata": {}
    },
    {
      "created_at": "2026-08-14T18:48:28.467913+00:00",
      "action": "linked",
      "actor": "",
      "changes": {},
      "metadata": {
        "relation": "alerts",
        "related_id": "b4e50058-800d-4ec1-ba0e-c43bbc2e1842",
        "related_label": "alert_000011",
        "related_resource": "alerts"
      }
    },
    {
      "created_at": "2026-08-14T19:02:12.289792+00:00",
      "action": "linked",
      "actor": "",
      "changes": {},
      "metadata": {
        "relation": "playbooks",
        "related_id": "d88398c5-15a7-404a-b44e-4020828afab4",
        "related_label": "playbook_000001",
        "related_resource": "playbooks"
      }
    },
    {
      "created_at": "2026-08-14T19:04:54.932529+00:00",
      "action": "linked",
      "actor": "",
      "changes": {},
      "metadata": {
        "relation": "playbooks",
        "related_id": "e171499a-914a-4ad3-b15a-05cd82aa9040",
        "related_label": "playbook_000002",
        "related_resource": "playbooks"
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
  "created_at": "2026-08-14T18:48:28.456518+00:00",
  "updated_at": "2026-08-14T19:14:32.372467+00:00",
  "title": "[DEMO LIVE OTX] External indicator enrichment",
  "severity": "High",
  "impact": "High",
  "priority": "High",
  "confidence": "Medium",
  "description": "Investigate an unknown executable observed after external network activity. Collect current AlienVault OTX intelligence for the related indicators before requesting LLM analysis.",
  "category": "EDR",
  "tags": [
    "case-triage-demo",
    "demo:live-otx-enrichment",
    "endpoint",
    "threat-intel",
    "live-enrichment"
  ],
  "status": "New",
  "acknowledged_time": null,
  "assignee": "Alice Analyst",
  "closed_time": null,
  "verdict": "",
  "summary": "Awaiting live AlienVault OTX enrichment and subsequent LLM investigation.",
  "alerts": [
    {
      "created_at": "2026-08-14T18:48:28.466749+00:00",
      "updated_at": "2026-08-14T18:48:28.466754+00:00",
      "title": "Unknown executable observed after an external download",
      "severity": "High",
      "confidence": "Medium",
      "impact": "High",
      "disposition": "Unknown",
      "action": "Observed",
      "labels": [
        "endpoint",
        "download",
        "live-otx"
      ],
      "desc": "An endpoint observed an executable with an unknown local reputation after outbound activity. The indicators have not yet been checked against external threat intelligence.",
      "first_seen_time": "2026-08-14T18:36:28.287850+00:00",
      "last_seen_time": "2026-08-14T18:39:28.287850+00:00",
      "rule_id": "DEMO-OTX-3001",
      "rule_name": "Unknown executable following external download",
      "analytic_name": "Endpoint file and network correlation",
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
      "risk_level": "High",
      "status": "New",
      "status_detail": "",
      "artifacts": [
        {
          "created_at": "2026-08-14T18:48:28.461153+00:00",
          "updated_at": "2026-08-14T18:48:28.461158+00:00",
          "name": "Source IP",
          "type": "IP Address",
          "role": "Actor",
          "value": "8.8.8.8",
          "enrichments": [
            {
              "created_at": "2026-08-14T19:02:14.443173+00:00",
              "updated_at": "2026-08-14T19:04:58.956472+00:00",
              "name": "Threat Intelligence",
              "type": "Threat Intelligence",
              "provider": "AlienVaultOTX",
              "value": "8.8.8.8",
              "desc": "AlienVaultOTX assessed indicator as not malicious with low risk."
            }
          ]
        },
        {
          "created_at": "2026-08-14T18:48:28.462868+00:00",
          "updated_at": "2026-08-14T18:48:28.462872+00:00",
          "name": "Destination Domain",
          "type": "Hostname",
          "role": "Related",
          "value": "example.com",
          "enrichments": []
        },
        {
          "created_at": "2026-08-14T18:48:28.464568+00:00",
          "updated_at": "2026-08-14T18:48:28.464573+00:00",
          "name": "File Hash",
          "type": "Hash",
          "role": "Related",
          "value": "84c82835a5d21bbcf75a61706d8ab549",
          "enrichments": [
            {
              "created_at": "2026-08-14T19:02:13.787599+00:00",
              "updated_at": "2026-08-14T19:04:58.372336+00:00",
              "name": "Threat Intelligence",
              "type": "Threat Intelligence",
              "provider": "AlienVaultOTX",
              "value": "84c82835a5d21bbcf75a61706d8ab549",
              "desc": "AlienVaultOTX assessed indicator as malicious with high risk."
            }
          ]
        }
      ],
      "enrichments": []
    }
  ],
  "enrichments": [],
  "comments": [],
  "audit_logs": [
    {
      "created_at": "2026-08-14T18:48:28.457060+00:00",
      "action": "create",
      "actor": "",
      "changes": {},
      "metadata": {}
    },
    {
      "created_at": "2026-08-14T18:48:28.459699+00:00",
      "action": "update",
      "actor": "",
      "changes": {
        "tags": {
          "to": [
            "case-triage-demo",
            "demo:live-otx-enrichment",
            "endpoint",
            "threat-intel",
            "live-enrichment"
          ],
          "from": [
            "case-triage-demo",
            "demo:live-otx-enrichment"
          ]
        },
        "summary": {
          "to": "Awaiting live AlienVault OTX enrichment and subsequent LLM investigation.",
          "from": "Prepared demo Case. Follow docs/demo/case-triage-and-ai-quality.md during the walkthrough."
        },
        "description": {
          "to": "Investigate an unknown executable observed after external network activity. Collect current AlienVault OTX intelligence for the related indicators before requesting LLM analysis.",
          "from": "Seeded scenario for the Case triage and AI–Human Agreement product demonstration."
        }
      },
      "metadata": {}
    },
    {
      "created_at": "2026-08-14T18:48:28.467913+00:00",
      "action": "linked",
      "actor": "",
      "changes": {},
      "metadata": {
        "relation": "alerts",
        "related_id": "b4e50058-800d-4ec1-ba0e-c43bbc2e1842",
        "related_label": "alert_000011",
        "related_resource": "alerts"
      }
    },
    {
      "created_at": "2026-08-14T19:02:12.289792+00:00",
      "action": "linked",
      "actor": "",
      "changes": {},
      "metadata": {
        "relation": "playbooks",
        "related_id": "d88398c5-15a7-404a-b44e-4020828afab4",
        "related_label": "playbook_000001",
        "related_resource": "playbooks"
      }
    },
    {
      "created_at": "2026-08-14T19:04:54.932529+00:00",
      "action": "linked",
      "actor": "",
      "changes": {},
      "metadata": {
        "relation": "playbooks",
        "related_id": "e171499a-914a-4ad3-b15a-05cd82aa9040",
        "related_label": "playbook_000002",
        "related_resource": "playbooks"
      }
    }
  ]
}

Selected provider: Gemini Flash / gemini-2.5-flash [tag: structured_output]

Structured LLM response:
{
  "keywords": [
    "84c82835a5d21bbcf75a61706d8ab549",
    "AlienVault OTX",
    "Unknown executable",
    "external download",
    "example.com",
    "8.8.8.8",
    "EDR",
    "DEMO-OTX-3001"
  ]
}

=== 3. Search Knowledge in PostgreSQL ===
Keywords:
[
  "84c82835a5d21bbcf75a61706d8ab549",
  "AlienVault OTX",
  "Unknown executable",
  "external download",
  "example.com",
  "8.8.8.8",
  "EDR",
  "DEMO-OTX-3001"
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
    "created_at": "2026-08-14T18:48:28.456518+00:00",
    "updated_at": "2026-08-14T19:14:32.372467+00:00",
    "title": "[DEMO LIVE OTX] External indicator enrichment",
    "severity": "High",
    "impact": "High",
    "priority": "High",
    "confidence": "Medium",
    "description": "Investigate an unknown executable observed after external network activity. Collect current AlienVault OTX intelligence for the related indicators before requesting LLM analysis.",
    "category": "EDR",
    "tags": [
      "case-triage-demo",
      "demo:live-otx-enrichment",
      "endpoint",
      "threat-intel",
      "live-enrichment"
    ],
    "status": "New",
    "acknowledged_time": null,
    "assignee": "Alice Analyst",
    "closed_time": null,
    "verdict": "",
    "summary": "Awaiting live AlienVault OTX enrichment and subsequent LLM investigation.",
    "alerts": [
      {
        "created_at": "2026-08-14T18:48:28.466749+00:00",
        "updated_at": "2026-08-14T18:48:28.466754+00:00",
        "title": "Unknown executable observed after an external download",
        "severity": "High",
        "confidence": "Medium",
        "impact": "High",
        "disposition": "Unknown",
        "action": "Observed",
        "labels": [
          "endpoint",
          "download",
          "live-otx"
        ],
        "desc": "An endpoint observed an executable with an unknown local reputation after outbound activity. The indicators have not yet been checked against external threat intelligence.",
        "first_seen_time": "2026-08-14T18:36:28.287850+00:00",
        "last_seen_time": "2026-08-14T18:39:28.287850+00:00",
        "rule_id": "DEMO-OTX-3001",
        "rule_name": "Unknown executable following external download",
        "analytic_name": "Endpoint file and network correlation",
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
        "risk_level": "High",
        "status": "New",
        "status_detail": "",
        "artifacts": [
          {
            "created_at": "2026-08-14T18:48:28.461153+00:00",
            "updated_at": "2026-08-14T18:48:28.461158+00:00",
            "name": "Source IP",
            "type": "IP Address",
            "role": "Actor",
            "value": "8.8.8.8",
            "enrichments": [
              {
                "created_at": "2026-08-14T19:02:14.443173+00:00",
                "updated_at": "2026-08-14T19:04:58.956472+00:00",
                "name": "Threat Intelligence",
                "type": "Threat Intelligence",
                "provider": "AlienVaultOTX",
                "value": "8.8.8.8",
                "desc": "AlienVaultOTX assessed indicator as not malicious with low risk."
              }
            ]
          },
          {
            "created_at": "2026-08-14T18:48:28.462868+00:00",
            "updated_at": "2026-08-14T18:48:28.462872+00:00",
            "name": "Destination Domain",
            "type": "Hostname",
            "role": "Related",
            "value": "example.com",
            "enrichments": []
          },
          {
            "created_at": "2026-08-14T18:48:28.464568+00:00",
            "updated_at": "2026-08-14T18:48:28.464573+00:00",
            "name": "File Hash",
            "type": "Hash",
            "role": "Related",
            "value": "84c82835a5d21bbcf75a61706d8ab549",
            "enrichments": [
              {
                "created_at": "2026-08-14T19:02:13.787599+00:00",
                "updated_at": "2026-08-14T19:04:58.372336+00:00",
                "name": "Threat Intelligence",
                "type": "Threat Intelligence",
                "provider": "AlienVaultOTX",
                "value": "84c82835a5d21bbcf75a61706d8ab549",
                "desc": "AlienVaultOTX assessed indicator as malicious with high risk."
              }
            ]
          }
        ],
        "enrichments": []
      }
    ],
    "enrichments": [],
    "comments": [],
    "audit_logs": [
      {
        "created_at": "2026-08-14T18:48:28.457060+00:00",
        "action": "create",
        "actor": "",
        "changes": {},
        "metadata": {}
      },
      {
        "created_at": "2026-08-14T18:48:28.459699+00:00",
        "action": "update",
        "actor": "",
        "changes": {
          "tags": {
            "to": [
              "case-triage-demo",
              "demo:live-otx-enrichment",
              "endpoint",
              "threat-intel",
              "live-enrichment"
            ],
            "from": [
              "case-triage-demo",
              "demo:live-otx-enrichment"
            ]
          },
          "summary": {
            "to": "Awaiting live AlienVault OTX enrichment and subsequent LLM investigation.",
            "from": "Prepared demo Case. Follow docs/demo/case-triage-and-ai-quality.md during the walkthrough."
          },
          "description": {
            "to": "Investigate an unknown executable observed after external network activity. Collect current AlienVault OTX intelligence for the related indicators before requesting LLM analysis.",
            "from": "Seeded scenario for the Case triage and AI–Human Agreement product demonstration."
          }
        },
        "metadata": {}
      },
      {
        "created_at": "2026-08-14T18:48:28.467913+00:00",
        "action": "linked",
        "actor": "",
        "changes": {},
        "metadata": {
          "relation": "alerts",
          "related_id": "b4e50058-800d-4ec1-ba0e-c43bbc2e1842",
          "related_label": "alert_000011",
          "related_resource": "alerts"
        }
      },
      {
        "created_at": "2026-08-14T19:02:12.289792+00:00",
        "action": "linked",
        "actor": "",
        "changes": {},
        "metadata": {
          "relation": "playbooks",
          "related_id": "d88398c5-15a7-404a-b44e-4020828afab4",
          "related_label": "playbook_000001",
          "related_resource": "playbooks"
        }
      },
      {
        "created_at": "2026-08-14T19:04:54.932529+00:00",
        "action": "linked",
        "actor": "",
        "changes": {},
        "metadata": {
          "relation": "playbooks",
          "related_id": "e171499a-914a-4ad3-b15a-05cd82aa9040",
          "related_label": "playbook_000002",
          "related_resource": "playbooks"
        }
      }
    ]
  },
  "knowledge": {
    "keywords": [
      "84c82835a5d21bbcf75a61706d8ab549",
      "AlienVault OTX",
      "Unknown executable",
      "external download",
      "example.com",
      "8.8.8.8",
      "EDR",
      "DEMO-OTX-3001"
    ],
    "records": []
  }
}

Structured LLM response:
{
  "verdict": "True Positive",
  "severity": "High",
  "impact": "High",
  "priority": "High",
  "confidence": "High",
  "digest": "This case is a True Positive security incident involving the observation and execution of a malicious executable on an endpoint. The file hash `84c82835a5d21bbcf75a61706d8ab549` was confirmed as malicious with high risk by AlienVault OTX. The executable was observed after external network activity, indicating a potential initial access vector via download. While the specific malicious download source is not definitively identified among the listed network indicators, the confirmed malicious nature of the executable poses a significant risk of endpoint compromise, requiring immediate containment and investigation.",
  "affected_assets": [
    {
      "asset_type": "Endpoint",
      "asset_value": "Unknown Endpoint"
    }
  ],
  "evidence_findings": [
    {
      "title": "Malicious Executable Confirmed by Threat Intelligence",
      "finding_type": "Threat Intelligence Match",
      "subject": "File Hash",
      "evidence": "AlienVaultOTX enrichment for hash `84c82835a5d21bbcf75a61706d8ab549` assessed as 'malicious with high risk'.",
      "conclusion": "The executable observed on the endpoint is confirmed to be malicious, indicating a successful compromise or execution of malware."
    },
    {
      "title": "Unknown Executable Observed on Endpoint",
      "finding_type": "Behavioral Alert",
      "subject": "Endpoint Activity",
      "evidence": "Alert 'Unknown executable observed after an external download' (rule ID: DEMO-OTX-3001) triggered, indicating an executable with unknown local reputation was observed.",
      "conclusion": "An unauthorized and potentially harmful executable was present and active on an internal endpoint."
    },
    {
      "title": "Benign Network Indicators",
      "finding_type": "Threat Intelligence Match",
      "subject": "Network Indicators",
      "evidence": "AlienVaultOTX enrichment for IP `8.8.8.8` assessed as 'not malicious with low risk'. The domain `example.com` is a reserved domain.",
      "conclusion": "The explicitly listed network indicators (`8.8.8.8`, `example.com`) associated with the 'external download' are not malicious, suggesting the actual malicious download source is either unlisted or the network activity was unrelated to the malicious download."
    }
  ],
  "attack_chain": [
    {
      "attack_stage": "Initial Access",
      "description": "An external download event preceded the observation of a malicious executable on an endpoint. While the specific malicious source is unclear, the download facilitated the introduction of the malware."
    },
    {
      "attack_stage": "Execution",
      "description": "An unknown executable, later confirmed malicious by threat intelligence, was observed running on an endpoint, indicating successful execution of the malware."
    }
  ],
  "attack_timeline": [
    {
      "timestamp": "2026-08-14T18:36:28.287850+00:00",
      "attack_behavior": "First observation of unknown executable and associated external network activity.",
      "evidence_field": "alerts[0].first_seen_time"
    },
    {
      "timestamp": "2026-08-14T18:39:28.287850+00:00",
      "attack_behavior": "Last observation of unknown executable and associated external network activity.",
      "evidence_field": "alerts[0].last_seen_time"
    },
    {
      "timestamp": "2026-08-14T19:04:58.372336+00:00",
      "attack_behavior": "File hash `84c82835a5d21bbcf75a61706d8ab549` confirmed malicious by AlienVault OTX.",
      "evidence_field": "alerts[0].artifacts[2].enrichments[0].updated_at"
    }
  ],
  "ioc_indicators": [
    {
      "indicator_type": "File Hash (MD5)",
      "value": "84c82835a5d21bbcf75a61706d8ab549",
      "context": "Malicious executable observed on endpoint, confirmed by AlienVault OTX."
    }
  ],
  "remediations": [
    {
      "action_type": "Containment",
      "description": "Immediately isolate the affected endpoint to prevent further compromise or lateral movement.",
      "priority": "High"
    },
    {
      "action_type": "Eradication",
      "description": "Initiate a full forensic investigation on the isolated endpoint to identify the source of the download, scope of compromise, and remove all malicious artifacts.",
      "priority": "High"
    },
    {
      "action_type": "Blocking",
      "description": "Add the malicious file hash `84c82835a5d21bbcf75a61706d8ab549` to all endpoint protection and network security solutions to prevent future execution or spread.",
      "priority": "High"
    },
    {
      "action_type": "Hunting",
      "description": "Perform a threat hunt across all endpoints and network logs for the malicious file hash and any related indicators to identify other potentially affected systems.",
      "priority": "Medium"
    }
  ],
  "unknowns": [
    "The specific identity (hostname, IP) of the affected endpoint is not provided.",
    "The exact source (URL/IP) of the malicious download is not identified, as the listed network indicators are benign.",
    "Whether the malicious executable established persistence mechanisms on the endpoint.",
    "The full scope of compromise, including potential lateral movement or data exfiltration."
  ]
}

=== 5. Stop without writing ===
The real worker now builds an AnalysisRecord and updates the Case AI fields, report, and job. This educational command deliberately leaves them unchanged.
```
