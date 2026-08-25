# Artifact Model

## Purpose

This document describes the artifact system of `conductor`: what each workflow stage produces, who owns it, where it lives, and how it hands off to the next stage.

Artifacts are the backbone of traceability. Agents collaborate through durable documents, never through free-form conversation chains.

The complete output contract for every artifact — required sections, completion criteria, downstream consumers — is defined in `agents/shared/artifact-contracts.md`. This document maps the system; that document specifies it.

## Artifact Catalog

| # | Stage | Owner agent | Command | Artifact | Template | Destination |
|---|---|---|---|---|---|---|
| 1 | Discovery | discovery | `/discover` | Discovery artifact | `templates/artifacts/discovery.md` | `docs/discovery.md` |
| 2 | Scoping | scopper | `/scope` | Requirements artifact | `templates/artifacts/requirements.md` | `docs/requirements.md` |
| 3 | Planning | planner | `/plan` | Implementation plan | `templates/artifacts/implementation-plan.md` | `docs/implementation-plan.md` |
| 4 | Architecture | architect | `/architect` | ADR(s), one per decision | `templates/artifacts/adr.md` | `docs/adr/YYYY-MM-DD_<slug>.md` |
| 5 | Implementation | developer | `/implement` | Code changes + implementation notes | `templates/artifacts/implementation-notes.md` | feature branch + `docs/notes/YYYY-MM-DD_<slug>.md` |
| 6 | Validation | tester | `/test` | Test report | `templates/artifacts/test-report.md` | `docs/tests/YYYY-MM-DD_<slug>.md` |
| 7 | Review | reviewer | `/review` | Review report | `templates/artifacts/review-report.md` | `docs/reviews/YYYY-MM-DD_<slug>_review.md` |
| 8 | Delivery | documenter | `/docs delivery` | Delivery checklist | `templates/artifacts/delivery-checklist.md` | `docs/delivery-checklist.md` |

The developer's primary artifact is production code itself; implementation notes are its lightweight companion document so humans and downstream agents have an entry point into the change.

## Status Lifecycle

Every reviewable artifact carries an explicit status in its header:

1. **🟡 pending approval** — produced, awaiting the human gate
2. **✅ approved** — the human approved it; only now is it valid input for the next stage

An unapproved artifact is never input for the next stage. Silence is not consent. Agents validate upstream approval before working; if it is missing, they stop and say so.

## Handoff Expectations

The default pipeline and its human gates:

```text
/discover   →  Discovery            🟡 → ✅ human approves
/scope      →  Requirements         🟡 → ✅ human approves
/plan       →  Implementation plan  🟡 → ✅ human approves
/architect  →  ADR(s)               🟡 → ✅ human approves
/implement  →  Code + notes         (feature branch, committed)
/test       →  Test report          factual, no approval needed
/review     →  Review report        verdict ✅ / 🔄 / ⛔ → human decides merge
/docs       →  Delivery checklist   🟡 → ✅ human accepts
```

Rules that make handoffs clean:

- each stage consumes exactly one upstream artifact family and produces exactly its own
- every artifact is understandable without access to the conversation that produced it
- tasks marked `[requires architecture]` in the plan block implementation until their ADR is approved
- the reviewer requires the test report as mandatory input context
- the delivery checklist consolidates requirements, notes, test report, and review report — if any are missing or unapproved, the documenter stops

## Where Artifacts Live

Artifact destinations are configured per project in `conductor.yaml` under `artifacts`. The defaults match the destinations above, plus directory-based outputs (`adr_directory`, `review_reports`, `test_reports`, `implementation_notes`).

Consumer projects receive empty scaffolds at these locations during bootstrap; agents replace scaffold content when they produce real artifacts.
