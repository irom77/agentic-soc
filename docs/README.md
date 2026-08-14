# Project Documentation

This directory contains internal project documentation for development, demonstrations, release planning, and operations. It is separate from `asp-doc`, the public VitePress documentation repository.

## Directories

| Directory | Contents | Start here |
| --- | --- | --- |
| [`demo/`](demo/) | Repeatable Case triage, live LLM investigation, AlienVault OTX enrichment, screenshots, setup, reset, and presentation instructions. | [`demo/README.md`](demo/README.md) |
| [`research/`](research/) | Source-backed engineering research and implementation inventories used to prepare technical documentation. These notes capture code references, verified behavior, and known limitations. | [`research/technical-stack-inventory.md`](research/technical-stack-inventory.md) |
| [`specs/`](specs/) | Versioned product and engineering specifications. Each version folder defines its release scope and the requirements for planned features. | [`specs/v0.6.0/README.md`](specs/v0.6.0/README.md) |
| [`technical/`](technical/) | Current implementation details for the architecture, Django and PostgreSQL data model, Workers, Agentic Runtime, LLM processing, enrichment, and demo management commands. | [`technical/README.md`](technical/README.md) |

## Root-level documents

| Document | Purpose |
| --- | --- |
| [`faq.md`](faq.md) | Frequently asked questions about Workers, agents, and agentic platform terminology. |
| [`release-runbook.md`](release-runbook.md) | Agent and maintainer procedure for preparing, validating, committing, and publishing an ASP release. |

## Documentation boundaries

- Use `docs/technical/` for implementation details that must track this repository's code.
- Use `docs/specs/<version>/` for requirements and acceptance criteria that describe planned or release-scoped behavior.
- Use `docs/demo/` for reproducible presentation data and operator walkthroughs.
- Use `docs/research/` for evidence-gathering notes that support a later specification or technical document.
- Use `asp-doc` for public end-user and deployment documentation published through VitePress.
