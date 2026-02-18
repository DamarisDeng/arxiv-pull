# 24/7 Q-Bio Watchtower — Implementation Plan

## Problem Statement

Build a "24/7 Q-Bio Watchtower" pipeline using GitHub Copilot custom agents, skills, and prompts,
scoped strictly to `.github/agents`, `.github/skills`, and `.github/prompts` in the
`damarisdeng/arxiv-pull` repository.

**Pipeline flow (with inline reviews):**
1. arXiv data fetch (`q-bio.QM`) → **review** → 2. abstract summarization/ranking → **review** → 3. visual HTML report → **review** → **final gate review** → 4. GitHub Pages deploy

**Trigger:** GitHub Actions cron — runs once every 24 hours (e.g., `0 6 * * *` UTC, shortly after arXiv's daily update)

---

## File Inventory to Create

### Workflow — `.github/workflows/watchtower.yml`

| File | Purpose |
|------|---------|
| `watchtower.yml` | Cron-triggered GitHub Actions workflow (`0 6 * * *` UTC); invokes the `watchtower-orchestrator` agent via `copilot --agent watchtower-orchestrator`; also supports `workflow_dispatch` for manual runs |

---

### Agents — `.github/agents/*.agent.md`

| File | Role |
|------|------|
| `watchtower-orchestrator.agent.md` | End-to-end coordinator; sequences steps, validates artifacts, handles failures |
| `arxiv-ingest.agent.md` | Fetches `q-bio.QM` papers from arXiv API; paginates; outputs normalized JSON |
| `paper-analyzer.agent.md` | Summarizes abstracts (TL;DR), extracts keywords, ranks by relevance |
| `report-visualizer.agent.md` | Builds HTML dashboard (tables + narrative summaries) |
| `code-reviewer.agent.md` | **Inline + gate reviewer** — audits artifacts against all `.github/prompts/` instructions; called by the orchestrator after *each* step that produces output AND as a final gate before deployment; blocks the pipeline on any violation |
| `pages-deployer.agent.md` | Publishes the dashboard to GitHub Pages |

**Format** (per [custom-agents-configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)):
```markdown
---
name: <kebab-case>
description: <when to use this agent>
tools: ["read", "search", "edit", "execute", ...]  # or omit for all tools
---
<agent instructions in Markdown>
```

---

### Skills — `.github/skills/<skill-name>/SKILL.md`

Each skill gets its own subdirectory containing a `SKILL.md` file (mandatory filename).

| Directory | Skill `name` | Purpose |
|-----------|-------------|---------|
| `run-pipeline/` | `run-pipeline` | Define execution order and artifact handoffs across agents |
| `validate-artifacts/` | `validate-artifacts` | Verify JSON data + HTML report are complete before deploying |
| `fetch-arxiv-papers/` | `fetch-arxiv-papers` | Query arXiv API with `search_query=cat:q-bio.QM&sortBy=submittedDate` |
| `parse-arxiv-response/` | `parse-arxiv-response` | Convert Atom/XML response → structured JSON (title, authors, date, pdf_link) |
| `filter-date-range/` | `filter-date-range` | Keep only papers from the last 24–48 hours |
| `summarize-abstract/` | `summarize-abstract` | Generate concise TL;DR from a technical abstract |
| `extract-keywords/` | `extract-keywords` | Identify algorithms/biological models mentioned in an abstract |

**Format:**
```markdown
---
name: <skill-name>
description: <what it does and when Copilot should use it>
---
<instructions, examples, guidelines>
```

---

### Prompts — `.github/prompts/*.prompt.md`

| File | Purpose |
|------|---------|
| `coding-style.prompt.md` | General coding/output style instructions (no manual coding; prefer declarative, readable outputs) |
| `arxiv-ingest.prompt.md` | Detailed behavioral guidance for the arXiv ingest step |
| `paper-analysis.prompt.md` | Guidance for abstract summarization and relevance ranking |
| `report-generation.prompt.md` | HTML/CSS style guidelines for the visual dashboard |
| `pages-deploy.prompt.md` | Steps and constraints for GitHub Pages publishing |

---

## Todos

1. **Review existing `.github` structure** — confirm `agents/` and `skills/` dirs exist and are empty
2. **Create `.github/workflows/watchtower.yml`** — daily cron + `workflow_dispatch` trigger
3. **Create 6 agent files** in `.github/agents/` (includes new `code-reviewer`)
4. **Create 7 skill subdirs + SKILL.md files** in `.github/skills/`
5. **Create 5 prompt files** in `.github/prompts/`

---

## Notes / Constraints

- **No source code outside `.github/`** — strictly `agents`, `skills`, `prompts` directories only.
- Agent files must use YAML frontmatter with `name`, `description`, and optional `tools`.
- Skill directories must be lowercase with hyphens; the single file inside must be named `SKILL.md`.
- Tools for `pages-deployer` and `arxiv-ingest` must include `execute` (shell) to run curl/git commands.
- Tools for `paper-analyzer` and `report-visualizer` can be restricted to `["read", "edit", "search"]`.
- Tools for `code-reviewer` should be read-only: `["read", "search"]` — it audits but does not modify.
- The orchestrator should use `["agent", "read", "search", "edit"]` to delegate to sub-agents.
- Pipeline execution order enforced by the orchestrator:
  ```
  arxiv-ingest → code-reviewer → paper-analyzer → code-reviewer → report-visualizer → code-reviewer (gate) → pages-deployer
  ```
  The orchestrator calls `code-reviewer` after every step that produces output, passing the step's artifact as context. It also calls it one final time as a holistic gate before invoking `pages-deployer`. If any review call reports a violation, the orchestrator halts and does not proceed to the next step.
- Prompts are plain Markdown (no required frontmatter) and are injected as Copilot instructions.
