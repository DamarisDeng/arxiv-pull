# Coding Style Instructions

These instructions apply to all agents and skills in the Q-Bio Watchtower pipeline.

## General Principles

- **No manual hard-coding**: Do not hard-code dates, paper counts, file paths, or API URLs that are already defined in skill files. Always derive dynamic values (e.g., today's date) at runtime.
- **Declarative and readable outputs**: Prefer clear, well-structured outputs over terse or cryptic ones. JSON should be pretty-printed with 2-space indentation. HTML should be indented and readable.
- **Fail loudly**: Never silently swallow errors. If a step fails, report the failure with enough detail to diagnose it.
- **Minimal footprint**: Each agent writes only to its designated output paths. No agent modifies files owned by another agent.

## JSON Output Style

- Pretty-print with 2-space indentation.
- Arrays of objects: one object per logical record, fields in the order defined by the schema.
- Null values are acceptable for missing fields; do not omit fields entirely.
- All string values must be UTF-8 and have leading/trailing whitespace stripped.

## Naming Conventions

- File names: lowercase, hyphen-separated (e.g., `papers.json`, `index.html`)
- JSON field names: `snake_case`
- arXiv IDs: preserve as-is (e.g., `2401.12345v1`)

## Commit Messages

- Format: `chore: watchtower update YYYY-MM-DD UTC`
- No emoji, no issue references unless a bug fix is being committed alongside data.
