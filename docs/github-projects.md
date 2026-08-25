# GitHub Projects

## Purpose

GitHub Projects is the tracking layer of `conductor`. It connects planning artifacts to trackable work: issues represent units of work, board state represents where each unit actually is, and transitions carry evidence.

GitHub as a whole is the system of record: code in repositories, tasks in issues, changes in pull requests, tracking in Projects.

The binding rules of interaction — who may create, move, or update what, and under which conditions — are defined in `agents/shared/github-projects-policy.md`. This document describes the board model; that policy governs it.

## Board Configuration

Each consumer project configures its own board in `conductor.yaml` under `github.projects`: owner, project number, field names, and state names. That file wins over any default whenever values differ.

Default fields:

| Field | Values |
|---|---|
| Status | Backlog, Ready, In Progress, Review, Blocked, Done |
| Priority | P0–P3 |
| Type | Feature, Bug, Chore, Spike |
| Area | project-defined |
| Effort | XS, S, M, L (relative sizes only) |
| Iteration | optional |
| Linked PR | PR reference |
| Risk | risk annotation |

## Default States

| State | Meaning |
|---|---|
| `Backlog` | captured as work, not yet scoped or planned |
| `Ready` | requirements and ADR approved; safe to implement |
| `In Progress` | a developer agent is actively working on it |
| `Review` | PR open; awaiting review report and human decision |
| `Blocked` | waiting on something external (decision, dependency, spike) |
| `Done` | accepted by the human — exclusively |

## Responsibility Summary

- **planner** creates items and proposes board operations — nothing reaches the board except through its plan
- **developer** may suggest `Ready → In Progress` and `In Progress → Review` with evidence (branch/PR link)
- **tester, reviewer, documenter** never move the board; they produce the reports others transition on
- **the human** applies every transition in MVP mode and owns `Done` unconditionally
- no status change without evidence: the PR, the review report, the test report, or explicit human approval

## MVP Mode

The MVP has no live GitHub integration. Agents emit suggested operations in a `## Board updates` section at the end of their artifacts; the human applies them manually through the GitHub UI or CLI.

Live write access (via GitHub MCP Server) is deliberately postponed — see `docs/roadmap.md`.

## Issue Types

Consumer projects receive four issue templates under `.github/ISSUE_TEMPLATE/`, matching the `Type` field:

- **Feature** — new functionality, traces to FR-N / AC-N / T-N identifiers
- **Bug** — deviation from a requirement or approved ADR, with severity 🔴🟡🟢
- **Chore** — maintenance task with an explicit scope guard
- **Spike** — time-boxed research answering one question

The pull request template mirrors what the reviewer expects as context: task IDs, traceability links, an explicit deviations statement, and validation performed.
