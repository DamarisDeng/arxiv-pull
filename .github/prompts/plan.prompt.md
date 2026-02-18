# Plan

## Problem statement
Create a structured implementation plan to design Copilot custom agents, skills, and prompts for the "24/7 Q-Bio Watchtower" pipeline (arXiv data fetch -> abstract summarization/ranking -> visual report -> GitHub Pages deploy), scoped strictly to `.github/agents`, `.github/skills`, and `.github/prompts`, targeting deployment to `damarisdeng/arxiv-pull`.

## Proposed agents
- **watchtower-orchestrator.agent.md**: Coordinates the end-to-end pipeline, sequences agent calls, validates artifacts (JSON data, HTML reports), and handles failures.
- **arxiv-ingest.agent.md**: Fetches the latest preprints from the arXiv API targeting `q-bio.QM` (Quantitative Methods), handles pagination, and outputs normalized datasets.
- **paper-analyzer.agent.md**: Analyzes abstracts for key methodologies, generates one-sentence summaries, and ranks papers by relevance to computational biology.
- **report-visualizer.agent.md**: Generates the visual research report (tables + narrative summaries) and assembles the HTML dashboard.
- **pages-deployer.agent.md**: Publishes the dashboard to GitHub Pages for `damarisdeng/arxiv-pull`.

## Skills catalog
- **Orchestration skills**
  - `run_pipeline`: define the execution order and artifact handoffs.
  - `validate_artifacts`: ensure data/report outputs are complete before deploying.
- **Data ingest skills**
  - `fetch_arxiv_papers`: query the API with `search_query=cat:q-bio.QM` and `sortBy=submittedDate`.
  - `parse_arxiv_response`: convert raw Atom/XML responses into structured JSON (title, authors, published_date, pdf_link).
  - `filter_date_range`: strict filtering to ensure only papers from the last 24-48 hours are processed.
- **Analysis skills**
  - `summarize_abstract`: generate concise TL;DRs for technical abstracts.
  - `extract_keywords`: identify specific algorithms or biological models mentioned.

## Workplan
- [ ] Review existing `.github` structure and note missing directories (`agents`, `skills`) while honoring the "no additional code" constraint.
- [ ] Define the agent roster and interaction flow for the pipeline (orchestrator + specialized agents for arXiv fetch, paper analysis, report/visualization, deployment).
- [ ] Draft agent files in `.github/agents` using `<agent-name>.agent.md` with YAML front matter (agent type, model, tools) per Copilot custom agent format.
- [ ] Define skills in `.github/skills` for each step (API retrieval, XML parsing, summarization, HTML generation, GitHub Pages publish).
- [ ] Write prompts in `.github/prompts` to guide each agent/skill, including general coding style instructions and HTML-specific guidelines.

## Notes / considerations
- Only create/update files under `.github/agents`, `.github/skills`, and `.github/prompts`, no source code or other directories.
- Follow the official Copilot custom agents format and include YAML front matter specifying agent type, model, and tools.
- Use the arXiv API as the data source and ensure prompts reflect "no manual coding" expectations.