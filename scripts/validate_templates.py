#!/usr/bin/env python3
"""Validate the structural integrity of the conductor framework repository.

Usage:
    python scripts/validate_templates.py

Checks that expected files exist, that every command targets an existing agent,
and that agent files declare the required frontmatter keys.
"""

from __future__ import annotations

import sys
from pathlib import Path

from bootstrap_project import (
    AGENT_TIERS,
    SOURCE_ROOT,
    REQUIRED_SOURCES,
    build_manifest,
    parse_frontmatter,
    validate_sources,
    validate_tiers,
)

AGENT_FRONTMATTER_KEYS = {"description", "mode", "model_tier"}
ARTIFACT_TEMPLATES = [
    "adr.md",
    "delivery-checklist.md",
    "discovery.md",
    "implementation-notes.md",
    "implementation-plan.md",
    "requirements.md",
    "review-report.md",
    "test-report.md",
]


def check_exists(relative: str) -> str | None:
    if not (SOURCE_ROOT / relative).exists():
        return f"missing: {relative}"
    return None


def validate() -> tuple[list[str], int]:
    errors: list[str] = []
    checks = 0

    for problem in validate_sources(build_manifest()):
        errors.append(problem)
        checks += 1

    manifest = build_manifest()
    for problem in validate_tiers(manifest):
        errors.append(problem)
        checks += 1

    for required in REQUIRED_SOURCES:
        checks += 1
        error = check_exists(required)
        if error:
            errors.append(error)

    for template in ARTIFACT_TEMPLATES:
        checks += 1
        error = check_exists(f"templates/artifacts/{template}")
        if error:
            errors.append(error)

    command_dir = SOURCE_ROOT / "commands"
    agent_dirs = [SOURCE_ROOT / "agents/primary", SOURCE_ROOT / "agents/subagents"]

    commands = sorted(command_dir.glob("*.md"))
    if not commands:
        errors.append("no commands found in commands/")
    checks += 1
    for command in commands:
        checks += 1
        frontmatter = parse_frontmatter(command.read_text(encoding="utf-8"))
        target_agent = frontmatter.get("agent", "")
        agent_path = next(
            (directory / f"{target_agent}.md" for directory in agent_dirs
             if (directory / f"{target_agent}.md").exists()),
            None,
        )
        if not target_agent:
            errors.append(f"command {command.name}: no 'agent:' in frontmatter")
        elif agent_path is None:
            errors.append(
                f"command {command.name}: targets unknown agent '{target_agent}'"
            )

    agents = sorted(agent_file for directory in agent_dirs for agent_file in directory.glob("*.md"))
    if not agents:
        errors.append("no agents found under agents/")
    checks += 1
    for agent in agents:
        checks += 1
        frontmatter = parse_frontmatter(agent.read_text(encoding="utf-8"))
        missing_keys = AGENT_FRONTMATTER_KEYS - frontmatter.keys()
        if missing_keys:
            errors.append(
                f"agent {agent.name}: missing frontmatter key(s): {', '.join(sorted(missing_keys))}"
            )
        mode = frontmatter.get("mode", "")
        if mode and mode not in ("primary", "subagent", "all"):
            errors.append(f"agent {agent.name}: invalid mode '{mode}'")
        tier = frontmatter.get("model_tier", "")
        if tier and tier not in AGENT_TIERS:
            errors.append(
                f"agent {agent.name}: invalid model_tier '{tier}' "
                f"(expected one of {', '.join(AGENT_TIERS)})"
            )

    return errors, checks


def main(argv: list[str] | None = None) -> int:
    errors, checks = validate()

    if errors:
        print(f"FAILED ({len(errors)} error(s) out of {checks} checks):\n")
        for error in errors:
            print(f"  x {error}")
        return 1

    print(f"OK: all {checks} checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
