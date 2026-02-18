# Run End-to-End Pipeline

Run the full Q-Bio Watchtower pipeline for today's arXiv papers.

Execute every step in order, using the `/run-pipeline` skill for sequencing. After each step, invoke the `code-reviewer` agent to audit the output before proceeding. Halt immediately if any review returns FAIL.

## Steps

1. Use the `arxiv-ingest` agent to fetch today's `q-bio.QM` papers → `data/papers.json`
2. Review `data/papers.json` with the `code-reviewer` agent
3. Use the `paper-analyzer` agent to summarize and rank → `data/analysis.json`
4. Review `data/analysis.json` with the `code-reviewer` agent
5. Use the `report-visualizer` agent to build the dashboard → `docs/index.html`
6. Review `docs/index.html` with the `code-reviewer` agent
7. Final gate review of all artifacts with the `code-reviewer` agent
8. Use the `pages-deployer` agent for pre-flight validation

After all steps pass, report a summary of papers fetched, top-ranked paper, and confirmation that artifacts are ready for deployment.
