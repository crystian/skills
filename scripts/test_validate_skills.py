from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate-skills.py")
SPEC = importlib.util.spec_from_file_location("validate_skills", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Could not load validate-skills.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class BodyLineLimitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Path(".tmp").mkdir(exist_ok=True)

    def write_skill(self, root: Path, body_lines: int) -> Path:
        skill_dir = root / "boundary-skill"
        skill_dir.mkdir()
        frontmatter = """---
name: boundary-skill
author: Test Author
license: MIT
description: Validates the exact body line boundary for contributed skills.
metadata:
  version: 0.1.0
  tags: validation, testing
  github: https://github.com/example/skills
  linkedin: https://www.linkedin.com/in/example
---
"""
        body = "\n".join(f"line {index}" for index in range(body_lines))
        (skill_dir / "SKILL.md").write_text(frontmatter + body, encoding="utf-8")
        (skill_dir / "README.md").write_text("# Boundary Skill\n", encoding="utf-8")
        return skill_dir

    def test_accepts_exactly_500_lines_without_trailing_newline(self) -> None:
        with tempfile.TemporaryDirectory(dir=".tmp") as directory:
            skill_dir = self.write_skill(Path(directory), 500)
            errors: list[str] = []
            VALIDATOR.validate_skill(str(skill_dir), "boundary-skill", errors)

        self.assertEqual(errors, [])

    def test_rejects_501_lines_without_trailing_newline(self) -> None:
        with tempfile.TemporaryDirectory(dir=".tmp") as directory:
            skill_dir = self.write_skill(Path(directory), 501)
            errors: list[str] = []
            VALIDATOR.validate_skill(str(skill_dir), "boundary-skill", errors)

        self.assertEqual(
            errors,
            ["[boundary-skill] body is 501 lines, max 500 (move overflow to references/)"],
        )


if __name__ == "__main__":
    unittest.main()
