# PageRankPro

PageRankPro is a production-ready CS50AI-style PageRank simulator. It crawls a folder of linked HTML pages, builds a directed web graph, ranks pages with both random sampling and iterative convergence, compares the results, and visualizes the graph.

## Problem

Search engines need to decide which pages matter most. A page becomes important when other pages link to it, especially when those linking pages are important themselves. PageRankPro models that idea with probability, Markov chains, random walks, graph representation, and iterative optimization.

## Features

- Crawls local HTML corpora and extracts internal links.
- Builds a transition model with configurable damping.
- Computes PageRank using random sampling.
- Computes PageRank using iterative convergence.
- Handles dead-end pages by treating them as linking to every page.
- Compares sampling and iteration side by side.
- Tracks convergence deltas for the iterative algorithm.
- Exports graph visualizations with rank-weighted node sizes.
- Includes a Streamlit dashboard for interactive experimentation.
- Includes pytest coverage for core algorithm behavior.

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| BeautifulSoup | HTML link parsing |
| NetworkX | Directed graph construction |
| Matplotlib | Graph visualization |
| Streamlit | Interactive dashboard |
| Pytest | Automated correctness checks |

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

For editable package development:

```bash
python -m pip install -r requirements-dev.txt
python -m pip install -e ".[dev,dashboard]"
```

## CLI Usage

Run the compatibility script:

```bash
python pagerankpro.py corpus/corpus0
```

Or, after editable installation:

```bash
pagerankpro corpus/corpus0
```

Generate a graph image:

```bash
python pagerankpro.py corpus/corpus0 --graph-out reports/corpus0.png
```

Useful options:

```bash
python pagerankpro.py corpus/corpus0 --damping 0.85 --samples 10000 --seed 42 --tolerance 0.001
```

## Dashboard

```bash
streamlit run app.py
```

The dashboard shows the web graph, ranking table, sampling vs iteration chart, damping-factor experiment, convergence chart, and page-level ranking explanations.

## Production Runtime

PageRankPro includes production-facing project infrastructure:

- Docker image with health checks.
- Docker Compose for local container runs.
- GitHub Actions CI for linting, unit tests, integration tests, browser tests, and Docker build validation.
- JSON structured logging for CLI and dashboard runtime events.
- Optional Sentry error monitoring through `SENTRY_DSN`.
- Streamlit Community Cloud configuration and secrets template.
- Playwright-backed end-to-end tests for the dashboard.

Run with Docker:

```bash
docker compose up --build
```

Then open:

```text
http://127.0.0.1:8510
```

See [docs/deployment.md](docs/deployment.md) for hosted deployment and operations details.

## Testing

Run the fast test suite:

```bash
python -m pytest tests/unit tests/integration
```

Run all tests, including dashboard browser tests:

```bash
python -m playwright install chromium
python -m pytest
```

Run linting:

```bash
python -m ruff check .
```

## Expected Output

```text
PageRank Results from Sampling
1.html: 0.1201
2.html: 0.3714
3.html: 0.3786
4.html: 0.1299

PageRank Results from Iteration
1.html: 0.1289
2.html: 0.3710
3.html: 0.3710
4.html: 0.1291

Top Page: 2.html
```

Exact sampling values can vary with sample count and random seed.

## Project Structure

```text
PageRankPro/
├── app.py
├── pagerankpro.py
├── pyproject.toml
├── requirements.txt
├── corpus/
│   ├── corpus0/
│   └── corpus1/
├── src/
│   └── pagerankpro/
│       ├── cli.py
│       ├── core.py
│       └── visualization.py
└── tests/
    └── test_core.py
```

## CS50AI Concepts Applied

| CS50AI Concept | How PageRankPro Uses It |
|---|---|
| Probability | Models the likelihood of moving from one page to another |
| Markov Chains | Represents browsing as state transitions between pages |
| Random Sampling | Estimates PageRank through simulated random walks |
| Iterative Algorithms | Recalculates ranks until convergence |
| Graph Representation | Models pages as nodes and hyperlinks as directed edges |
| Optimization | Stops iteration when PageRank values stabilize |
| Uncertainty | Handles probabilistic movement and random page jumps |

## Resume Bullet

Built PageRankPro, a Python-based search ranking simulator that models web-page authority using Markov chains, random walks, damping factors, and iterative convergence, with graph visualizations and algorithm comparison tools.
