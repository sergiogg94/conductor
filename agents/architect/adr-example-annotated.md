# ADR example — annotated

This file explains what makes a good ADR for each section.
Use it alongside `templates/adr.md` when reviewing ADRs produced by the architect agent.

---

## What the architect SHOULD produce

**Context** — A tight paragraph that explains *why* a decision is needed now.
Good: "The recipe CRUD scope requires persisting structured ingredient data alongside recipe metadata.
The existing project has PostgreSQL available via Docker Compose. The data model decision must be
made before the developer agent can write any migration or endpoint."

Bad: "We need to store data." (too vague) / "In the future we may want to support multiple users,
so we should design a multi-tenant schema now." (out of scope speculation)

---

**Decision statement** — One sentence, active voice, present tense.
Good: "We will use a single `recipes` table with a JSONB `ingredients` column for ingredient data."
Bad: "We decided that perhaps a JSONB approach might be considered for the ingredients."

---

**Options** — Each option must be genuinely viable. The architect must know the project well enough
to argue for each one. If an option is added only to be rejected, remove it.

Example of a genuine option (not a strawman):
Option A — Separate `ingredients` table (normalized relational model)
Option B — JSONB column in `recipes` table
Option C — Embedded document in a NoSQL store (only valid if the project already has one)

---

**Rationale** — Must cite the scope brief. Must cite a project constraint.
Good: "Option B (JSONB) satisfies AC-1 and AC-2 from the scope brief: ingredient data is always
read and written together with the recipe, so a join-free access pattern reduces query complexity.
The project uses PostgreSQL which has mature JSONB support. Option A would be preferred if
ingredient data needed to be queried independently (e.g. 'find all recipes using chicken') but
that use case is explicitly out of scope in the current brief."

---

**Implementation guidance** — The most important section.
The developer agent reads this and writes code. Ambiguity here = bugs or scope creep.
Every field name, every endpoint path, every status code must be explicit.

---

**Guard rails** — Underused but critical.
These prevent the developer agent from adding features that are out of scope.
Examples:
- Do not add a `tags` field to the data model (out of scope).
- Do not implement pagination on `GET /recipes` (explicitly out of scope in the brief).
- Do not add authentication middleware (single-user system, out of scope).

---

## Red flags in an architect output — ask for revision

- Options section has only one real option and one obvious strawman.
- Implementation guidance uses vague language ("appropriate validation", "suitable error handling").
- Guard rails section is empty.
- The ADR does not reference the scope brief's acceptance criteria.
- The recommended option introduces a new library not in the current stack without justification.
- The ADR covers more than one independent architectural decision.
