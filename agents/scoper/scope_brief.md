# Scope brief: {{FEATURE_NAME}}

**Date:** {{YYYY-MM-DD}}  
**Project:** {{PROJECT_NAME}}  
**Requested by:** human  
**Status:** 🟡 pending approval

---

## Problem

<!--
One or two sentences. Describe what is broken or missing, from the user's or system's perspective.
Do not describe the solution here. Only the problem.
-->

{{PROBLEM_STATEMENT}}

---

## Objective

<!--
One sentence. The concrete outcome sought by completing this feature.
Suggested format: "Allow [who] to [do what] so that [why]."
-->

{{OBJECTIVE}}

---

## In scope

<!--
Numbered list. Only what will be built in this iteration.
Be specific: not "recipe CRUD" but "POST /recipes endpoint that persists name, ingredients, and instructions".
-->

1. {{IN_SCOPE_1}}
2. {{IN_SCOPE_2}}

---

## Out of scope

<!--
Just as important as the above. List what will explicitly NOT be done.
Include things the human might assume are covered but are not.
-->

- {{OUT_OF_SCOPE_1}}
- {{OUT_OF_SCOPE_2}}

---

## Dependencies

<!--
Only real, verifiable dependencies: existing modules being touched, data that must exist,
required external services. If there are none, write "None."
-->

- {{DEPENDENCY_1}}

---

## Identified risks

<!--
Only concrete, non-hypothetical risks. If there are none, write "None identified."
Format: [risk] → [suggested mitigation]
-->

- {{RISK_1}} → {{MITIGATION_1}}

---

## Acceptance criteria

<!--
Strict format: Given / When / Then.
Must be unambiguously verifiable by the tester agent.
Minimum 2, maximum 6. If you need more than 6, the scope is too large.
-->

**AC-1**  
Given {{context}}  
When {{action}}  
Then {{expected_result}}

**AC-2**  
Given {{context}}  
When {{action}}  
Then {{expected_result}}

---

## Open questions

<!--
Only if there are decisions the human must make before the architect can work.
If there are none, remove this section.
Maximum 3 questions. One is ideal.
-->

1. {{OPEN_QUESTION}}

---

## Notes for the architect

<!--
Minimal useful technical context: decisions already made in the project that the architect must respect,
existing code conventions, known infrastructure constraints.
This is not a technical design. It is context so the architect does not start from scratch.
If there are no relevant notes, remove this section.
-->

- {{ARCH_NOTE_1}}

---

**Approved by:** ________________  
**Approval date:** ________________  
**Next agent:** architect
