# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Versions are bumped automatically by the `bump-version` GitHub Action on each push to `main`. See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

## [Unreleased]

## [1.4.12] – 2026-04-18

### Added

- **docs**: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` for standard open-source layout
- **templates**: `skills/_template/` scaffold with SKILL.md and README.md for new skill contributions
- **ci**: `.github/workflows/validate-skills.yml` linter for SKILL.md files
- **github**: issue templates (bug, feature, new skill proposal) and pull request template
- **tooling**: `scripts/validate-skills.py` for local SKILL.md validation

### Changed

- **docs**: reworked `README.md` with badges, table of contents, and contribution pointers
- **docs**: consolidated project standards and persona activation in `CLAUDE.md`
- **docs**: refreshed `HUMAN.md` with design principles and mental roadmap
- **ci**: updated `bump-version.yml` to skip template skills (directories starting with `_`)
- **build**: expanded `.gitignore` with editor, OS, and Python patterns

## [1.4.11]

- Documentation and metadata polish. See commit history for details.

## [1.4.0] – skill-optimizer rename

- Renamed `skill-sharpen` to `skill-optimizer` — more representative of its kaizen behavior.

---

Older history: see `git log`.
