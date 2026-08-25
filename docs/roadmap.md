# Roadmap

## Purpose

This document separates what the MVP includes from what is deliberately deferred. Post-MVP ideas live here, never mixed into current implementation.

## MVP Scope (complete)

The MVP delivers one usable, installable workflow:

- [x] conceptual model and agent catalog documentation
- [x] framework configuration template (`templates/project/conductor.yaml`)
- [x] shared contracts: `core-principles.md`, `artifact-contracts.md`, `github-projects-policy.md`
- [x] base agent generation template (`agents/shared/agent-template.md`)
- [x] 1 primary agent (`orchestrator`) + 9 subagents as OpenCode agent files
- [x] 8 artifact templates under `templates/artifacts/`
- [x] 9 OpenCode commands wired to their agents
- [x] consumer project templates: opencode.json, docs scaffolds, issue/PR templates, CI + review workflows
- [x] bootstrap, sync, and validation scripts

The MVP success criterion: a consumer project can be bootstrapped and run a full human-gated pipeline — `/discover` through `/docs delivery` — with every stage producing its contracted artifact.

## Explicitly Postponed

Do not build any of these while the MVP is being proven on real projects:

- automatic model routing — agents carry explicit `model:` values; tier resolution stays manual
- bidirectional sync between artifacts and GitHub Projects
- prompt evaluations / regression harness for agent behavior
- live GitHub MCP integration code — board operations remain human-applied suggestions
- multiple project types or presets beyond the single generic scaffold
- metrics, dashboards, or usage telemetry

## Future Directions

Candidates after the MVP proves itself in daily use:

1. **Live board integration** — apply suggested transitions through the GitHub MCP Server under the existing policy's permission rules
2. **Model tier resolver** — map `model_tier` from `conductor.yaml` to concrete provider models per project
3. **Framework test suite** — automated tests for bootstrap/sync scripts and template integrity
4. **Examples** — a sample consumer repository demonstrating a full pipeline run
5. **Multiple scaffolds** — project templates per stack (python-api, node-web, etc.) selected at bootstrap
6. **Evaluation fixtures** — recorded artifact sets for testing agent changes without live projects
7. **AGENTS.md conventions** — repository-level instructions file for consumer projects

Each of these should graduate into the checklist only when there is evidence from real usage that it is needed.
