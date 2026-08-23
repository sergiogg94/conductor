# Review report: {{FEATURE_NAME}}

**Date:** {{YYYY-MM-DD}}  
**Project:** {{PROJECT_NAME}}  
**Branch reviewed:** `{{BRANCH_NAME}}`  
**Scope brief:** `docs/scopes/{{SCOPE_BRIEF_FILENAME}}`  
**ADR(s):** `docs/adr/{{ADR_FILENAME}}`  
**Tester output:** `docs/reviews/{{TEST_REPORT_FILENAME}}` *(or "not available")*  
**Reviewer agent model:** {{MODEL_NAME}}

---

## Summary

| Category | Blocking 🔴 | Non-blocking 🟡 | Positive 🟢 |
|---|---|---|---|
| ADR conformance | {{N}} | {{N}} | {{N}} |
| Acceptance criteria | {{N}} | {{N}} | {{N}} |
| Code quality | {{N}} | {{N}} | {{N}} |
| Test coverage | {{N}} | {{N}} | {{N}} |
| Scope creep | {{N}} | — | — |
| **Total** | **{{N}}** | **{{N}}** | **{{N}}** |

---

## Findings

### ADR conformance

<!--
Verify the implementation matches the approved ADR exactly.
One finding per deviation.
-->

#### 🔴 / 🟡 / 🟢 {{FINDING_TITLE}}

**File:** `{{FILE_PATH}}:{{LINE_NUMBER}}`  
**Issue:** {{CLEAR_DESCRIPTION_OF_THE_PROBLEM}}  
**ADR reference:** {{ADR_SECTION_OR_FIELD_THAT_IS_VIOLATED}}  
**Suggestion:** {{CONCRETE_FIX}}

---

### Acceptance criteria

<!--
For each AC in the scope brief, state whether it is satisfied.
If not satisfied or cannot be verified from code, flag it.
-->

| AC | Status | Notes |
|---|---|---|
| AC-1 | ✅ Satisfied / 🔴 Not satisfied / ⚠️ Needs manual check | {{NOTES}} |
| AC-2 | ✅ Satisfied / 🔴 Not satisfied / ⚠️ Needs manual check | {{NOTES}} |

---

### Code quality

<!--
Only concrete issues affecting correctness, maintainability, or safety.
One finding per issue.
-->

#### 🔴 / 🟡 {{FINDING_TITLE}}

**File:** `{{FILE_PATH}}:{{LINE_NUMBER}}`  
**Issue:** {{CLEAR_DESCRIPTION}}  
**Suggestion:** {{CONCRETE_FIX}}

---

### Test coverage

<!--
One finding per missing test. Reference the ADR endpoint or AC it should cover.
-->

#### 🔴 Missing test: {{WHAT_IS_NOT_TESTED}}

**ADR / AC reference:** {{WHAT_REQUIRES_THIS_TEST}}  
**Suggestion:** Add a test that {{WHAT_THE_TEST_SHOULD_DO}}

---

### Scope creep

<!--
List any code that was implemented but is not in the scope brief or ADR.
All scope creep is blocking regardless of quality.
If none found, write "None identified."
-->

#### 🔴 Scope creep: {{WHAT_WAS_ADDED}}

**File:** `{{FILE_PATH}}`  
**Description:** {{WHAT_WAS_BUILT_THAT_WAS_NOT_IN_SCOPE}}  
**Action required:** Remove or move to a separate scope brief.

---

### Positives

<!--
Note at least one thing done well if the work merits it.
Skip this section if nothing stands out.
-->

#### 🟢 {{POSITIVE_TITLE}}

**File:** `{{FILE_PATH}}`  
**Description:** {{WHAT_WAS_DONE_WELL_AND_WHY}}

---

## Verdict

<!--
Choose exactly one. Remove the other two.
-->

### ✅ Approved

No blocking issues found. The implementation conforms to the ADR and satisfies all acceptance criteria. Human may merge branch `{{BRANCH_NAME}}` into `{{TARGET_BRANCH}}`.

---

### 🔄 Changes requested

**{{N}} blocking issue(s) found.** The developer agent must address all 🔴 findings before re-review. Non-blocking findings are optional for this iteration.

**Blocking issues to resolve:**
1. {{BRIEF_SUMMARY_OF_BLOCKING_ISSUE_1}}
2. {{BRIEF_SUMMARY_OF_BLOCKING_ISSUE_2}}

---

### ⛔ Escalate to human

Findings require an architectural decision that goes beyond the current ADR. The developer agent cannot resolve these without architect input.

**Reason for escalation:** {{WHAT_ARCHITECTURAL_QUESTION_NEEDS_TO_BE_ANSWERED}}  
**Recommended action:** Human + architect agent to produce a revised or supplementary ADR before development continues.

---

**Report produced by:** reviewer agent  
**Human action required:** Merge / Request changes / Escalate to architect
