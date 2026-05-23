"""Streamlit dashboard for PageRankPro."""

from __future__ import annotations

import io
import json
import os
import sys
import zipfile
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from matplotlib.colors import LinearSegmentedColormap

from pagerankpro.core import (
    DEFAULT_DAMPING,
    DEFAULT_SAMPLES,
    crawl,
    explain_rank,
    iterate_pagerank,
    sample_pagerank,
    transition_model,
)
from pagerankpro.observability import configure_logging, init_error_monitoring
from pagerankpro.visualization import build_graph

SAMPLE_CORPORA = {
    "Sample corpus 0": Path("corpus/corpus0"),
    "Sample corpus 1": Path("corpus/corpus1"),
}
THEME_COLORS = {
    "green": "#16a34a",
    "yellow": "#facc15",
    "blue": "#2563eb",
    "purple": "#7c3aed",
    "ink": "#111827",
    "muted": "#64748b",
    "surface": "#ffffff",
    "panel": "#f8fafc",
}
RANK_CMAP = LinearSegmentedColormap.from_list(
    "pagerankpro",
    [THEME_COLORS["blue"], THEME_COLORS["green"], THEME_COLORS["yellow"], THEME_COLORS["purple"]],
)

logger = configure_logging("pagerankpro-dashboard")


def _get_runtime_setting(name: str) -> str | None:
    value = os.getenv(name)
    return value if value else None


st.set_page_config(page_title="PageRankPro", layout="wide")
init_error_monitoring(
    dsn=_get_runtime_setting("SENTRY_DSN"),
    environment=_get_runtime_setting("APP_ENV") or "dashboard",
)


def main() -> None:
    inject_theme()
    render_header()

    with st.sidebar:
        st.markdown("### Controls")
        source_type = st.radio(
            "Corpus source",
            ["Built-in sample", "Upload HTML", "Manual graph", "Server folder"],
        )
        damping = st.slider(
            "Damping factor",
            min_value=0.0,
            max_value=1.0,
            value=DEFAULT_DAMPING,
            step=0.01,
        )
        sample_count = st.number_input(
            "Sampling steps",
            min_value=100,
            max_value=1_000_000,
            value=DEFAULT_SAMPLES,
            step=1_000,
        )
        seed = st.number_input("Random seed", min_value=0, value=42, step=1)

        st.divider()
        if st.button("Run self-checks", use_container_width=True):
            show_self_check_results()

    corpus = load_corpus_from_ui(source_type)
    if not corpus:
        st.info("Create, upload, or select a corpus to run PageRank.")
        return

    try:
        sampling = sample_pagerank(corpus, damping, int(sample_count), int(seed))
        iteration = iterate_pagerank(corpus, damping_factor=damping)
    except Exception as exc:
        logger.exception("dashboard_run_failed", extra={"source_type": source_type})
        st.error(str(exc))
        return

    logger.info(
        "dashboard_run_completed",
        extra={
            "source_type": source_type,
            "damping": damping,
            "sample_count": int(sample_count),
            "page_count": len(corpus),
            "link_count": sum(len(links) for links in corpus.values()),
            "top_page": iteration.top_page,
        },
    )

    comparison = build_comparison_table(corpus, sampling, iteration.ranks)
    render_results(
        corpus,
        comparison,
        sampling,
        iteration.ranks,
        iteration.iterations,
        iteration.deltas,
    )


def inject_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --prp-green: #16a34a;
            --prp-yellow: #facc15;
            --prp-blue: #2563eb;
            --prp-purple: #7c3aed;
            --prp-ink: #111827;
            --prp-muted: #64748b;
            --prp-panel: #f8fafc;
            --prp-border: #dbe4f0;
        }

        .stApp {
            background:
                linear-gradient(180deg, rgba(37, 99, 235, 0.06), rgba(255, 255, 255, 0) 280px),
                #ffffff;
            color: var(--prp-ink);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #eef7ff 0%, #f7f4ff 48%, #fbfff1 100%);
            border-right: 1px solid var(--prp-border);
        }

        [data-testid="stSidebar"] h3 {
            color: var(--prp-purple);
            font-weight: 800;
            letter-spacing: 0;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid rgba(124, 58, 237, 0.12);
            border-radius: 8px;
            padding: 0.22rem 0.45rem;
            margin-bottom: 0.25rem;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1380px;
        }

        .prp-header {
            border: 1px solid var(--prp-border);
            border-left: 8px solid var(--prp-green);
            background:
                linear-gradient(
                    90deg,
                    rgba(22, 163, 74, 0.10),
                    rgba(37, 99, 235, 0.08) 46%,
                    rgba(124, 58, 237, 0.10)
                ),
                #ffffff;
            border-radius: 8px;
            padding: 1.35rem 1.45rem 1.2rem;
            margin-bottom: 1.15rem;
        }

        .prp-title {
            font-size: clamp(2.1rem, 4vw, 3.45rem);
            font-weight: 900;
            line-height: 1;
            letter-spacing: 0;
            color: var(--prp-ink);
            margin: 0 0 0.55rem;
        }

        .prp-title span:nth-child(1) { color: var(--prp-green); }
        .prp-title span:nth-child(2) { color: var(--prp-blue); }
        .prp-title span:nth-child(3) { color: var(--prp-purple); }

        .prp-subtitle {
            color: var(--prp-muted);
            font-size: 1.02rem;
            max-width: 860px;
            margin: 0;
        }

        .prp-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.45rem;
            margin-top: 1rem;
        }

        .prp-strip div {
            height: 6px;
            border-radius: 999px;
        }

        .prp-strip div:nth-child(1) { background: var(--prp-green); }
        .prp-strip div:nth-child(2) { background: var(--prp-yellow); }
        .prp-strip div:nth-child(3) { background: var(--prp-blue); }
        .prp-strip div:nth-child(4) { background: var(--prp-purple); }

        h2, h3 {
            letter-spacing: 0;
            color: var(--prp-ink);
        }

        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid var(--prp-border);
            border-top: 5px solid var(--prp-blue);
            border-radius: 8px;
            padding: 1rem 1rem 0.9rem;
            box-shadow: 0 12px 26px rgba(15, 23, 42, 0.06);
        }

        div[data-testid="column"]:nth-of-type(1) [data-testid="stMetric"] {
            border-top-color: var(--prp-green);
        }

        div[data-testid="column"]:nth-of-type(2) [data-testid="stMetric"] {
            border-top-color: var(--prp-yellow);
        }

        div[data-testid="column"]:nth-of-type(3) [data-testid="stMetric"] {
            border-top-color: var(--prp-blue);
        }

        div[data-testid="column"]:nth-of-type(4) [data-testid="stMetric"] {
            border-top-color: var(--prp-purple);
        }

        [data-testid="stMetricLabel"] {
            color: var(--prp-muted);
            font-weight: 700;
        }

        [data-testid="stMetricValue"] {
            color: var(--prp-ink);
            font-weight: 900;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--prp-border);
            border-radius: 8px;
            overflow: hidden;
        }

        .stButton > button,
        .stDownloadButton > button {
            border-radius: 8px;
            border: 1px solid rgba(37, 99, 235, 0.22);
            background: #ffffff;
            color: var(--prp-blue);
            font-weight: 800;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            border-color: var(--prp-purple);
            color: var(--prp-purple);
            background: #f7f4ff;
        }

        .prp-analysis-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 0.85rem;
            margin-top: 0.35rem;
        }

        .prp-analysis-card {
            background: #ffffff;
            border: 1px solid var(--prp-border);
            border-left: 6px solid var(--prp-green);
            border-radius: 8px;
            padding: 0.9rem 1rem;
            box-shadow: 0 10px 22px rgba(15, 23, 42, 0.05);
        }

        .prp-analysis-card:nth-child(4n + 2) {
            border-left-color: var(--prp-yellow);
        }

        .prp-analysis-card:nth-child(4n + 3) {
            border-left-color: var(--prp-blue);
        }

        .prp-analysis-card:nth-child(4n + 4) {
            border-left-color: var(--prp-purple);
        }

        .prp-analysis-head {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 0.75rem;
            margin-bottom: 0.55rem;
        }

        .prp-analysis-page {
            font-size: 1.05rem;
            font-weight: 900;
            color: var(--prp-ink);
        }

        .prp-analysis-rank {
            font-size: 0.92rem;
            font-weight: 900;
            color: var(--prp-purple);
            background: #f7f4ff;
            border: 1px solid rgba(124, 58, 237, 0.16);
            border-radius: 999px;
            padding: 0.15rem 0.55rem;
            white-space: nowrap;
        }

        .prp-analysis-stats {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.45rem;
            margin-bottom: 0.65rem;
        }

        .prp-analysis-stat {
            background: var(--prp-panel);
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 0.48rem;
        }

        .prp-analysis-stat span {
            display: block;
            color: var(--prp-muted);
            font-size: 0.72rem;
            font-weight: 800;
        }

        .prp-analysis-stat strong {
            color: var(--prp-ink);
            font-size: 0.95rem;
        }

        .prp-analysis-text {
            color: #334155;
            line-height: 1.45;
            margin: 0;
            font-size: 0.94rem;
        }

        .stSlider [data-testid="stTickBarMin"],
        .stSlider [data-testid="stTickBarMax"] {
            color: var(--prp-muted);
        }

        div[data-testid="stAlert"] {
            border-radius: 8px;
        }

        @media (max-width: 900px) {
            .prp-strip {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <section class="prp-header">
            <h1 class="prp-title"><span>Page</span><span>Rank</span><span>Pro</span></h1>
            <p class="prp-subtitle">
                Explore how link structure, probability, damping, and iterative convergence
                shape search-engine style authority scores.
            </p>
            <div class="prp-strip"><div></div><div></div><div></div><div></div></div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def load_corpus_from_ui(source_type: str) -> dict[str, set[str]]:
    if source_type == "Built-in sample":
        selected = st.selectbox("Sample corpus", list(SAMPLE_CORPORA))
        return crawl(SAMPLE_CORPORA[selected])

    if source_type == "Upload HTML":
        st.subheader("Upload Corpus")
        uploaded_files = st.file_uploader(
            "Upload HTML files or a ZIP containing HTML files",
            type=["html", "htm", "zip"],
            accept_multiple_files=True,
        )
        if not uploaded_files:
            return {}
        return corpus_from_uploads(uploaded_files)

    if source_type == "Manual graph":
        st.subheader("Build Corpus")
        return corpus_from_manual_editor()

    st.subheader("Server Folder")
    corpus_path = st.text_input("Corpus directory", value="corpus/corpus0")
    return crawl(Path(corpus_path))


def corpus_from_uploads(uploaded_files: list) -> dict[str, set[str]]:
    documents: dict[str, str] = {}
    for uploaded_file in uploaded_files:
        name = Path(uploaded_file.name).name
        payload = uploaded_file.getvalue()
        if name.lower().endswith(".zip"):
            documents.update(read_zip_documents(payload))
        elif name.lower().endswith((".html", ".htm")):
            documents[name] = payload.decode("utf-8", errors="replace")

    if not documents:
        raise ValueError("No HTML files were found in the upload.")
    return corpus_from_html_documents(documents)


def read_zip_documents(payload: bytes) -> dict[str, str]:
    documents = {}
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        for member in archive.namelist():
            name = Path(member).name
            if not name.lower().endswith((".html", ".htm")):
                continue
            documents[name] = archive.read(member).decode("utf-8", errors="replace")
    return documents


def corpus_from_html_documents(documents: dict[str, str]) -> dict[str, set[str]]:
    page_names = set(documents)
    corpus = {}
    for page, html in documents.items():
        soup = BeautifulSoup(html, "html.parser")
        links = {
            Path(link.get("href")).name
            for link in soup.find_all("a")
            if link.get("href") and Path(link.get("href")).name in page_names
        }
        corpus[page] = links - {page}
    return corpus


def corpus_from_manual_editor() -> dict[str, set[str]]:
    pages_text = st.text_area(
        "Pages",
        value="home.html\nabout.html\nblog.html\ncontact.html",
        help="Enter one page name per line.",
    )
    pages = [page.strip() for page in pages_text.splitlines() if page.strip()]
    pages = [page if page.lower().endswith((".html", ".htm")) else f"{page}.html" for page in pages]

    default_edges = pd.DataFrame(
        [
            {"Source": "home.html", "Target": "about.html"},
            {"Source": "home.html", "Target": "blog.html"},
            {"Source": "about.html", "Target": "blog.html"},
            {"Source": "blog.html", "Target": "contact.html"},
        ]
    )
    edges = st.data_editor(
        default_edges,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Source": st.column_config.SelectboxColumn("Source", options=pages),
            "Target": st.column_config.SelectboxColumn("Target", options=pages),
        },
    )

    corpus = {page: set() for page in pages}
    for row in edges.to_dict("records"):
        source = row.get("Source")
        target = row.get("Target")
        if source in corpus and target in corpus and source != target:
            corpus[source].add(target)
    return corpus


def build_comparison_table(
    corpus: dict[str, set[str]],
    sampling: dict[str, float],
    iteration: dict[str, float],
) -> pd.DataFrame:
    pages = sorted(corpus)
    return pd.DataFrame(
        {
            "Page": pages,
            "Sampling": [sampling[page] for page in pages],
            "Iteration": [iteration[page] for page in pages],
            "Difference": [abs(sampling[page] - iteration[page]) for page in pages],
            "Incoming Links": [
                sum(1 for links in corpus.values() if page in links) for page in pages
            ],
            "Outgoing Links": [len(corpus[page]) for page in pages],
        }
    ).sort_values("Iteration", ascending=False)


def render_results(
    corpus: dict[str, set[str]],
    comparison: pd.DataFrame,
    sampling: dict[str, float],
    iteration: dict[str, float],
    iteration_count: int,
    deltas: list[float],
) -> None:
    top_page = comparison.iloc[0]["Page"]
    st.subheader("Ranking Overview")
    metric_cols = st.columns(4)
    metric_cols[0].metric("Pages", len(corpus))
    metric_cols[1].metric("Links", sum(len(links) for links in corpus.values()))
    metric_cols[2].metric("Top Page", top_page)
    metric_cols[3].metric("Converged", f"{iteration_count} rounds")

    graph_col, rank_col = st.columns([1.2, 1])
    with graph_col:
        st.subheader("Web Graph")
        fig = draw_graph(corpus, iteration)
        st.pyplot(fig, clear_figure=True)

    with rank_col:
        st.subheader("Ranking Table")
        st.dataframe(
            comparison,
            use_container_width=True,
            height=460,
            hide_index=True,
            column_config={
                "Sampling": st.column_config.NumberColumn(format="%.4f"),
                "Iteration": st.column_config.NumberColumn(format="%.4f"),
                "Difference": st.column_config.NumberColumn(format="%.4f"),
            },
        )

    chart_col, convergence_col = st.columns(2)
    with chart_col:
        st.subheader("Sampling vs Iteration")
        st.pyplot(draw_comparison_chart(comparison), clear_figure=True)

    with convergence_col:
        st.subheader("Convergence")
        st.pyplot(draw_convergence_chart(deltas), clear_figure=True)

    st.subheader("Ranking Analysis")
    render_ranking_analysis(corpus, comparison, iteration)

    st.subheader("Export")
    report = build_report(corpus, sampling, iteration, iteration_count, deltas)
    export_cols = st.columns(3)
    export_cols[0].download_button(
        "Download ranking CSV",
        comparison.to_csv(index=False),
        file_name="pagerankpro-rankings.csv",
        mime="text/csv",
        use_container_width=True,
    )
    export_cols[1].download_button(
        "Download report JSON",
        json.dumps(report, indent=2),
        file_name="pagerankpro-report.json",
        mime="application/json",
        use_container_width=True,
    )
    export_cols[2].download_button(
        "Download graph PNG",
        figure_to_png(draw_graph(corpus, iteration)),
        file_name="pagerankpro-graph.png",
        mime="image/png",
        use_container_width=True,
    )


def render_ranking_analysis(
    corpus: dict[str, set[str]],
    comparison: pd.DataFrame,
    iteration: dict[str, float],
) -> None:
    st.caption(f"Showing analysis for all {len(comparison)} ranked pages.")

    cards = []
    for _, row in comparison.iterrows():
        page = str(row["Page"])
        explanation = explain_rank(page, corpus, iteration)
        cards.append(
            '<article class="prp-analysis-card">'
            '<div class="prp-analysis-head">'
            f'<div class="prp-analysis-page">{escape(page)}</div>'
            f'<div class="prp-analysis-rank">{row["Iteration"]:.4f}</div>'
            "</div>"
            '<div class="prp-analysis-stats">'
            '<div class="prp-analysis-stat">'
            "<span>Incoming</span>"
            f'<strong>{int(row["Incoming Links"])}</strong>'
            "</div>"
            '<div class="prp-analysis-stat">'
            "<span>Outgoing</span>"
            f'<strong>{int(row["Outgoing Links"])}</strong>'
            "</div>"
            '<div class="prp-analysis-stat">'
            "<span>Diff</span>"
            f'<strong>{row["Difference"]:.4f}</strong>'
            "</div>"
            "</div>"
            f'<p class="prp-analysis-text">{escape(explanation)}</p>'
            "</article>"
        )

    st.markdown(
        f'<div class="prp-analysis-grid">{"".join(cards)}</div>',
        unsafe_allow_html=True,
    )


def build_report(
    corpus: dict[str, set[str]],
    sampling: dict[str, float],
    iteration: dict[str, float],
    iteration_count: int,
    deltas: list[float],
) -> dict:
    return {
        "summary": {
            "pages": len(corpus),
            "links": sum(len(links) for links in corpus.values()),
            "top_page": max(iteration, key=iteration.get),
            "iterations": iteration_count,
            "final_delta": deltas[-1] if deltas else 0,
        },
        "corpus": {page: sorted(links) for page, links in corpus.items()},
        "sampling": sampling,
        "iteration": iteration,
    }


def show_self_check_results() -> None:
    sample = crawl(SAMPLE_CORPORA["Sample corpus 0"])
    transition = transition_model(sample, "1.html", DEFAULT_DAMPING)
    sampling = sample_pagerank(sample, DEFAULT_DAMPING, 1_000, seed=7)
    iteration = iterate_pagerank(sample, DEFAULT_DAMPING)

    checks = {
        "Transition model sums to 1": abs(sum(transition.values()) - 1) < 0.000001,
        "Sampling ranks sum to 1": abs(sum(sampling.values()) - 1) < 0.000001,
        "Iteration ranks sum to 1": abs(sum(iteration.ranks.values()) - 1) < 0.000001,
        "Iteration converges": iteration.iterations > 0,
        "Dead-end page handled": "12.html" in sample and not sample["12.html"],
    }
    if all(checks.values()):
        st.success("All self-checks passed.")
    else:
        st.error("One or more self-checks failed.")
    st.json(checks)


def draw_graph(corpus: dict[str, set[str]], ranks: dict[str, float]) -> plt.Figure:
    graph = build_graph(corpus)
    position = nx.spring_layout(graph, seed=7)
    values = [ranks.get(node, 0.0) for node in graph.nodes]
    sizes = [900 + 7_000 * value for value in values]

    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw_networkx_edges(
        graph,
        position,
        ax=ax,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=16,
        edge_color=THEME_COLORS["muted"],
        width=1.4,
        connectionstyle="arc3,rad=0.08",
    )
    nodes = nx.draw_networkx_nodes(
        graph,
        position,
        ax=ax,
        node_size=sizes,
        node_color=values,
        cmap=RANK_CMAP,
        edgecolors="#111827",
        linewidths=1.1,
    )
    nx.draw_networkx_labels(
        graph,
        position,
        ax=ax,
        font_size=9,
        font_weight="bold",
        font_color=THEME_COLORS["ink"],
    )
    fig.colorbar(nodes, ax=ax, label="PageRank")
    ax.set_axis_off()
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    return fig


def draw_comparison_chart(comparison: pd.DataFrame) -> plt.Figure:
    chart_data = comparison.sort_values("Iteration", ascending=False)
    x_positions = range(len(chart_data))
    width = 0.38

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.bar(
        [position - width / 2 for position in x_positions],
        chart_data["Sampling"],
        width=width,
        label="Sampling",
        color=THEME_COLORS["green"],
    )
    ax.bar(
        [position + width / 2 for position in x_positions],
        chart_data["Iteration"],
        width=width,
        label="Iteration",
        color=THEME_COLORS["purple"],
    )
    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(chart_data["Page"], rotation=20, ha="right")
    ax.set_ylabel("PageRank")
    ax.grid(axis="y", color="#e5e7eb", linewidth=0.9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#cbd5e1")
    ax.legend(frameon=False)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    return fig


def draw_convergence_chart(deltas: list[float]) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 4.8))
    rounds = list(range(1, len(deltas) + 1))
    ax.plot(rounds, deltas, color=THEME_COLORS["blue"], linewidth=2.5, marker="o")
    ax.fill_between(rounds, deltas, color=THEME_COLORS["yellow"], alpha=0.22)
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Max Delta")
    ax.grid(axis="y", color="#e5e7eb", linewidth=0.9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#cbd5e1")
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    return fig


def figure_to_png(fig: plt.Figure) -> bytes:
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    return buffer.getvalue()


if __name__ == "__main__":
    main()
