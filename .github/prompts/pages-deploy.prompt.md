# GitHub Pages Deployment Instructions

These instructions guide the `pages-deployer` agent when committing and publishing the dashboard.

## Pre-Deployment Requirements

Before running any git commands, confirm all of the following:
1. `docs/index.html` exists and contains `<!DOCTYPE html>`
2. `data/papers.json` exists and is valid JSON
3. `data/analysis.json` exists and is valid JSON
4. The `code-reviewer` has issued `REVIEW RESULT: PASS` for this pipeline run

If any requirement is not met, **do not proceed** — report which requirement failed.

## Git Operations

> Git commit, push, and GitHub Pages deployment are handled by the GitHub Actions workflow (`.github/workflows/watchtower.yml`), **not** by the agent. The agent's job is pre-flight validation only.

The workflow will:
- Stage `docs/index.html`, `data/papers.json`, `data/analysis.json`
- Commit with message: `chore: watchtower update YYYY-MM-DD UTC`
- Push to `origin main`
- Deploy to GitHub Pages via `actions/deploy-pages`

## GitHub Pages Configuration

- The site is served from the `docs/` folder on the `main` branch
- Published URL: `https://damarisdeng.github.io/arxiv-pull/`
- GitHub Pages will automatically pick up `docs/index.html` after the push

## Post-Deployment Report

After a successful push, output:
```
[pages-deployer] Deployed successfully.
Commit: <SHA>
URL: https://damarisdeng.github.io/arxiv-pull/
Timestamp: <UTC datetime>
```
