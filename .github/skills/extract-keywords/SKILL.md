---
name: extract-keywords
description: Identifies up to 5 specific algorithms, statistical methods, or biological models mentioned in an arXiv abstract. Use this skill when enriching each paper in the paper-analyzer step.
---

## Task

Given a scientific abstract, extract up to 5 keywords representing **specific** technical concepts — prioritize named algorithms, named models, and named statistical or computational methods over generic terms.

## Priority Order (extract in this order, up to 5 total)

1. **Named algorithms** — e.g., "UMAP", "Gaussian process regression", "hidden Markov model", "LASSO", "variational autoencoder"
2. **Named biological models** — e.g., "Lotka-Volterra model", "SIR model", "Hill function", "Michaelis-Menten kinetics"
3. **Statistical methods** — e.g., "Bayesian inference", "Monte Carlo simulation", "principal component analysis", "bootstrap"
4. **Computational frameworks** — e.g., "ordinary differential equations", "stochastic simulation", "graph neural network", "dynamic programming"
5. **Biological concepts with quantitative framing** — e.g., "transcriptional noise", "cell fate bifurcation", "phylogenetic reconstruction"

## Formatting Rules

- Each keyword: 1–4 words, title-case (e.g., `"Gaussian Process Regression"`, `"UMAP"`)
- Return as a JSON array of strings, length 0–5
- If fewer than 5 specific technical terms appear in the abstract, return only what is present — do not pad with generic terms like "machine learning" or "biology"

## Examples

**Input:** "...we apply variational autoencoders and UMAP to single-cell RNA-seq data, using a negative binomial likelihood..."
**Output:** `["Variational Autoencoder", "UMAP", "Negative Binomial Likelihood", "Single-Cell RNA-seq"]`
