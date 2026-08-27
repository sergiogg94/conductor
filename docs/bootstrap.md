# Bootstrap

## Purpose

This document explains how `conductor` is installed into a consumer project, which files belong to the framework and which belong to the project, and how installed files are updated.

The automation lives in three scripts under `scripts/`:

| Script | Role |
|---|---|
| `bootstrap_project.py` | installs the framework into a target repository |
| `sync_framework.py` | updates framework-managed files in an already-bootstrapped project |
| `validate_templates.py` | validates the structural integrity of the source framework repo |

## Installing

From the root of the conductor repository:

```bash
python scripts/bootstrap_project.py /path/to/target-project
```

Options:

- `--dry-run` — show what would be installed without writing anything
- `--force` — overwrite existing framework-managed files (default: never overwrite)

Bootstrap is idempotent: re-running it on an installed project skips everything already present.

## Install Map

| Source in conductor | Destination in consumer project |
|---|---|
| `templates/project/conductor.yaml` | `./conductor.yaml` |
| `templates/project/.opencode/opencode.json` | `./.opencode/opencode.json` |
| `agents/primary/*.md`, `agents/subagents/*.md` | `./.opencode/agent/` (flattened) |
| `commands/*.md` | `./.opencode/command/` |
| `agents/shared/*.md` | `./.conductor/` |
| `templates/artifacts/*.md` | `./templates/artifacts/` |
| `templates/project/docs/**` | `./docs/**` |
| `templates/project/.github/**` | `./.github/**` |

Notes:

- agents are installed **rendered**: each source agent carries only a `model_tier` (`low` / `medium` / `high`); bootstrap resolves it to a concrete `model: provider/model-id` from the `model_tiers` map in `conductor.yaml`
- shared framework docs land at `.conductor/` so agent references to them resolve inside the consumer project
- artifact templates keep the literal path `templates/artifacts/` because agent output contracts reference it
- `agent-template.md` is source-only tooling for generating new framework agents and is never installed

## Model Tiers

Each agent references an effort tier instead of a hardcoded model. The concrete model per tier is defined once in `conductor.yaml`:

```yaml
model_tiers:
  low: opencode/big-pickle
  medium: opencode/big-pickle
  high: opencode/big-pickle
```

To change what a tier runs on, edit one line and re-sync — agents that use that tier are re-rendered automatically (see below). Adding a new tier requires updating both this map and the source agents' `model_tier`, which `validate_templates.py` enforces.

## Ownership Model

| Category | Files | Sync behavior |
|---|---|---|
| Framework-managed | `.opencode/agent/**`, `.opencode/command/**`, `.conductor/**`, `templates/artifacts/**`, `.opencode/opencode.json` | updated by `sync_framework.py --apply` |
| Project-owned | `conductor.yaml`, `docs/**`, `.github/**` | never synchronized |

Project-owned files hold user data: the filled-in configuration, real artifacts produced by agents, customized CI. Synchronizing would destroy them, so sync excludes them by design.

## Updating a Consumer Project

```bash
python scripts/sync_framework.py            # status report only
python scripts/sync_framework.py --apply    # update differing + restore missing
```

Status values: `up-to-date`, `differs`, `missing` (framework file absent locally), `local-only` (extra file in a managed directory — always preserved). Review results with `git diff` before committing.

Sync resolves agent models from the **project's own** `conductor.yaml` `model_tiers` map. If you reassign a tier there, the matching `.opencode/agent/*.md` files show as `differs` and are updated with `--apply`; agents whose tier did not change are left untouched.

## Post-install Steps

1. Edit `conductor.yaml`: project identity, `github.repository`, `github.projects` and (optionally) the `model_tiers` map
2. Start opencode in the project — `orchestrator` loads as the default agent
3. Run `/discover <idea>` to produce the first artifact
4. Optional: store the provider API key as the `ANTHROPIC_API_KEY` secret to enable `.github/workflows/opencode-review.yml`

## Validating the Source Framework

After changing framework structure (adding or renaming agents, commands, or templates):

```bash
python scripts/validate_templates.py
```

It verifies expected paths, artifact templates, command-to-agent wiring, and required agent frontmatter.
