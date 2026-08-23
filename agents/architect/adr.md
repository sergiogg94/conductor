# ADR-{{NUMBER}}: {{DECISION_TITLE}}

**Date:** {{YYYY-MM-DD}}  
**Project:** {{PROJECT_NAME}}  
**Status:** 🟡 pending approval  
**Scope brief:** `docs/scopes/{{SCOPE_BRIEF_FILENAME}}`  
**Supersedes:** {{ADR-NUMBER or "N/A"}}  
**Superseded by:** N/A

---

## Context

<!--
One short paragraph. Describe the situation that makes this decision necessary.
Reference the scope brief. State any constraints that narrow the options.
Do not describe the decision itself here.
-->

{{CONTEXT}}

---

## Decision

<!--
One sentence. State clearly what has been decided.
Format: "We will use [X] for [Y]."
-->

{{DECISION_STATEMENT}}

---

## Options considered

### Option A — {{OPTION_A_NAME}}

{{OPTION_A_DESCRIPTION}}

**Pros:** {{OPTION_A_PROS}}  
**Cons:** {{OPTION_A_CONS}}

---

### Option B — {{OPTION_B_NAME}}

{{OPTION_B_DESCRIPTION}}

**Pros:** {{OPTION_B_PROS}}  
**Cons:** {{OPTION_B_CONS}}

---

### Option C — {{OPTION_C_NAME}} *(optional)*

{{OPTION_C_DESCRIPTION}}

**Pros:** {{OPTION_C_PROS}}  
**Cons:** {{OPTION_C_CONS}}

---

## Rationale

<!--
Why option [X] was chosen over the alternatives.
Must reference at least one acceptance criterion from the scope brief.
Must reference at least one project constraint (stack, scale, or goals).
3–5 sentences maximum.
-->

{{RATIONALE}}

---

## Implementation guidance

<!--
This section is the specification the developer agent will follow.
Be concrete. Names, types, paths, contracts. No pseudocode unless the algorithm is the decision.
-->

### Data model

<!--
Table or list of fields with type, constraints, and description.
Include DB table name and any indexes.
-->

| Field | Type | Constraints | Description |
|---|---|---|---|
| {{FIELD}} | {{TYPE}} | {{CONSTRAINTS}} | {{DESCRIPTION}} |

### API contract

<!--
One block per endpoint. Include method, path, request body shape, response body shape,
success status code, and all expected error codes with their meaning.
-->

#### `{{METHOD}} {{PATH}}`

**Request body:**
```json
{{REQUEST_BODY}}
```

**Response ({{SUCCESS_CODE}}):**
```json
{{RESPONSE_BODY}}
```

**Error cases:**
- `{{ERROR_CODE}}` — {{ERROR_MEANING}}

### File and folder structure

<!--
List only new files and folders. For modified files, note what changes.
-->

```
{{PROJECT_ROOT}}/
  {{NEW_FILE_OR_FOLDER}}    ← {{PURPOSE}}
```

### Naming conventions

<!--
Any naming rules that apply specifically to this decision.
If the project-wide conventions already cover this, write "Follow project conventions in README.md."
-->

- {{CONVENTION}}

### Guard rails for the developer

<!--
Explicit list of things the developer must NOT do.
These prevent common overengineering or scope creep during implementation.
-->

- Do not {{GUARD_RAIL_1}}
- Do not {{GUARD_RAIL_2}}

---

## Acceptance criteria satisfied

<!--
Copy the AC identifiers from the scope brief and confirm how this design satisfies each.
Format: AC-N → [how the design satisfies it]
-->

- AC-1 → {{HOW_SATISFIED}}
- AC-2 → {{HOW_SATISFIED}}

---

## Consequences

<!--
What becomes easier and what becomes harder as a result of this decision.
Honest assessment. Include technical debt introduced, if any.
-->

**Easier:** {{WHAT_BECOMES_EASIER}}  
**Harder:** {{WHAT_BECOMES_HARDER}}  
**Technical debt introduced:** {{DEBT or "None"}}

---

**Approved by:** ________________  
**Approval date:** ________________  
**Next agent:** developer
