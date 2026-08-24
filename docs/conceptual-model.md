# Conceptual Model

## Purpose

`conductor` is a reusable framework for running software development workflows through specialized AI agents, with the human acting as the director of the process.

The framework is designed to provide structure, consistency, and traceability across projects by standardizing:

- agent roles
- expected artifacts
- working conventions
- project setup
- GitHub-based task tracking
- OpenCode-based execution

Its purpose is not to automate software development end to end without supervision. Its purpose is to make human-directed, agent-assisted development repeatable and scalable across repositories.

## Core Idea

`conductor` separates the framework from the product repository.

- `conductor` contains the reusable development method
- product repositories consume and apply that method

This allows the same working model to be reused across multiple projects without rebuilding prompts, conventions, and tooling from scratch every time.

## Operating Model

The operating model of `conductor` is based on five layers:

1. Human direction
2. Specialized agents
3. Structured artifacts
4. Operational tooling
5. Project tracking

These layers work together to turn ideas into implemented and reviewed software changes.

## Layer 1: Human Direction

The human is the owner of intent, priority, and approval.

The human is responsible for:

- defining goals
- clarifying ambiguity
- validating scope
- approving technical direction
- deciding when work is ready to merge or release

Agents assist the process, but they do not replace human judgment on important decisions.

This principle is fundamental to `conductor`.

## Layer 2: Specialized Agents

`conductor` models software development as collaboration between specialized agents instead of one general-purpose assistant.

Each agent has:

- a specific responsibility
- a defined scope
- expected inputs
- expected outputs
- operational constraints
- a preferred model profile
- explicit permissions where applicable

Agents should not behave like free-form personas. They should behave like role-based workers that produce useful, reviewable outputs.

### Agent Roles in the Framework

The exact catalog may evolve, but the framework assumes roles such as:

- discovery
- scopper
- planner
- architect
- developer
- reviewer
- tester
- devops
- docs
- orchestrator

Each role exists to reduce ambiguity, separate concerns, and improve handoff quality between stages.

## Layer 3: Structured Artifacts

Agents collaborate by producing artifacts, not by relying on long unstructured conversations.

Artifacts are the backbone of traceability in `conductor`.

Examples include:

- discovery notes
- requirements documents
- architecture documents
- implementation plans
- issue definitions
- pull request descriptions
- review reports
- test plans
- delivery checklists

Each artifact should have:

- a clear owner agent
- a clear purpose
- a stable location when possible
- a minimum required structure

Artifacts make it easier to:

- inspect progress
- validate handoffs
- reduce context loss
- rerun or continue work later
- sync work with GitHub issues and projects

## Layer 4: Operational Tooling

`conductor` assumes OpenCode is the primary operational environment for agent execution.

OpenCode is used for:

- running agents
- switching between roles
- invoking commands
- reading and modifying code
- interacting with tools in the development environment

`conductor` does not attempt to replace OpenCode. Instead, it provides a reusable structure on top of it.

The framework also assumes supporting tooling around:

- Git
- GitHub
- CI/CD
- local model runtimes
- external model providers
- optional MCP integrations

## Layer 5: Project Tracking

`conductor` treats GitHub as the system of record for operational project state.

This includes:

- repositories for source code
- issues for units of work
- pull requests for proposed changes
- GitHub Projects for backlog and execution tracking
- GitHub Actions for automation and validation

GitHub Projects is especially important in the framework because it connects planning and execution.

The framework should make it possible to map agent work to project state in a structured way.

## Primary Objects in the Framework

The conceptual model of `conductor` revolves around a small set of primary objects.

### 1. Framework Repository

The `conductor` repository is the source of truth for the framework itself.

It contains:

- agent definitions
- command definitions
- templates
- conventions
- bootstrap logic
- framework documentation

### 2. Consumer Repository

A consumer repository is a software project that installs and uses `conductor`.

It contains:

- project code
- project-specific configuration
- installed agent files
- installed command files
- generated artifacts
- GitHub workflows and templates where applicable

### 3. Agent

An agent is a role-specific worker defined by the framework.

An agent has:

- name
- purpose
- mode
- prompt/instructions
- permissions
- expected inputs
- expected outputs

### 4. Command

A command is a reusable entry point for invoking a repeatable task in OpenCode.

Commands provide a stable interface for common actions such as:

- discovery
- scoping
- planning
- architecture
- implementation
- review
- testing
- documentation
- project sync

### 5. Artifact

An artifact is a persistent output produced by an agent or a workflow stage.

Artifacts are designed to survive beyond a single session and become shared context for the project.

### 6. Task

A task is a unit of work tracked in GitHub, usually through an issue and a GitHub Project item.

Tasks connect planning to execution.

### 7. Project Board State

A project board state represents the workflow status of a task inside GitHub Projects.

Examples:

- Backlog
- Ready
- In Progress
- Review
- Blocked
- Done

### 8. Framework Configuration

Each consumer repository should define a framework configuration file, expected to be `conductor.yaml`.

This configuration controls how the framework is applied in that specific project.

## Workflow Stages

The framework assumes a staged workflow, even if some projects iterate more loosely.

### Stage 1: Discovery

Goal:
- clarify the problem, users, and goals

Outputs:
- discovery artifact
- open questions
- assumptions

### Stage 2: Scope

Goal:
- define what will and will not be built

Outputs:
- requirements
- acceptance criteria
- initial backlog candidates

### Stage 3: Planning

Goal:
- convert scope into executable work items

Outputs:
- issues
- project board items
- task priorities
- dependencies

### Stage 4: Architecture

Goal:
- define technical direction and implementation structure

Outputs:
- architecture artifact
- technical decisions
- interfaces
- risks
- ADRs when needed

### Stage 5: Development

Goal:
- implement code changes

Outputs:
- code
- branch changes
- pull requests
- implementation notes

### Stage 6: Review and Testing

Goal:
- validate code quality and behavior

Outputs:
- review findings
- test artifacts
- acceptance validation
- follow-up fixes

### Stage 7: Delivery

Goal:
- complete and document the work

Outputs:
- updated documentation
- release notes if needed
- task state updates
- final delivery summary

## Agent Interaction Model

Agents should interact through controlled handoffs.

The recommended pattern is:

1. an agent receives a defined input
2. the agent produces a structured output
3. the output becomes the next agent's input
4. the human validates important transitions

This reduces:

- ambiguity
- duplicated work
- uncontrolled agent-to-agent drift
- context explosion

### Recommended Handoff Style

Instead of:
- long conversational chains between agents

Prefer:
- documented artifacts
- issue-linked outputs
- explicit acceptance criteria
- structured review reports

## Governance Model

`conductor` should enforce a lightweight governance model.

Important decisions should require human review, especially:

- project scope
- architecture choices
- high-impact code changes
- task completion for critical work
- release readiness

The framework should support agent autonomy for execution, but not remove human control from important checkpoints.

## Model Strategy

The conceptual model of `conductor` is model-agnostic.

It should support different model classes depending on task complexity, cost, and speed requirements.

A typical strategy may include:

- local models for small, cheap, repeatable tasks
- free hosted models for medium-complexity work
- premium or faster APIs for harder implementation and reasoning tasks

The framework should define which roles or commands are suitable for which model tier, but should not hardcode a single provider strategy.

## Reusability Model

`conductor` is intended to be reusable across many repositories.

This means the framework should distinguish between:

- framework defaults
- project-specific overrides

Projects should be able to override:

- enabled agents
- model assignments
- coding conventions
- artifact paths
- GitHub project settings
- command behavior

Without this separation, the framework would become too rigid to reuse effectively.

## GitHub Projects Model

GitHub Projects is a first-class tracking layer in `conductor`.

The framework should define a standard way to represent work using fields such as:

- status
- priority
- type
- area
- effort
- iteration
- owner
- linked PR
- risk

It should also define which agents are responsible for updating project state and under what conditions.

This is important to avoid inconsistent board state when multiple agents interact with the same project.

## Bootstrap Model

`conductor` should provide a bootstrap process for consumer repositories.

The bootstrap process should install or generate:

- OpenCode agent files
- OpenCode commands
- framework configuration
- artifact templates
- optional GitHub workflow templates
- documentation scaffolding

The goal is to let a new project adopt the framework quickly and consistently.

## Success Criteria for the MVP

The MVP succeeds if it can do the following reliably:

- define a small, coherent agent catalog
- install the framework into a project repository
- support a repeatable development flow in OpenCode
- produce stable artifacts between workflow stages
- integrate conceptually with GitHub Issues, Pull Requests, and GitHub Projects
- remain simple enough to use on real projects without heavy maintenance

## Design Constraints

The framework should be designed with the following constraints in mind:

- prompts and agent behavior will evolve over time
- different projects will need different levels of rigor
- model availability may vary
- some tasks will remain manual
- GitHub integration may begin lightweight before becoming deeper
- the MVP should optimize for clarity and usability over completeness

## Summary

`conductor` is a human-directed, agent-assisted software development framework built around:

- specialized agents
- structured artifacts
- OpenCode execution
- GitHub-based tracking
- reusable project setup

Its central promise is not full automation.

Its central promise is a repeatable operating model for building software with AI agents in a way that is structured, inspectable, and reusable.
