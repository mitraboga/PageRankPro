"""Graph visualization helpers."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx


def build_graph(corpus: Mapping[str, set[str]]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for page, links in corpus.items():
        graph.add_node(page)
        for linked_page in links:
            graph.add_edge(page, linked_page)
    return graph


def save_graph_visualization(
    corpus: Mapping[str, set[str]],
    ranks: Mapping[str, float],
    output_path: str | Path,
) -> Path:
    """Save a PageRank-weighted graph image."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    graph = build_graph(corpus)
    position = nx.spring_layout(graph, seed=7)
    values = [ranks.get(node, 0.0) for node in graph.nodes]
    sizes = [1_200 + 8_000 * value for value in values]

    plt.figure(figsize=(10, 7))
    nx.draw_networkx_edges(
        graph,
        position,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=18,
        edge_color="#6b7280",
        width=1.5,
        connectionstyle="arc3,rad=0.08",
    )
    nodes = nx.draw_networkx_nodes(
        graph,
        position,
        node_size=sizes,
        node_color=values,
        cmap=plt.cm.viridis,
        edgecolors="#111827",
        linewidths=1.2,
    )
    nx.draw_networkx_labels(graph, position, font_size=10, font_weight="bold")
    plt.colorbar(nodes, label="PageRank")
    plt.title("PageRankPro Web Graph")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return path
