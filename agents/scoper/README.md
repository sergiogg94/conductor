# Agent: Scoper

**Purpose:** Produce a clear, well-scoped `scope_brief.md` before any other agent works on a feature or change.

**Recommended model:** `gemini-2.0-flash` (Google AI Studio — long context to read the full repo)  
**Temperature:** 0.2 (deterministic responses, no unnecessary creativity)  
**Trigger:** Always the first agent to run for any new feature or significant change.  
**HITL:** Yes — the human must approve the scope brief before continuing to the `architect` agent.

## When to invoke

- New feature or user story
- Change that affects more than one module
- Any ambiguous request the human described in natural language

## When NOT to invoke

- Small bug fix with a clear cause (go directly to `developer`)
- Documentation-only change (go directly to `documenter`)
- Internal refactor with no behaviour change

## Expected output

A `scope_brief.md` file in the project's `docs/scopes/` folder, named:  
`YYYY-MM-DD_<feature-slug>.md`
