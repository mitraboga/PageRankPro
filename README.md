<div align="center">

# 🌐 PageRankPro 📊

### Production-Grade Search Ranking Sim using Markov Chains, Random Walks & Graph Intelligence

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?logo=python">
  <img src="https://img.shields.io/badge/Artificial%20Intelligence-CS50AI-red">
  <img src="https://img.shields.io/badge/Graphs-NetworkX-orange?logo=networkx">
  <img src="https://img.shields.io/badge/Visualization-Matplotlib-green?logo=plotly">
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit">
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker">
  <img src="https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?logo=githubactions">
  <img src="https://img.shields.io/badge/Pytest-Tested-0A9EDC?logo=pytest">
  <img src="https://img.shields.io/badge/Playwright-E2E%20Testing-2EAD33?logo=playwright">
  <img src="https://img.shields.io/badge/Sentry-Observability-362D59?logo=sentry">
</p>

</div>

---

# 📖 Executive Summary

**PageRankPro** is a production-style implementation of the famous PageRank algorithm originally used by search engines to determine the importance of web pages.

The system crawls interconnected HTML pages, constructs a directed web graph, simulates probabilistic web surfing behaviour, computes ranking scores using both random sampling and iterative convergence, and visualizes the structure of the web graph.

Instead of remaining a simple academic assignment, PageRankPro expands the original CS50AI project into a modern engineering-grade platform with:

- Interactive graph analytics
- Algorithm comparison dashboards
- Convergence tracking
- Dockerized deployment
- CI/CD automation
- Structured logging
- Error monitoring
- End-to-end browser testing
- Streamlit-based visualization tooling

The result is a complete AI + systems engineering project that demonstrates:

- Probabilistic reasoning
- Markov chains
- Random walks
- Graph-based intelligence
- Algorithm convergence
- Visualization engineering
- Production-grade software development practices

---

# 🎯 Problem Statement

Search engines face one critical challenge:

> Out of millions of interconnected pages, which ones are actually important?

A webpage should not rank highly simply because it exists.

Its importance should depend on:

1. How many pages link to it
2. The quality of those linking pages
3. The structure of the surrounding web graph
4. The probability that a random user eventually lands on it

PageRankPro solves this problem by modelling the internet as a probabilistic directed graph.

The platform computes long-term visitation probabilities across linked pages and uses those probabilities to estimate page authority.

---

# 🧠 How PageRank Works

PageRankPro simulates the behaviour of a **random web surfer**.

At every step, the surfer has two choices:

1. Follow one of the current page's links
2. Randomly jump to another page

This behaviour is controlled using a **damping factor**.

Example:

```text
85% chance → follow a hyperlink
15% chance → jump to a random page
```

Over time, some pages receive more visits than others.

Those pages become more important.

That long-term probability distribution becomes the final **PageRank score**.

---

# ⚙️ Core System Workflow

## 1. Corpus Crawling

The system scans a directory of HTML files.

Example:

```text
corpus/
├── 1.html
├── 2.html
├── 3.html
└── 4.html
```

Each file is parsed using BeautifulSoup to detect hyperlinks.

---

## 2. Graph Construction

The discovered links are transformed into a directed graph.

```text
A.html → B.html
A.html → C.html
B.html → D.html
```

Pages become nodes.

Hyperlinks become directed edges.

---

## 3. Transition Model

The transition model calculates the probability of moving from one page to another.

The model combines:

- Hyperlink-following probability
- Random-jump probability

This prevents the system from becoming trapped in dead-end pages.

---

## 4. Sampling-Based PageRank

The system performs thousands of simulated random walks.

Each page visit is counted.

Higher visitation frequency produces a higher estimated PageRank.

---

## 5. Iterative PageRank

The iterative algorithm repeatedly updates ranking values until convergence.

The system stops when PageRank values stabilize below a configurable tolerance threshold.

---

## 6. Visualization & Analysis

PageRankPro visualizes:

- Directed web graphs
- Node importance
- Rank distributions
- Convergence behavior
- Sampling vs iteration comparisons

---

# 🚀 Key Features

## 🔗 Web Corpus Crawling

- Parses interconnected HTML pages
- Detects internal hyperlinks
- Automatically constructs the web graph

---

## 📊 Directed Graph Intelligence

- Builds graph structures using NetworkX
- Models web relationships as directed edges
- Enables visual graph analytics

---

## 🎲 Random Sampling Simulation

- Simulates thousands of random surfer transitions
- Approximates PageRank through probabilistic sampling
- Demonstrates Monte Carlo estimation concepts

---

## 🔄 Iterative Convergence Engine

- Implements iterative PageRank updates
- Tracks convergence deltas over time
- Produces mathematically stable rankings

---

## 📈 Interactive Visualization Dashboard

The Streamlit dashboard includes:

- Graph visualization
- Ranking comparison tables
- Convergence charts
- Damping-factor experiments
- Page-level ranking explanations
- Algorithm analytics

---

## 🧪 Production Testing Infrastructure

Includes:

- Unit tests
- Integration tests
- End-to-end browser tests
- CI/CD validation pipelines
- Docker runtime verification

---

## 🐳 Dockerized Deployment

PageRankPro can run entirely inside containers.

Features include:

- Dockerfile configuration
- Docker Compose orchestration
- Health checks
- Environment-based configuration

---

## 📡 Observability & Monitoring

Production-grade runtime features:

- Structured JSON logging
- Runtime diagnostics
- Optional Sentry integration
- Error visibility and monitoring

---

# 🧠 CS50AI Concepts Applied

| CS50AI Concept | How PageRankPro Uses It |
|---|---|
| Probability | Models the likelihood of moving between pages |
| Markov Chains | Represents browsing as probabilistic state transitions |
| Random Sampling | Estimates rank through simulated random walks |
| Iterative Algorithms | Recalculates values until convergence |
| Graph Representation | Models pages as nodes and links as directed edges |
| Optimization | Stops iteration when ranks stabilize |
| Uncertainty | Handles probabilistic jumps and random movement |
| Search Intelligence | Simulates ranking logic inspired by search engines |

---

# 🧪 AI & Mathematical Concepts Used

PageRankPro focuses on **classical AI** and probabilistic intelligence.

## Concepts Used

- Markov Chains
- Random Walks
- Probability Distributions
- Directed Graph Theory
- Monte Carlo Sampling
- Iterative Optimization
- Convergence Analysis
- Network Centrality
- Stochastic Transitions

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| BeautifulSoup | HTML parsing and link extraction |
| NetworkX | Directed graph modeling |
| Matplotlib | Graph visualization |
| Streamlit | Interactive dashboard UI |
| Pytest | Automated testing |
| Playwright | End-to-end browser testing |
| Docker | Containerization |
| GitHub Actions | CI/CD automation |
| Sentry | Error monitoring |
| Ruff | Linting and static analysis |

---

# 🏗️ System Architecture

```text
                ┌────────────────────┐
                │ HTML Corpus Input  │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │  Corpus Crawler    │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Directed Web Graph │
                └─────────┬──────────┘
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
┌──────────────────┐          ┌────────────────────┐
│ Sampling Engine  │          │ Iteration Engine   │
└─────────┬────────┘          └─────────┬──────────┘
          ▼                               ▼
 ┌─────────────────┐          ┌────────────────────┐
 │ Rank Estimation │          │ Rank Convergence   │
 └─────────┬───────┘          └─────────┬──────────┘
           └──────────────┬─────────────┘
                          ▼
                ┌────────────────────┐
                │ Visualization Layer│
                └─────────┬──────────┘
                          ▼
                ┌────────────────────┐
                │ Streamlit Dashboard│
                └────────────────────┘
```

---

# 📂 Project Structure

```text
PageRankPro/
│
├── app.py
├── pagerankpro.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── docker-compose.yml
│
├── corpus/
│   ├── corpus0/
│   └── corpus1/
│
├── docs/
│   ├── deployment.md
│   └── project-scope.md
│
├── src/
│   └── pagerankpro/
│       ├── cli.py
│       ├── core.py
│       ├── observability.py
│       └── visualization.py
│
└── tests/
    ├── e2e/
    ├── integration/
    └── unit/
```

---

# ⚡ Installation

## Clone the Repository

```bash
git clone https://github.com/yourusername/PageRankPro.git
cd PageRankPro
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

---

## Activate Environment

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

## Install Development Dependencies

```bash
python -m pip install -r requirements-dev.txt
python -m pip install -e ".[dev,dashboard]"
```

---

# ▶️ Running the Project

## CLI Mode

```bash
python pagerankpro.py corpus/corpus0
```

---

## Generate Graph Visualizations

```bash
python pagerankpro.py corpus/corpus0 --graph-out reports/corpus0.png
```

---

## Custom Parameters

```bash
python pagerankpro.py corpus/corpus0 --damping 0.85 --samples 10000 --seed 42 --tolerance 0.001
```

---

# 🌐 Streamlit Dashboard

Launch the dashboard:

```bash
streamlit run app.py
```

Dashboard Features:

- Interactive graph rendering
- Sampling vs iteration comparison
- Rank tables
- Damping-factor experiments
- Convergence analysis
- Node importance visualization
- Page-level analytics

---

# 🐳 Docker Deployment

Run the entire platform in containers:

```bash
docker compose up --build
```

Open the dashboard:

```text
http://127.0.0.1:8510
```

---

# 🔄 CI/CD Pipeline

PageRankPro includes a production-style GitHub Actions pipeline.

The pipeline automatically performs:

- Linting
- Unit testing
- Integration testing
- End-to-end browser testing
- Docker build validation
- Dependency verification

---

# 🧪 Testing

## Run Unit & Integration Tests

```bash
python -m pytest tests/unit tests/integration
```

---

## Run Full Test Suite

```bash
python -m playwright install chromium
python -m pytest
```

---

## Run Linting

```bash
python -m ruff check .
```

---

# 📈 Example Output

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

Sampling values may vary depending on:

- Random seed
- Sample count
- Corpus structure

---

# 📊 Production Enhancements

The original CS50AI assignment was expanded with modern software engineering practices.

## Added Production Features

| Enhancement | Purpose |
|---|---|
| Docker Support | Containerized deployment |
| Docker Compose | Multi-service orchestration |
| GitHub Actions | Automated CI/CD |
| Structured Logging | Production diagnostics |
| Sentry Monitoring | Error tracking and observability |
| Streamlit Hosting | Interactive deployed dashboard |
| Playwright Testing | Browser-level end-to-end validation |
| Modular Architecture | Cleaner maintainability |
| Convergence Tracking | Advanced analytics |
| Visualization Engine | Graph intelligence rendering |

---

# 📚 Learning Outcomes

PageRankPro demonstrates practical understanding of:

- Search engine ranking systems
- Probabilistic AI systems
- Markov processes
- Graph-based intelligence
- Convergence algorithms
- Visualization engineering
- Production deployment workflows
- Software observability
- CI/CD automation
- Testing infrastructure

---

# 💼 Resume Bullet

> Built PageRankPro, a production-grade search ranking simulator that models webpage authority using Markov chains, random walks, damping factors, and iterative convergence, featuring graph visualization, Streamlit analytics, Dockerized deployment, CI/CD automation, and end-to-end testing.

---

# 👤 Author

<p align="center">
  <b>Mitra Boga</b><br><br>
  <a href="https://www.linkedin.com/in/bogamitra/">
    <img src="https://img.shields.io/badge/LinkedIn-Mitra_Boga-blue?logo=linkedin">
  </a>
  <a href="https://x.com/techtraboga">
    <img src="https://img.shields.io/badge/X-@techtraboga-black?logo=x">
  </a>
</p>

---

# 📜 License

This project is licensed under the MIT License.

````
