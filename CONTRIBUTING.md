# Contributing

Contributions are welcome. This guide explains how to contribute to the research-agent-starter-kit.

## How to contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run validation: `python scripts/run_skill_evals.py && python scripts/validate_agent_schemas.py`
5. Commit with a clear message: `git commit -m "Add: description of change"`
6. Push and open a Pull Request

## Adding a new skill

Every new skill must include:

1. **SKILL.md** in `.agents/skills/your-skill-name/SKILL.md` with:
   - Trigger conditions (when should this skill activate)
   - Workflow steps
   - Boundary statements (what this skill does NOT do)

2. **At least 2 eval test cases** registered in `research-wiki/SKILL_EVAL_REGISTRY.md`:
   - One positive case (should trigger)
   - One negative/boundary case (should NOT trigger)

3. **No conflicts** with existing skills — check `research-wiki/SKILL_DEPENDENCY_GRAPH.md`

## Skill naming convention

New skills should use generic prefixes (e.g. `research-*`, `academic-*`, `project-*`) rather than `dissertation-*`. Existing `dissertation-*` skills are kept for backwards compatibility and will be renamed in a future release.

## Code style

- Python: UTF-8 encoding, LF line endings, no BOM
- Markdown: ATX headings (`#`), one blank line between sections
- File names: lowercase with hyphens for skills, underscores for Python scripts

## Commit messages

Use prefixes:

- `Add:` — new feature or file
- `Fix:` — bug fix
- `Update:` — modification to existing content
- `Remove:` — deletion
- `Docs:` — documentation only

## What not to submit

- Personal dissertation content (source notes, ethics forms, proposal text)
- Real names, emails, or institutional details
- API keys, tokens, or credentials
- Generated runtime data (receipts, audit reports, event logs)
