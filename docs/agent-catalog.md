# Agent Catalog

## Purpose

This document defines the MVP agent catalog for `conductor`.

Its purpose is to describe:

- which agents exist in the MVP
- what each agent is responsible for
- what each agent should receive as input
- what each agent should produce as output
- what each agent should not do
- how agents relate to each other in the workflow

This document is the design reference for the actual OpenCode agent files that will be created later.

## Design Principles

The agent catalog is designed around the following principles:

1. Agents are role-based workers, not free-form personalities.
2. Each agent should have a narrow and clear responsibility.
3. Agents should collaborate through artifacts and task state, not long conversations.
4. Important decisions should remain visible and reviewable by a human.
5. Agents should be reusable across multiple repositories and project types.
6. The MVP should prefer clarity over excessive specialization.

## Agent Types

The MVP uses two categories of agents:

- primary agents
- subagents

### Primary Agents

Primary agents are top-level control agents used as the main entry point in OpenCode sessions.

For the MVP, `conductor` defines one primary agent:

- `orchestrator`

### Subagents

Subagents are specialized role agents invoked for focused work.

The MVP defines the following subagents:

- `discovery`
- `scopper`
- `planner`
- `architect`
- `developer`
- `reviewer`
- `tester`
- `devops`
- `docs`

## Workflow Positioning

The agents roughly map to the development lifecycle like this:

1. `orchestrator`
   - coordinates the workflow
2. `discovery`
   - frames the problem
3. `scopper`
   - defines scope and requirements
4. `planner`
   - converts scope into tasks and tracking structures
5. `architect`
   - defines technical direction
6. `developer`
   - implements changes
7. `reviewer`
   - reviews implementation quality
8. `tester`
   - validates expected behavior
9. `devops`
   - supports automation, CI/CD, and environment workflows
10. `docs`
   - maintains documentation and delivery-facing written outputs

## Agent Definition Template

Each agent in this catalog is described using the same structure:

- role
- purpose
- typical inputs
- expected outputs
- responsibilities
- non-responsibilities
- dependencies
- model tier (`low` / `medium` / `high`) — the effort tier the agent needs; the concrete model is resolved from the `model_tiers` map in `conductor.yaml` at install
- GitHub Projects relationship

This structure should later map into each OpenCode agent definition.

---

## 1. Orchestrator

### Role

Primary agent.

### Purpose

The `orchestrator` is the top-level coordinating agent of the framework.

It is responsible for:
- understanding the current state of work
- selecting the next appropriate agent or workflow step
- enforcing structured handoffs
- identifying missing inputs or unresolved ambiguity
- keeping the process aligned with the framework

The `orchestrator` is not the main executor of specialized work. Its value is coordination, sequencing, and control.

### Typical Inputs

- user goals
- current repository context
- existing framework artifacts
- task status from GitHub Issues / GitHub Projects
- outputs from subagents
- current stage of the workflow

### Expected Outputs

- workflow recommendations
- next-step instructions
- delegation to specialized agents
- gap analysis
- coordination summaries

### Responsibilities

- decide which agent should act next
- check whether previous outputs are sufficient
- prevent premature implementation
- detect missing requirements, architecture, or validation
- keep the workflow structured
- escalate major uncertainty to the human

### Non-Responsibilities

- writing detailed requirements
- designing architecture itself when an architect agent should do it
- performing implementation work in place of the developer
- acting as the final human approver

### Dependencies

- all artifact types
- all specialized subagents

### Suggested Model Tier

- medium or strong reasoning model

### GitHub Projects Relationship

- may inspect project state
- may recommend transitions
- should not be the main agent updating task state directly unless explicitly instructed

---

## 2. Discovery

### Role

Subagent.

### Purpose

The `discovery` agent turns an initial idea into a clarified problem statement.

Its purpose is to surface:
- user goals
- business or product intent
- assumptions
- constraints
- open questions
- non-goals

It creates the earliest structured understanding of the work.

### Typical Inputs

- rough feature idea
- problem statement
- initial notes
- product context
- user description
- existing documentation if available

### Expected Outputs

- discovery notes
- problem framing
- goals and non-goals
- assumptions
- open questions
- early risk signals

### Responsibilities

- clarify what problem is being solved
- distinguish goals from implementation ideas
- identify ambiguity early
- make assumptions explicit
- capture missing information
- prepare input for scoping

### Non-Responsibilities

- writing final requirements
- creating implementation tasks
- defining architecture
- writing production code

### Dependencies

- human-provided intent
- optional existing product documentation

### Suggested Model Tier

- small to medium model

### GitHub Projects Relationship

- no direct responsibility for project state changes
- may inform future issue and project item creation

---

## 3. Scopper

### Role

Subagent.

### Purpose

The `scopper` agent converts discovery outputs into scope and requirements.

Its purpose is to define:
- what should be built
- what should not be built
- acceptance criteria
- edge cases
- functional and non-functional expectations

This agent transforms broad intent into actionable scope.

### Typical Inputs

- discovery output
- product constraints
- current project context
- user clarifications
- relevant existing documentation

### Expected Outputs

- requirements artifact
- scoped feature definition
- acceptance criteria
- exclusions and non-goals
- edge case checklist
- initial backlog candidates

### Responsibilities

- define scope boundaries
- write clear requirements
- define testable acceptance criteria
- identify key edge cases
- separate core scope from optional follow-up work
- prepare work for planning

### Non-Responsibilities

- creating GitHub tasks directly unless explicitly routed through planning
- choosing technical architecture
- implementing code
- approving scope changes without human input

### Dependencies

- discovery artifact
- human clarifications where required

### Suggested Model Tier

- small to medium model

### GitHub Projects Relationship

- no direct ownership of task state
- provides the material that planning will convert into trackable work

---

## 4. Planner

### Role

Subagent.

### Purpose

The `planner` agent converts scoped work into executable tasks and tracking structures.

Its purpose is to break work into:
- issues
- task groups
- implementation slices
- priorities
- dependencies
- project board updates

This agent is the bridge between requirements and execution.

### Typical Inputs

- requirements artifact
- acceptance criteria
- project conventions
- GitHub Projects policy
- repository context

### Expected Outputs

- implementation plan
- issue definitions
- task breakdown
- dependency map
- task priorities
- GitHub Project update suggestions

### Responsibilities

- break scoped work into manageable tasks
- define task sequencing
- identify dependencies and blockers
- map tasks to GitHub Issues and GitHub Projects
- distinguish MVP work from optional work
- prepare the handoff to architecture and development

### Non-Responsibilities

- defining low-level architecture in detail
- implementing changes
- reviewing code
- validating final acceptance

### Dependencies

- requirements artifact
- GitHub Projects conventions
- repository and product context

### Suggested Model Tier

- medium model

### GitHub Projects Relationship

- primary task-structuring agent for project tracking
- may create or update task state if the workflow enables it
- should be the main source of board organization logic

---

## 5. Architect

### Role

Subagent.

### Purpose

The `architect` agent defines technical direction for a scoped body of work.

Its purpose is to produce:
- technical design
- implementation approach
- component boundaries
- interface definitions
- technical risks
- design tradeoffs

It should make implementation easier by reducing ambiguity.

### Typical Inputs

- requirements artifact
- implementation plan
- repository context
- existing architecture documentation
- technical constraints

### Expected Outputs

- architecture artifact
- implementation approach
- module or component changes
- interface or API proposals
- ADR-style decisions when needed
- technical risk notes

### Responsibilities

- define a reasonable technical approach
- align implementation with existing project structure
- identify tradeoffs
- minimize architectural ambiguity for development
- highlight areas requiring human technical approval
- surface risk before implementation starts

### Non-Responsibilities

- implementing code directly
- writing final tests
- approving production readiness
- managing board state as its primary task

### Dependencies

- scoped requirements
- repository structure
- planning outputs

### Suggested Model Tier

- medium to strong reasoning model

### GitHub Projects Relationship

- may annotate technical risk or complexity
- not the primary owner of board maintenance

---

## 6. Developer

### Role

Subagent.

### Purpose

The `developer` agent implements approved work inside the repository.

Its purpose is to:
- modify code
- create or update files
- follow the implementation plan
- align changes with requirements and architecture
- keep the work focused on the assigned task

### Typical Inputs

- implementation task
- requirements artifact
- architecture artifact
- repository context
- existing codebase
- acceptance criteria

### Expected Outputs

- code changes
- implementation notes
- updated files
- proposed follow-up issues if needed

### Responsibilities

- implement the assigned change
- stay within scope
- preserve consistency with project conventions
- avoid unrelated edits
- call out blockers or ambiguity
- leave the work in a reviewable state

### Non-Responsibilities

- inventing or changing requirements without approval
- redefining architecture on its own
- marking work as complete without review and validation
- owning project board planning logic

### Dependencies

- scoped and approved task
- architecture guidance when required
- relevant existing code

### Suggested Model Tier

- medium to strong coding model

### GitHub Projects Relationship

- may move assigned work into active execution states if permitted
- should not autonomously close the work loop without review and testing

---

## 7. Reviewer

### Role

Subagent.

### Purpose

The `reviewer` agent evaluates implementation quality before completion.

Its purpose is to inspect:
- correctness
- code quality
- maintainability
- consistency
- obvious risks
- unnecessary complexity

It should behave like a disciplined code reviewer, not just a summarizer.

### Typical Inputs

- code changes
- pull request diff
- requirements artifact
- architecture artifact
- project conventions

### Expected Outputs

- review report
- findings by severity
- suggested fixes
- maintainability concerns
- consistency feedback

### Responsibilities

- review whether the implementation matches intent
- identify code smells and risky changes
- check maintainability and consistency
- flag likely defects or weak design choices
- produce clear review feedback

### Non-Responsibilities

- writing the main implementation instead of reviewing it
- approving business scope
- replacing the tester
- making final human merge decisions

### Dependencies

- implementation outputs
- requirements and architecture context

### Suggested Model Tier

- medium to strong reasoning/coding model

### GitHub Projects Relationship

- may recommend transition into review-related states
- should not mark work done on its own

---

## 8. Tester

### Role

Subagent.

### Purpose

The `tester` agent validates whether implemented work satisfies requirements.

Its purpose is to create or assess:
- unit tests
- integration tests
- validation scenarios
- acceptance checks
- regression concerns

This agent focuses on behavior validation, not style or architecture.

### Typical Inputs

- requirements artifact
- acceptance criteria
- code changes
- test suite context
- repository structure

### Expected Outputs

- test plan
- test additions or suggestions
- validation notes
- uncovered cases
- acceptance status summary

### Responsibilities

- map requirements to validation
- identify missing tests
- create or improve test coverage where appropriate
- check important edge cases
- assess whether acceptance criteria appear satisfied

### Non-Responsibilities

- replacing the code reviewer
- changing project scope
- making production release decisions
- doing broad architecture redesign

### Dependencies

- requirements artifact
- implementation output
- repository testing structure

### Suggested Model Tier

- medium coding model

### GitHub Projects Relationship

- may recommend whether a task is ready for review or completion
- should not independently declare final completion for critical work

---

## 9. DevOps

### Role

Subagent.

### Purpose

The `devops` agent supports delivery infrastructure and engineering workflow automation.

Its purpose is to work on:
- CI/CD workflows
- GitHub Actions
- local development setup
- automation scripts
- environment consistency
- release-path concerns

### Typical Inputs

- repository configuration
- workflow files
- build/test requirements
- deployment or automation goals
- developer workflow constraints

### Expected Outputs

- workflow recommendations
- CI/CD changes
- environment setup notes
- automation scripts
- pipeline review findings

### Responsibilities

- inspect and improve workflows
- reduce friction in build and validation pipelines
- support release and automation needs
- align CI/CD with project requirements
- identify obvious workflow reliability issues

### Non-Responsibilities

- owning product requirements
- writing feature implementation as its primary task
- acting as the final release approver
- managing all project board logic

### Dependencies

- repository workflows
- build and release context
- project conventions

### Suggested Model Tier

- medium model

### GitHub Projects Relationship

- may interact with tasks related to automation, CI, deployment, or reliability
- not the default board manager for all task types

---

## 10. Docs

### Role

Subagent.

### Purpose

The `docs` agent creates and maintains written project documentation.

Its purpose is to improve clarity around:
- feature behavior
- technical design summaries
- implementation notes
- delivery notes
- user-facing or contributor-facing documentation

### Typical Inputs

- requirements artifact
- architecture artifact
- implementation notes
- review findings
- repository docs context

### Expected Outputs

- updated documentation
- feature notes
- setup instructions
- architecture summaries
- delivery summaries
- release-oriented written artifacts

### Responsibilities

- keep written artifacts consistent and useful
- translate implementation outcomes into understandable documentation
- update documentation when behavior changes
- reduce knowledge loss

### Non-Responsibilities

- defining scope by itself
- replacing architecture decisions
- implementing production code as its main job
- approving work completion

### Dependencies

- upstream workflow artifacts
- repository documentation context

### Suggested Model Tier

- small to medium model

### GitHub Projects Relationship

- may support documentation-related tasks and completion notes
- should not be the main source of project planning state

---

## Agent Handoff Model

The MVP assumes the following default handoff pattern:

1. `orchestrator`
   - determines the current stage and required next step

2. `discovery`
   - creates initial understanding

3. `scopper`
   - converts understanding into scope and requirements

4. `planner`
   - converts scope into executable tracked work

5. `architect`
   - defines the technical approach

6. `developer`
   - implements the work

7. `reviewer`
   - checks implementation quality

8. `tester`
   - validates behavior and acceptance criteria

9. `devops`
   - supports workflow automation where needed

10. `docs`
   - updates written artifacts and delivery-facing outputs

Not every task must pass through every agent, but this is the reference workflow model.

## Suggested Ownership Boundaries

To keep the framework disciplined, each agent should own a narrow layer of responsibility:

- `discovery` owns problem framing
- `scopper` owns requirements and boundaries
- `planner` owns execution decomposition
- `architect` owns technical direction
- `developer` owns implementation
- `reviewer` owns code quality review
- `tester` owns validation logic
- `devops` owns workflow automation and pipeline concerns
- `docs` owns documentation updates
- `orchestrator` owns sequencing and coordination

These boundaries should be reflected in the actual agent files.

## Suggested Permission Philosophy

At a high level, permissions should follow role responsibility:

- `orchestrator`: limited direct mutation, broad coordination
- `discovery`: read-heavy, no write by default
- `scopper`: read-heavy, no code write by default
- `planner`: read-heavy, task- and planning-oriented actions
- `architect`: read-heavy, no broad code write by default
- `developer`: write-enabled
- `reviewer`: read-only or review-oriented
- `tester`: selective write depending on whether generating tests is allowed
- `devops`: may require workflow and config edits
- `docs`: documentation write allowed, broad system mutation not required

The exact permissions will be defined in the actual OpenCode agent files.

## MVP Scope Notes

The MVP deliberately keeps some responsibilities lightweight:

- no dedicated security agent yet
- no dedicated release agent yet
- no separate product manager agent yet
- no separate refactor agent yet

These may be added later, but the current catalog is enough to validate the core framework.

## Summary

The MVP agent catalog for `conductor` is designed to provide:

- clear separation of responsibilities
- artifact-based collaboration
- compatibility with OpenCode workflows
- alignment with GitHub Issues, Pull Requests, and GitHub Projects
- a strong enough structure to support real project work without over-specializing too early

This catalog is the basis for the next implementation step: writing the actual agent definition files.
