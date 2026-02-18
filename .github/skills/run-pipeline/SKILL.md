---
name: run-pipeline
description: Defines the execution order and artifact handoffs for the Q-Bio Watchtower pipeline. Use this skill when orchestrating or resuming the full pipeline sequence.
---

## Pipeline Execution Order

The Watchtower pipeline runs in the following strict sequence. Each step must complete successfully before the next begins.

| Step | Agent | Input | Output |
|------|-------|-------|--------|
| 1 | `arxiv-ingest` | arXiv API | `data/papers.json` |
| 2 | `code-reviewer` | `data/papers.json` | PASS / FAIL |
| 3 | `paper-analyzer` | `data/papers.json` | `data/analysis.json` |
| 4 | `code-reviewer` | `data/analysis.json` | PASS / FAIL |
| 5 | `report-visualizer` | `data/analysis.json` | `docs/index.html` |
| 6 | `code-reviewer` | `docs/index.html` | PASS / FAIL |
| 7 | `code-reviewer` (gate) | all three artifacts | PASS / FAIL |
| 8 | `pages-deployer` | `docs/index.html` + data files | GitHub Pages live |

## Artifact Handoff Rules

- Each agent writes its output to the agreed file path listed above.
- The orchestrator reads those paths and passes them as context when invoking the next agent.
- If a `code-reviewer` step returns FAIL, the orchestrator halts immediately and does not invoke the next agent.

## Resuming a Failed Run

If the pipeline halted at step N, inspect the FAIL output to fix the violation, then re-run the pipeline from step N (not from step 1), unless the ingest data is stale (older than 24 hours), in which case restart from step 1.
