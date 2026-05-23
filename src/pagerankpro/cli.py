"""Command-line interface for PageRankPro."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pagerankpro.core import (
    CONVERGENCE_TOLERANCE,
    DEFAULT_DAMPING,
    DEFAULT_SAMPLES,
    crawl,
    explain_rank,
    iterate_pagerank,
    sample_pagerank,
)
from pagerankpro.observability import configure_logging, init_error_monitoring
from pagerankpro.visualization import save_graph_visualization

logger = configure_logging("pagerankpro-cli")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pagerankpro",
        description="Rank linked HTML pages using sampling and iterative PageRank.",
    )
    parser.add_argument("corpus", type=Path, help="Directory containing HTML pages")
    parser.add_argument("--damping", type=float, default=DEFAULT_DAMPING)
    parser.add_argument("--samples", type=int, default=DEFAULT_SAMPLES)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--tolerance", type=float, default=CONVERGENCE_TOLERANCE)
    parser.add_argument("--max-iterations", type=int, default=10_000)
    parser.add_argument("--graph-out", type=Path, help="Optional path for graph PNG output")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    init_error_monitoring(environment="cli")

    try:
        logger.info(
            "pagerank_run_started",
            extra={
                "corpus": str(args.corpus),
                "damping": args.damping,
                "samples": args.samples,
                "tolerance": args.tolerance,
            },
        )
        corpus = crawl(args.corpus)
        sampling = sample_pagerank(corpus, args.damping, args.samples, args.seed)
        iteration = iterate_pagerank(
            corpus,
            damping_factor=args.damping,
            tolerance=args.tolerance,
            max_iterations=args.max_iterations,
        )

        print_report(corpus, sampling, iteration.ranks, iteration.iterations, iteration.deltas)

        if args.graph_out:
            save_graph_visualization(corpus, iteration.ranks, args.graph_out)
            print(f"\nGraph visualization saved to: {args.graph_out}")

        logger.info(
            "pagerank_run_completed",
            extra={
                "page_count": len(corpus),
                "link_count": sum(len(links) for links in corpus.values()),
                "top_page": max(iteration.ranks, key=iteration.ranks.get),
                "iterations": iteration.iterations,
            },
        )
        return 0
    except (FileNotFoundError, NotADirectoryError, ValueError, RuntimeError, KeyError) as exc:
        logger.exception("pagerank_run_failed")
        print(f"Error: {exc}", file=sys.stderr)
        return 1


def print_report(
    corpus: dict[str, set[str]],
    sampling: dict[str, float],
    iteration: dict[str, float],
    iteration_count: int,
    deltas: list[float],
) -> None:
    pages = sorted(corpus)

    print("PageRank Results from Sampling")
    for page in pages:
        print(f"{page}: {sampling[page]:.4f}")

    print("\nPageRank Results from Iteration")
    for page in pages:
        print(f"{page}: {iteration[page]:.4f}")

    print("\nAlgorithm Comparison")
    print(f"{'Page':<20} {'Sampling':>10} {'Iteration':>10} {'Abs Diff':>10}")
    for page in pages:
        print(f"{page:<20} {sampling[page]:>10.4f} {iteration[page]:>10.4f} "
              f"{abs(sampling[page] - iteration[page]):>10.4f}")

    top_page = max(iteration, key=iteration.get)
    last_delta = deltas[-1] if deltas else 0
    print(f"\nTop Page: {top_page}")
    print(f"Iteration converged in {iteration_count} round(s); final max delta: {last_delta:.6f}")
    print(explain_rank(top_page, corpus, iteration))


if __name__ == "__main__":
    raise SystemExit(main())
