# ASP v0.6.0 specification index

This directory is the cross-session implementation source of truth for v0.6.0. Completed feature discussions are frozen as implementation-level specs. Unfinished topics only record TODOs and open questions; do not treat recommendations in TODOs as confirmed requirements.

## Confirmed specs

| Document | Status | Contents |
| --- | --- | --- |
| [00-release-scope.md](00-release-scope.md) | Confirmed | Release goals, deployment boundaries, compatibility matrix, capacity, permissions, and exclusions |
| [01-bulk-case-triage.md](01-bulk-case-triage.md) | Confirmed | Bulk Case triage, shared state machine, notifications, and audit |
| [02-case-relationships.md](02-case-relationships.md) | Confirmed | Weak Case relationships, relationship constraints, Artifact candidates, and Agent reads |
| [03-playbook-execution.md](03-playbook-execution.md) | Confirmed | Playbook Run, structured Stage, cancellation, retries, and Worker semantics |
| [05-worker-health.md](05-worker-health.md) | Confirmed | Redis heartbeats, Worker state, and Admin API |
| [07-sla-management.md](07-sla-management.md) | Confirmed | TTD/TTA/TTR deadlines, Severity policy, notifications, and Dashboard compliance rates |
| [08-ai-quality-evaluation.md](08-ai-quality-evaluation.md) | Confirmed | AI–Human Agreement, coverage, confusion matrix, and sample drilldown |

## Open items

[TODO-remaining-domains.md](TODO-remaining-domains.md) only records version acceptance. All v0.6.0 domains are either confirmed or explicitly excluded.

## Implementation order

1. Finish the Case state machine first, then implement bulk triage and Case Relationships.
2. Complete Playbook Run/Stage.
3. Build the shared Worker Health infrastructure and connect the five Worker types.
4. Complete SLA and AI Quality.
5. Finish the remaining v0.6.0 acceptance specs.

## Spec usage rules

- `Confirmed` means the product decision is finalized and implementation must not change the behavior.
- Model names and URLs in the spec are target design. If there is a naming conflict with existing code, equivalent adjustments are allowed, but external behavior must remain the same.
- Each feature must cover backend, frontend, permissions, audit, migrations, and failure behavior.
- v0.6.0 allows breaking API changes and does not need to preserve compatibility with the old CLI or plugins.
- Do not copy this directory into `asp-doc` as user-facing documentation; user docs should be written separately after the implementation stabilizes.
