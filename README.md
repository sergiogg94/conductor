# conductor

A framework for building software by directing AI agents, not manually writing every line of code.

## Vision

`conductor` is a working framework for agent-assisted software development. Its goal is not to fully automate the development lifecycle, but to give you a structured way to collaborate with specialized agents inside your projects.

The core idea is simple:

- `conductor` defines the agents, commands, conventions, and artifacts
- each product repository consumes that framework
- OpenCode is used as the operational environment to execute the work
- GitHub is used as the system of record for code, issues, pull requests, and tracking
- GitHub Projects is used to manage the backlog and task status

## Problem it aims to solve

Working with AI agents in software development often degrades quickly into one or more of these problems:

- improvised prompts that are hard to reuse
- agents without clearly defined roles
- inconsistent outputs
- poor traceability between idea, task, code, and validation
- too much coupling to a single project
- difficulty repeating the same workflow across new repositories

`conductor` aims to solve this by defining a reusable foundation for working with agents in a clearer, more consistent, and more controlled way.

## What conductor is

`conductor` is the source repository for a framework that defines:

- a catalog of role-based agents
- reusable OpenCode commands
- working conventions between agents
- output contracts for each stage
- documentation templates
- a minimal structure for consumer repositories
- guidelines for GitHub Projects integration

## What conductor is not

`conductor` is not intended to be:

- a fully autonomous system that develops software without supervision
- a replacement for GitHub, CI/CD, or product management
- a framework tied to a single model provider
- a chaotic collection of prompts without a method

The human remains responsible for directing the development process, validating important decisions, and approving significant changes.

## Framework principles

1. The human leads
   - agents assist, propose, implement, and review
   - important decisions still require human validation

2. Agents exchange artifacts, not free-form conversations
   - requirements
   - architecture
   - work plans
   - code
   - reviews
   - tests
   - documentation

3. Each agent has a clear role
   - defined scope
   - expected inputs
   - concrete outputs
   - responsibility boundaries

4. GitHub is the system of record
   - code lives in the repository
   - tasks live in issues
   - changes happen through pull requests
   - tracking happens in GitHub Projects

5. OpenCode is the operational workspace
   - agent execution
   - commands
   - code iteration
   - human-agent collaboration

6. The framework must be reusable
   - agents live in `conductor`
   - consumer projects inherit a base configuration
   - conventions should apply across multiple repositories

## MVP components

The `conductor` MVP aims to include a minimal but usable foundation:

- an initial catalog of agents
- a standard file structure for consumer projects
- base OpenCode commands
- initial artifact templates
- a central framework configuration per project
- guidelines for using GitHub Projects as the tracking board
- a bootstrap script to install the framework into a project repository

## Expected workflow

At a high level, the workflow `conductor` aims to support looks like this:

1. Discovery
   - an idea is turned into a problem statement, goals, and context

2. Scope and requirements
   - scope, acceptance criteria, and an initial backlog are defined

3. Planning
   - tasks are generated and registered in GitHub Issues / GitHub Projects

4. Architecture
   - technical decisions and an implementation plan are defined

5. Development
   - changes are implemented in branches and pull requests using OpenCode

6. Review and testing
   - code is reviewed, tests are generated, and requirements are validated

7. Delivery
   - documentation, task status, and final outputs are updated

## MVP agent set

The exact set may evolve, but the MVP starts with agents such as:

- `orchestrator`
- `discovery`
- `scopper`
- `planner`
- `architect`
- `developer`
- `reviewer`
- `tester`
- `devops`
- `docs`

Each agent will define:
- purpose
- inputs
- outputs
- expected permissions
- usage rules

## GitHub integration

`conductor` is designed to work with GitHub as the operational center of the project:

- repositories for code
- issues for tasks
- pull requests for changes
- actions for automation
- projects for work tracking

Integration with GitHub Projects is an important part of the framework because it keeps the backlog and execution state aligned with agent-driven work.

## Model integration

`conductor` does not depend on a single model or provider.

It is designed to support a hybrid strategy, for example:

- local models for small tasks
- free models for medium-complexity work
- more powerful APIs for demanding tasks

The policy for which agent uses which class of model will be defined per project.

## Expected repository structure

This repository will grow to include, at minimum:

- agents
- commands
- templates
- configuration
- bootstrap scripts
- framework documentation

## Current status

`conductor` is under construction. This repository is being used to define the MVP of the framework and turn an agent-driven development idea into a reusable foundation for real projects.

## Immediate goal

The immediate goal is to reach an MVP that allows you to:

- install a base structure into a new project
- work with agents defined in `conductor`
- use OpenCode as the main development interface
- organize tasks in GitHub Projects
- maintain consistency between requirements, execution, and tracking

## Initial roadmap

1. Define the conceptual model of the framework
2. Design the MVP agent catalog
3. Create the base repository structure
4. Define `conductor.yaml`
5. Create MVP agents and commands
6. Design consumer project templates
7. Implement framework bootstrap
8. Formalize GitHub Projects usage

## License

GPL-3.0

## Project status

MVP in design and construction.
