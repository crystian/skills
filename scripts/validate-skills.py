#!/usr/bin/env python3
"""
Validate every SKILL.md under skills/ against the project standard.

Exits 0 if all skills are valid, 1 otherwise.

Rules enforced (see CONTRIBUTING.md / CLAUDE.md for the full spec):
  - SKILL.md exists and starts with YAML frontmatter delimited by ---.
  - Required top-level fields: name, author, license, description, metadata.
  - name is kebab-case (lowercase, hyphens, 1-64 chars) and matches directory name.
  - description is a non-trivial string <= 1024 chars.
  - metadata has required keys (version, tags, github, linkedin).
  - metadata.version is semver (X.Y.Z).
  - Body (after frontmatter) is <= 500 lines.
  - README.md exists alongside SKILL.md.

Directories under skills/ whose name starts with "_" are skipped (templates).

Usage:
  python3 scripts/validate-skills.py
  python3 scripts/validate-skills.py --skills-dir path/to/skills
"""

from __future__ import annotations

import argparse
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "error: PyYAML is required. Install with `pip install pyyaml` "
        "or `apt-get install python3-yaml`.\n"
    )
    sys.exit(2)


MAX_DESCRIPTION = 1024
MIN_DESCRIPTION = 20
MAX_BODY_LINES = 500
NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
REQUIRED_TOP = ["name", "author", "license", "description", "metadata"]
REQUIRED_META = ["version", "tags", "github", "linkedin"]


def validate_skill(skill_dir: str, name: str, errors: list[str]) -> None:
    skill_md = os.path.join(skill_dir, "SKILL.md")
    readme = os.path.join(skill_dir, "README.md")

    if not os.path.isfile(skill_md):
        errors.append(f"[{name}] missing SKILL.md")
        return
    if not os.path.isfile(readme):
        errors.append(f"[{name}] missing README.md")

    with open(skill_md, "r", encoding="utf-8") as fh:
        content = fh.read()

    if not content.startswith("---\n"):
        errors.append(f"[{name}] SKILL.md must start with YAML frontmatter (---)")
        return

    parts = content.split("---\n", 2)
    if len(parts) < 3:
        errors.append(f"[{name}] SKILL.md frontmatter not terminated with ---")
        return

    fm_raw, body = parts[1], parts[2]

    try:
        fm = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError as exc:
        errors.append(f"[{name}] invalid YAML frontmatter: {exc}")
        return

    for key in REQUIRED_TOP:
        if key not in fm:
            errors.append(f"[{name}] missing required frontmatter field: {key}")

    skill_name = str(fm.get("name", ""))
    if not NAME_PATTERN.match(skill_name):
        errors.append(
            f"[{name}] name '{skill_name}' must be lowercase, hyphens only, 1-64 chars"
        )
    if skill_name and skill_name != name:
        errors.append(
            f"[{name}] name '{skill_name}' does not match directory name '{name}'"
        )

    desc = fm.get("description", "")
    if not isinstance(desc, str):
        errors.append(f"[{name}] description must be a string")
    elif len(desc) > MAX_DESCRIPTION:
        errors.append(
            f"[{name}] description is {len(desc)} chars, max {MAX_DESCRIPTION}"
        )
    elif len(desc.strip()) < MIN_DESCRIPTION:
        errors.append(
            f"[{name}] description is too short (< {MIN_DESCRIPTION} chars)"
        )

    meta = fm.get("metadata", {})
    if not isinstance(meta, dict):
        errors.append(f"[{name}] metadata must be an object")
    else:
        for key in REQUIRED_META:
            if key not in meta:
                errors.append(f"[{name}] metadata.{key} is required")
        version = str(meta.get("version", ""))
        if version and not SEMVER_PATTERN.match(version):
            errors.append(
                f"[{name}] metadata.version '{version}' must be semver (X.Y.Z)"
            )

    body_lines = body.count("\n")
    if body_lines > MAX_BODY_LINES:
        errors.append(
            f"[{name}] body is {body_lines} lines, max {MAX_BODY_LINES} "
            f"(move overflow to references/)"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SKILL.md files.")
    parser.add_argument(
        "--skills-dir",
        default="skills",
        help="Directory containing skills (default: skills).",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.skills_dir):
        print(f"No {args.skills_dir}/ directory — nothing to validate.")
        return 0

    errors: list[str] = []
    validated = 0
    skipped = 0

    for entry in sorted(os.listdir(args.skills_dir)):
        skill_dir = os.path.join(args.skills_dir, entry)
        if not os.path.isdir(skill_dir):
            continue
        if entry.startswith("_"):
            print(f"Skipping {entry} (private/template)")
            skipped += 1
            continue
        validate_skill(skill_dir, entry, errors)
        validated += 1

    if errors:
        print("\n=== Validation errors ===")
        for err in errors:
            print(f"  - {err}")
        print(f"\n{len(errors)} error(s) found across {validated} skill(s).")
        return 1

    print(f"All {validated} skill(s) valid ({skipped} skipped).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
