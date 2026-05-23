# Deployment Guide

This project supports two production-style deployment paths:

1. Streamlit Community Cloud for the public dashboard.
2. Docker for local, staging, or container-hosted environments.

## Streamlit Community Cloud

Use this setup when you want the dashboard hosted as a public Streamlit app.

Required repository files:

- `app.py` as the Streamlit entrypoint.
- `requirements.txt` for Python dependencies.
- `.streamlit/config.toml` for Streamlit runtime configuration.
- `.streamlit/secrets.toml.example` as the template for secrets.

Deployment steps:

1. Push this repository to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app from the GitHub repository.
4. Set the entrypoint file to `app.py`.
5. Paste production secrets in Advanced settings.
6. Deploy the app and use the generated `streamlit.app` URL.

Recommended secrets:

```toml
SENTRY_DSN = "https://examplePublicKey@o0.ingest.sentry.io/0"
APP_ENV = "production"
```

Do not commit `.streamlit/secrets.toml`.

## Docker

Build the image:

```bash
docker build -t pagerankpro:latest .
```

Run the container:

```bash
docker run --rm -p 8510:8501 --env APP_ENV=production pagerankpro:latest
```

Open:

```text
http://127.0.0.1:8510
```

With Docker Compose:

```bash
docker compose up --build
```

## CI/CD

The GitHub Actions workflow in `.github/workflows/ci.yml` runs:

- Dependency installation.
- Ruff linting.
- Unit tests.
- Integration tests.
- CLI smoke test.
- Playwright-backed dashboard end-to-end tests.
- Docker image build validation.

For Streamlit Community Cloud, deployment is GitHub-driven: after CI passes and code is merged to the configured branch, Community Cloud pulls the latest app revision.

## Observability

Runtime logs are JSON-formatted so they are easy to search in Docker logs, CI logs, Streamlit logs, and hosted log pipelines.

Error monitoring is optional and activated with `SENTRY_DSN`.

Environment variables:

```bash
APP_ENV=production
PAGERANKPRO_LOG_LEVEL=INFO
SENTRY_DSN=https://examplePublicKey@o0.ingest.sentry.io/0
SENTRY_TRACES_SAMPLE_RATE=0.0
SENTRY_PROFILES_SAMPLE_RATE=0.0
```

## Health Checks

The Docker image checks:

```text
http://localhost:8501/_stcore/health
```

The end-to-end test suite waits for the same health endpoint before opening the dashboard with Playwright.
