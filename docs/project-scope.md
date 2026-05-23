# PageRankPro - Total Project Scope

## Project Identity

Project Name: PageRankPro

Category: Artificial Intelligence / Search Ranking / Graph Algorithms / Interactive SaaS Dashboard

Core Algorithm: PageRank

Main CS50AI Topic: Probability

Secondary Topics: Graphs, Markov Chains, Sampling, Iteration, Convergence, Software Engineering, Deployment

Final Output: A production-ready PageRank simulator with a CLI, Streamlit dashboard, Docker runtime, CI/CD, structured logging, error monitoring hooks, hosted deployment support, and automated tests.

## Problem This Project Solves

Search engines need to decide which pages are most important. A page is not important just because it exists. It becomes important when other pages link to it, important pages link to it, it sits in a strong part of the web graph, and a random user is likely to land on it over time.

PageRankPro solves this problem:

Given a collection of connected web pages, determine which pages are most important using link-based probability, graph structure, and iterative ranking algorithms.

## Core Product Goal

PageRankPro turns the classic CS50AI PageRank assignment into a complete interactive product.

Instead of only calculating ranks in the terminal, the project lets users:

- Build or upload a mini web corpus.
- Visualize page links as a directed graph.
- Run sampling-based PageRank.
- Run iterative PageRank.
- Compare both algorithms.
- Adjust damping and sampling settings.
- Inspect convergence behavior.
- Understand why each page ranked where it did.
- Export ranking results and reports.

## How PageRankPro Works

PageRankPro takes a corpus of HTML pages and extracts links between pages.

Example:

```text
corpus/
├── 1.html
├── 2.html
├── 3.html
└── 4.html
```

The system then:

1. Crawls the corpus.
2. Parses internal HTML links.
3. Builds a directed graph.
4. Builds a transition probability model.
5. Handles dead-end pages by treating them as linking to every page.
6. Calculates PageRank with random sampling.
7. Calculates PageRank with iterative convergence.
8. Compares the two methods.
9. Visualizes the graph and ranking output.
10. Generates downloadable CSV, JSON, and PNG outputs.

## AI and Algorithmic Concepts

PageRankPro uses classical AI and search-ranking concepts rather than deep learning.

| Concept | How PageRankPro Uses It |
|---|---|
| Probability | Models the likelihood of a user moving from one page to another |
| Markov Chains | Represents browsing as state transitions between pages |
| Random Walks | Simulates a user moving through the graph over many steps |
| Sampling | Estimates rank from visit frequency |
| Iterative Algorithms | Updates rank values repeatedly until convergence |
| Graph Representation | Models pages as nodes and hyperlinks as directed edges |
| Optimization | Stops iteration when rank changes fall below a tolerance |
| Uncertainty | Uses damping and random jumps to model uncertain browsing behavior |

## User-Facing Dashboard Scope

The Streamlit dashboard is the primary product interface. It is designed so users can operate and test the project without using the terminal.

Dashboard capabilities:

- Select built-in sample corpora.
- Upload `.html`, `.htm`, or `.zip` corpora.
- Build a graph manually inside the UI.
- Optionally load a server-side corpus folder.
- Adjust damping factor.
- Adjust sampling steps.
- Adjust random seed.
- Run self-checks from the sidebar.
- View high-level metrics.
- View a rank-weighted directed graph.
- View a full ranking table.
- Compare sampling and iteration results.
- Track convergence over time.
- Read structured ranking analysis cards for every page.
- Download ranking CSV.
- Download final report JSON.
- Download graph PNG.

Dashboard visual identity:

- Green, yellow, blue, and purple color scheme.
- Styled sidebar controls.
- Styled header.
- Colored metric cards.
- Custom graph and chart colors.
- Responsive ranking analysis cards.

## CLI Scope

The CLI remains available for automation, grading, scripting, and reproducible command-line runs.

Example:

```bash
python pagerankpro.py corpus/corpus0
```

CLI capabilities:

- Run PageRank against a corpus folder.
- Configure damping factor.
- Configure sampling count.
- Configure random seed.
- Configure convergence tolerance.
- Export graph visualization as PNG.
- Print sampling results.
- Print iterative results.
- Print algorithm comparison.
- Print top-ranked page and explanation.
- Emit structured JSON logs.

## Production-Grade Engineering Scope

PageRankPro includes production-oriented software engineering additions beyond the original CS50AI project.

### Project Structure

- Python package under `src/pagerankpro`.
- Separate core algorithm module.
- Separate CLI module.
- Separate visualization module.
- Separate observability module.
- Streamlit dashboard as the product UI.
- Sample corpora for demonstrations and tests.
- Documentation under `docs`.

### Dependency Management

- `requirements.txt` for runtime and hosted deployment.
- `requirements-dev.txt` for local development, linting, and tests.
- `pyproject.toml` for package metadata, pytest config, and Ruff config.

### Docker

Docker support includes:

- `Dockerfile` for containerized production runtime.
- `docker-compose.yml` for local container usage.
- Health check against Streamlit's health endpoint.
- Runtime environment variables for logging and monitoring.

### CI/CD

GitHub Actions workflow includes:

- Python setup.
- Dependency installation.
- Ruff linting.
- Unit tests.
- Integration tests.
- CLI smoke test.
- Playwright browser end-to-end tests.
- Docker image build validation.

### Structured Logging

The app emits JSON logs for important runtime events:

- CLI run started.
- CLI run completed.
- CLI run failed.
- Dashboard run completed.
- Dashboard run failed.
- Logging configured.

This makes logs easier to inspect in Docker, CI, Streamlit Cloud, and production log pipelines.

### Error Monitoring

Optional Sentry integration is included.

The app activates Sentry when `SENTRY_DSN` is provided through environment variables or hosted deployment secrets.

Supported environment variables:

```bash
APP_ENV=production
PAGERANKPRO_LOG_LEVEL=INFO
SENTRY_DSN=https://examplePublicKey@o0.ingest.sentry.io/0
SENTRY_TRACES_SAMPLE_RATE=0.0
SENTRY_PROFILES_SAMPLE_RATE=0.0
```

### Hosted Deployment

The dashboard is prepared for Streamlit Community Cloud.

Deployment-ready files:

- `app.py`
- `requirements.txt`
- `.streamlit/config.toml`
- `.streamlit/secrets.toml.example`
- `docs/deployment.md`

Hosted deployment flow:

1. Push the repository to GitHub.
2. Create a Streamlit Community Cloud app.
3. Select `app.py` as the entrypoint.
4. Configure secrets such as `SENTRY_DSN`.
5. Deploy the dashboard.

## Testing Scope

The test suite is split by responsibility.

| Test Type | Purpose |
|---|---|
| Unit tests | Validate PageRank math, crawling, transition models, normalization, and logging |
| Integration tests | Validate the CLI against a sample corpus |
| End-to-end tests | Launch the Streamlit dashboard and verify browser-visible workflows |
| Smoke tests | Validate CLI and Docker runtime behavior |

Primary commands:

```bash
python -m ruff check .
python -m pytest
docker build -t pagerankpro:ci .
```

## Expected Outputs

PageRankPro produces:

- Sampling PageRank results.
- Iterative PageRank results.
- Top-ranked page.
- Algorithm comparison table.
- Rank-weighted graph visualization.
- Convergence chart.
- Ranking analysis cards.
- Downloadable CSV report.
- Downloadable JSON report.
- Downloadable PNG graph.

## Final Project Deliverable

The final deliverable is a complete, production-ready web-ranking simulator that demonstrates PageRank through both algorithmic correctness and an interactive user experience.

It is suitable as:

- A CS50AI enhanced final project.
- A portfolio AI/search-ranking project.
- A graph algorithms demonstration.
- A Streamlit SaaS-style dashboard.
- A deployable Python product with CI, Docker, observability, and browser tests.

## Resume Bullet

Built PageRankPro, a production-ready Python and Streamlit search-ranking simulator that models web-page authority with Markov chains, random walks, damping factors, iterative convergence, graph visualizations, structured analysis cards, Docker deployment, CI/CD, JSON logging, Sentry monitoring hooks, and Playwright end-to-end testing.
