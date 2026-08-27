#!/usr/bin/env python3
"""Synchronize framework-managed files in a bootstrapped consumer project.

Usage:
    python scripts/sync_framework.py [TARGET] [--apply]

TARGET defaults to the current directory. Without --apply this only reports
the status of each framework-managed file. Project-owned files (conductor.yaml,
docs/, .github/) are never touched.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from bootstrap_project import (
    SOURCE_ROOT,
    build_manifest,
    is_agent_destination,
    load_default_tiers,
    parse_model_tiers,
    render_agent,
)

MANAGED_PREFIXES = (
    ".opencode/agent/",
    ".opencode/command/",
    ".conductor/",
    "templates/artifacts/",
)
MANAGED_EXACT = {".opencode/opencode.json"}

STATUS_UP_TO_DATE = "up-to-date"
STATUS_DIFFERS = "differs"
STATUS_MISSING = "missing"
STATUS_LOCAL_ONLY = "local-only"


def managed_entries() -> list[tuple[Path, str]]:
    return [
        (src, destination)
        for src, destination in build_manifest()
        if destination.startswith(MANAGED_PREFIXES) or destination in MANAGED_EXACT
    ]


def target_tiers(target: Path) -> dict[str, str]:
    project_yaml = target / "conductor.yaml"
    if project_yaml.is_file():
        return parse_model_tiers(project_yaml.read_text(encoding="utf-8"))
    return load_default_tiers()


def expected_content(source: Path, destination: str, tiers: dict[str, str]) -> bytes:
    if is_agent_destination(destination):
        return render_agent(source, tiers).encode("utf-8")
    return source.read_bytes()


def files_match(source: Path, destination: str, target_file: Path, tiers: dict[str, str]) -> bool:
    return expected_content(source, destination, tiers) == target_file.read_bytes()


def inspect(target: Path) -> tuple[list[tuple[str, str]], int]:
    statuses: list[tuple[str, str]] = []
    managed_destinations = {destination for _, destination in managed_entries()}
    tiers = target_tiers(target)

    for source, destination in managed_entries():
        target_file = target / destination
        if not target_file.exists():
            statuses.append((STATUS_MISSING, destination))
        elif files_match(source, destination, target_file, tiers):
            statuses.append((STATUS_UP_TO_DATE, destination))
        else:
            statuses.append((STATUS_DIFFERS, destination))

    local_only = 0
    for prefix in MANAGED_PREFIXES:
        directory = target / prefix.rstrip("/")
        if not directory.is_dir():
            continue
        for existing in directory.rglob("*"):
            if not existing.is_file():
                continue
            relative = existing.relative_to(target).as_posix()
            if relative not in managed_destinations:
                statuses.append((STATUS_LOCAL_ONLY, relative))
                local_only += 1

    return statuses, local_only


def print_report(statuses: list[tuple[str, str]], project_owned_note: bool) -> None:
    icons = {
        STATUS_UP_TO_DATE: "=",
        STATUS_DIFFERS: "~",
        STATUS_MISSING: "-",
        STATUS_LOCAL_ONLY: "?",
    }
    for status, path in sorted(statuses, key=lambda item: item[1]):
        print(f"  {icons[status]} [{status:>10}] {path}")

    counts: dict[str, int] = {}
    for status, _path in statuses:
        counts[status] = counts.get(status, 0) + 1
    print()
    for status in (STATUS_UP_TO_DATE, STATUS_DIFFERS, STATUS_MISSING, STATUS_LOCAL_ONLY):
        if counts.get(status):
            print(f"  {counts[status]} {status}")
    if project_owned_note:
        print("\n  conductor.yaml, docs/ and .github/ are project-owned and never synchronized.")


def apply_updates(target: Path) -> tuple[int, int]:
    updated = 0
    restored = 0
    tiers = target_tiers(target)
    for source, destination in managed_entries():
        target_file = target / destination
        if target_file.exists() and files_match(source, destination, target_file, tiers):
            continue
        target_file.parent.mkdir(parents=True, exist_ok=True)
        action = "restored" if not target_file.exists() else "updated"
        target_file.write_bytes(expected_content(source, destination, tiers))
        print(f"  {'+' if action == 'restored' else '~'} [{action:>8}] {destination}")
        if action == "restored":
            restored += 1
        else:
            updated += 1
    return updated, restored


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Synchronize framework-managed files in a bootstrapped consumer project."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="bootstrapped project directory (default: current directory)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="update differing and missing framework files (local changes are overwritten)",
    )
    args = parser.parse_args(argv)

    target = Path(args.target).resolve()

    if not (target / ".opencode").is_dir():
        print(
            f"error: {target} does not look like a bootstrapped conductor project "
            "(no .opencode directory); run bootstrap_project.py first",
            file=sys.stderr,
        )
        return 1

    statuses, _local_only_count = inspect(target)
    print(f"Framework-managed files in {target}\n")
    print_report(statuses, project_owned_note=True)

    if not args.apply:
        print("\nRun with --apply to update differing and missing files.")
        return 0

    print("\nApplying updates:")
    updated, restored = apply_updates(target)
    print(f"\nDone: {updated} updated, {restored} restored.")
    print("Review the result with 'git diff' before committing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
