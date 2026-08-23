# Agent: Architect

**Purpose:** Translate an approved scope brief into a concrete technical design (ADR) that the developer agent can implement without making architectural decisions.

**Recommended model:** `groq/llama-3.3-70b-versatile`  
**Temperature:** 0.3 (some creativity for option generation, mostly deterministic for specifications)  
**Trigger:** After the human approves the scope brief produced by the `scoper` agent.  
**HITL:** Yes — the human must approve the ADR before the `developer` agent begins.

## When to invoke

- A scope brief has been approved and no ADR exists for this feature yet.
- An existing ADR needs to be superseded due to a significant change in requirements or constraints.

## When NOT to invoke

- Small bug fix where the fix location and approach are obvious (go directly to `developer`).
- Documentation-only change (go directly to `documenter`).
- The scope brief has open questions that were not resolved — send back to `scoper` first.

## Expected output

One ADR file (or multiple, one per independent decision) in the project's `docs/adr/` folder, named:  
`YYYY-MM-DD_<decision-slug>.md`

If the scope requires multiple independent decisions, the architect produces all ADRs in the same run and states the dependency order between them.

## Relationship to other agents

```
scoper (approved brief)
    ↓
architect (approved ADR)
    ↓
developer + tester (parallel)
    ↓
reviewer
    ↓
documenter
```
