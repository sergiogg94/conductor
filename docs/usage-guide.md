# Usage Guide

## Purpose

This guide walks through the framework from zero to your first interaction in OpenCode: installing the framework into a consumer project, starting OpenCode, and running a discovery against a real idea. It complements `docs/bootstrap.md`, which documents the install mechanics in detail.

## What You Need

- Python 3.13 or newer (framework scripts are stdlib-only)
- `pipx install opencode` (or any way you prefer to run OpenCode)
- the `conductor` framework repository cloned locally
- a Git repository that will be your consumer project

The framework targets Linux/macOS. Paths below assume a Bash shell.

## Step 1 — Have a Consumer Project

Your consumer project is the repository where real work happens. It can be empty:

```bash
mkdir ~/projects/my-app && cd ~/projects/my-app
git init
```

You can bootstrap into an existing project too; bootstrap only adds framework files and never touches your source tree.

## Step 2 — Bootstrap the Framework

From inside the `conductor` repository, point the installer at your project:

```bash
# from the conductor repo root
python scripts/bootstrap_project.py ~/projects/my-app
```

The installer copies agents, commands, shared contracts, artifact templates, config, and GitHub scaffolding into the target, flattened and ready to use. It never overwrites existing framework files by default, and it refuses to run inside the conductor repo itself.

Preview first if you want, then run for real:

```bash
python scripts/bootstrap_project.py ~/projects/my-app --dry-run
python scripts/bootstrap_project.py ~/projects/my-app
```

## Step 3 — Configure the Project

Open `~/projects/my-app/conductor.yaml` and edit the fields that are placeholders by default:

- `project.name`, `project.slug`, `project.description` — who this project is
- `github.repository.owner` / `name` / `default_branch` — your repo identity
- `github.projects.owner` / `project_number` — which board to track against
- per-agent `model_tier` — `small` / `medium` / `strong` for what each role deserves
- `artifacts.*` — keep the defaults unless you have a reason to move them

The agents reference these values, so fill in the project identity before your first run. `conductor.yaml` is the single project-owned configuration file; sync never overwrites it.

## Step 4 — Start OpenCode in the Project

```bash
cd ~/projects/my-app
opencode
```

The bootstrap installed `.opencode/opencode.json` with `"default_agent": "orchestrator"`, so OpenCode starts you in the orchestrator agent. Orchestrator is the dispatcher: it holds the full pipeline view and connects each stage to the right specialized agent.

## Step 5 — Your First Interaction

Give the orchestrator a real idea to work on in plain language (no slash command — the orchestrator is the default agent and dispatches stages for you):

```
Build a public REST API for our user registry, with validation and unit tests.
```

Orchestrator breaks work into stages and hands off to the specialized agents in order. The stages it runs through match the framework commands, each producing its contracted artifact and returning to the human for approval before the next stage runs:

```text
/discover   →  docs/discovery.md                  (first command on any new idea)
/scope      →  docs/requirements.md
/plan       →  docs/implementation-plan.md
/architect  →  ADR(s) under docs/adr/
/implement  →  code on a feature branch + notes
/test       →  test report under docs/tests/
/review     →  review report under docs/reviews/
/docs       →  docs/delivery-checklist.md
```

### What Approvals Look Like

`conductor` is human-directed. At each gate the agent fills its artifact, marks it **🟡 pending approval**, and stops. You review it, approve (✅) or request changes, and confirm before the pipeline advances. The orchestrator will tell you when it is your turn and what to look at.

### Invoking Commands Directly

You are not limited to the orchestrator. Each command maps to its own agent and can be run directly when you know what you want:

```
/discover <idea>          → discovery agent
/scope <statement>        → scopper agent
/plan <goal>              → planner agent
/architect <requirements> → architect agent
/implement <tasks>        → developer agent
/test <work>              → tester agent
/review <work>            → reviewer agent
/docs <work>              → documenter agent
```

For example, once discovery is approved, run `/plan <goal>` to convert it into trackable tasks. `validate_templates.py` guarantees every command points at an agent that actually exists.

## Step 6 — Update the Framework Later

When the conductor repo ships improvements, update the installed copy of the framework-managed assets:

```bash
# report what changed
python scripts/sync_framework.py ~/projects/my-app

# apply changes to framework-managed files only
python scripts/sync_framework.py ~/projects/my-app --apply
```

Sync touches only `.opencode/agent/**`, `.opencode/command/**`, `.conductor/**`, `templates/artifacts/**`, and `.opencode/opencode.json`. Your artifacts under `docs/**`, your `conductor.yaml`, and your `.github/**` are preserved.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `bootstrap_project.py` exits 1 | you ran it inside the conductor repo itself — point it at the consumer project |
| command `/xyz` not found | the command file is not in `.opencode/command/`; re-run sync with `--apply` |
| agents can't find `core-principles.md` | shared contracts live in `.conductor/`; if missing, re-run bootstrap |
| artifacts land in unexpected places | paths come from `conductor.yaml` under `artifacts` — check them there |
| a stage refuses to start | an upstream artifact was not approved; review and approve it first |
