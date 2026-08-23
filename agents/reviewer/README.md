# Agent: Reviewer

**Purpose:** Evaluate code produced by the developer agent against the approved ADR and scope brief, and produce a structured review report for the human to act on.

**Recommended model:** `gemini-2.0-flash` (Google AI Studio — long context to read entire files, not just diffs)  
**Temperature:** 0.1 (as deterministic as possible; reviews must be consistent)  
**Trigger:** After the developer agent commits to its branch and the tester agent has run.  
**HITL:** Yes — the human reads the report and decides to merge, request changes, or escalate.

## When to invoke

- Developer agent has completed its implementation on a feature branch.
- Tester agent output is available (pass the test report as context).
- Before any merge to the main branch.

## When NOT to invoke

- The developer agent's branch has not been committed yet.
- The tester agent has not run (tests are required context for a complete review).

## Expected output

A review report file in the project's `docs/reviews/` folder, named:  
`YYYY-MM-DD_<feature-slug>_review.md`

## Relationship to other agents

```
developer + tester (parallel)
    ↓
reviewer
    ↓  (if ✅ Approved)
documenter + human merges PR
    ↓  (if 🔄 Changes requested)
developer (addresses findings)
    ↓  (if ⛔ Escalate)
human + architect (architectural decision needed)
```

## Notes on model choice

The reviewer reads entire files — not just diffs — to catch issues that only appear in context. Gemini 2.0 Flash's large context window (1M tokens) makes it well suited for this. For very large codebases, pass the most relevant files explicitly rather than the entire repo.
