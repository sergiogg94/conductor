#!/usr/bin/env python3
"""Install the conductor framework into a target project repository.

Usage:
    python scripts/bootstrap_project.py [TARGET] [--force] [--dry-run]

TARGET defaults to the current directory.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_SOURCES = [
    "templates/project/conductor.yaml",
    "templates/project/.opencode/opencode.json",
    "templates/project/docs",
    "templates/project/.github",
    "agents/primary",
    "agents/subagents",
    "agents/shared",
    "commands",
    "templates/artifacts",
]

AGENT_DIR = ".opencode/agent"
AGENT_TIERS = ("low", "medium", "high")
CONDUCTOR_YAML = SOURCE_ROOT / "templates/project/conductor.yaml"


def is_agent_destination(destination: str) -> bool:
    return destination.startswith(f"{AGENT_DIR}/")


def parse_frontmatter(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return fields
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        if not line.startswith((" ", "\t")) and ":" in stripped:
            key, _, value = stripped.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def parse_model_tiers(yaml_text: str) -> dict[str, str]:
    tiers: dict[str, str] = {}
    in_tiers = False
    for line in yaml_text.splitlines():
        if line.startswith("model_tiers:"):
            in_tiers = True
            continue
        if in_tiers:
            if not line.startswith((" ", "\t")):
                break
            stripped = line.rstrip()
            if ":" in stripped:
                key, _, value = stripped.partition(":")
                key = key.strip()
                value = value.strip()
                if key:
                    tiers[key] = value
    return tiers


def load_default_tiers() -> dict[str, str]:
    return parse_model_tiers(CONDUCTOR_YAML.read_text(encoding="utf-8"))


def render_agent(source: Path, tiers: dict[str, str]) -> str:
    text = source.read_text(encoding="utf-8")
    in_frontmatter = False
    rendered: list[str] = []
    for line in text.splitlines():
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            rendered.append(line)
            continue
        if in_frontmatter and line.strip().startswith("model_tier:"):
            tier = line.split(":", 1)[1].strip()
            model = tiers.get(tier, "")
            if not model:
                raise ValueError(
                    f"{source.name}: model_tier '{tier}' has no entry in the "
                    "model_tiers map in conductor.yaml"
                )
            rendered.append(f"model: {model}")
            continue
        rendered.append(line)
    return "\n".join(rendered) + ("\n" if text.endswith("\n") else "")


def build_manifest() -> list[tuple[Path, str]]:
    manifest: list[tuple[Path, str]] = []

    manifest.append(
        (
            SOURCE_ROOT / "templates/project/conductor.yaml",
            "conductor.yaml",
        )
    )
    manifest.append(
        (
            SOURCE_ROOT / "templates/project/.opencode/opencode.json",
            ".opencode/opencode.json",
        )
    )

    for group in ("primary", "subagents"):
        for agent_file in sorted((SOURCE_ROOT / "agents" / group).glob("*.md")):
            manifest.append((agent_file, f".opencode/agent/{agent_file.name}"))

    for command_file in sorted((SOURCE_ROOT / "commands").glob("*.md")):
        manifest.append((command_file, f".opencode/command/{command_file.name}"))

    SHARED_EXCLUSIONS = {"agent-template.md"}

    for shared_file in sorted((SOURCE_ROOT / "agents/shared").glob("*.md")):
        if shared_file.name in SHARED_EXCLUSIONS:
            continue
        manifest.append((shared_file, f".conductor/{shared_file.name}"))

    for template_file in sorted((SOURCE_ROOT / "templates/artifacts").glob("*.md")):
        manifest.append(
            (template_file, f"templates/artifacts/{template_file.name}")
        )

    docs_src = SOURCE_ROOT / "templates/project/docs"
    for doc_file in sorted(docs_src.rglob("*")):
        if doc_file.is_file():
            relative = doc_file.relative_to(docs_src)
            manifest.append((doc_file, f"docs/{relative.as_posix()}"))

    github_src = SOURCE_ROOT / "templates/project/.github"
    for gh_file in sorted(github_src.rglob("*")):
        if gh_file.is_file():
            relative = gh_file.relative_to(github_src)
            manifest.append((gh_file, f".github/{relative.as_posix()}"))

    return manifest


def validate_sources(manifest: list[tuple[Path, str]]) -> list[str]:
    problems = []
    for required in REQUIRED_SOURCES:
        if not (SOURCE_ROOT / required).exists():
            problems.append(f"missing framework source: {required}")
    for src, _dst in manifest:
        if not src.is_file():
            problems.append(f"missing file listed in manifest: {src}")
    return problems


def validate_tiers(manifest: list[tuple[Path, str]]) -> list[str]:
    problems: list[str] = []
    if not CONDUCTOR_YAML.exists():
        problems.append(f"missing framework source: {CONDUCTOR_YAML.relative_to(SOURCE_ROOT)}")
        return problems
    tiers = parse_model_tiers(CONDUCTOR_YAML.read_text(encoding="utf-8"))
    for tier in AGENT_TIERS:
        if tier not in tiers:
            problems.append(f"conductor.yaml: model_tiers map is missing tier '{tier}'")
        elif not tiers[tier]:
            problems.append(f"conductor.yaml: model_tiers['{tier}'] is empty")
    for src, destination in manifest:
        if not is_agent_destination(destination):
            continue
        frontmatter = parse_frontmatter(src.read_text(encoding="utf-8"))
        tier = frontmatter.get("model_tier", "")
        if tier not in AGENT_TIERS:
            problems.append(
                f"agent {src.name}: missing or invalid 'model_tier' "
                f"(expected one of {', '.join(AGENT_TIERS)})"
            )
        elif tier not in tiers:
            problems.append(
                f"agent {src.name}: model_tier '{tier}' not defined in conductor.yaml"
            )
    return problems


def apply_manifest(
    manifest: list[tuple[Path, str]], target: Path, force: bool
) -> tuple[list[str], list[str]]:
    created: list[str] = []
    skipped: list[str] = []

    tiers = load_default_tiers()

    for src, destination_relative in manifest:
        destination = target / destination_relative
        if destination.exists() and not force:
            skipped.append(destination_relative)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        if is_agent_destination(destination_relative):
            destination.write_text(render_agent(src, tiers), encoding="utf-8")
        else:
            shutil.copyfile(src, destination)
        created.append(destination_relative)

    return created, skipped


def print_report(
    created: list[str], skipped: list[str], force: bool, dry_run: bool
) -> None:
    action = "Would create" if dry_run else "Created"
    print(f"{action} {len(created)} file(s):")
    for path in created:
        print(f"  + {path}")

    label = "Already present (use --force to overwrite)" if not force else "Overwritten"
    verb = "would skip" if dry_run and not force else ("overwrote" if force else "skipped")
    if skipped:
        print(f"\n{label}: {len(skipped)} file(s) {verb}:")
        for path in skipped:
            print(f"  = {path}")


def print_next_steps(target: Path) -> None:
    print("\nNext steps:")
    print(f"  1. Edit {target / 'conductor.yaml'}: fill in project identity and github.repository/github.projects values.")
    print("     Optionally set concrete models per tier under 'model_tiers' (defaults to opencode/big-pickle).")
    print(f"  2. Start opencode in {target} and confirm the orchestrator loads as default agent.")
    print("  3. Run /discover <idea> to produce your first Discovery artifact.")
    print("  4. Optional: set the ANTHROPIC_API_KEY secret to enable .github/workflows/opencode-review.yml.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Install the conductor framework into a target project repository."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="target project directory (default: current directory)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite existing framework-managed files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would be installed without writing anything",
    )
    args = parser.parse_args(argv)

    target = Path(args.target).resolve()

    if target == SOURCE_ROOT:
        print("error: refusing to bootstrap the conductor repository itself", file=sys.stderr)
        return 1
    if not target.exists():
        print(f"error: target does not exist: {target}", file=sys.stderr)
        return 1

    manifest = build_manifest()
    problems = validate_sources(manifest) + validate_tiers(manifest)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1

    if not (target / ".git").exists():
        print("warning: target is not a git repository; conductor expects a GitHub-hosted repo")

    print(f"Bootstrapping conductor into {target}\n")

    if args.dry_run:
        planned = [
            destination
            for _, destination in manifest
            if not (target / destination).exists() or args.force
        ]
        existing = [
            destination
            for _, destination in manifest
            if (target / destination).exists()
        ]
        print_report(planned, existing, args.force, dry_run=True)
        return 0

    created, skipped = apply_manifest(manifest, target, force=args.force)
    print_report(created, skipped, args.force, dry_run=False)
    print_next_steps(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
