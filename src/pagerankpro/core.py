"""Core PageRank algorithms and corpus parsing."""

from __future__ import annotations

import random
import re
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup

DEFAULT_DAMPING = 0.85
DEFAULT_SAMPLES = 10_000
CONVERGENCE_TOLERANCE = 0.001


Corpus = dict[str, set[str]]
Ranks = dict[str, float]


@dataclass(frozen=True)
class PageRankResult:
    """Container for PageRank outputs and convergence diagnostics."""

    ranks: Ranks
    iterations: int
    deltas: list[float]
    history: list[Ranks]

    @property
    def top_page(self) -> str:
        return max(self.ranks, key=self.ranks.get)


def crawl(directory: str | Path) -> Corpus:
    """Parse HTML files and return a directed graph represented as page -> linked pages."""

    corpus_dir = Path(directory)
    if not corpus_dir.exists():
        raise FileNotFoundError(f"Corpus directory does not exist: {corpus_dir}")
    if not corpus_dir.is_dir():
        raise NotADirectoryError(f"Corpus path is not a directory: {corpus_dir}")

    pages = {
        path.name: _extract_links(path)
        for path in sorted(corpus_dir.iterdir())
        if path.is_file() and path.suffix.lower() in {".html", ".htm"}
    }
    if not pages:
        raise ValueError(f"No HTML files found in corpus directory: {corpus_dir}")

    page_names = set(pages)
    return {page: links & page_names - {page} for page, links in pages.items()}


def transition_model(corpus: Mapping[str, set[str]], page: str, damping_factor: float) -> Ranks:
    """Return the probability distribution over next pages from the given page."""

    _validate_corpus(corpus)
    _validate_damping(damping_factor)
    if page not in corpus:
        raise KeyError(f"Page is not in corpus: {page}")

    pages = sorted(corpus)
    page_count = len(pages)
    random_jump = (1 - damping_factor) / page_count
    links = corpus[page] or set(pages)
    linked_probability = damping_factor / len(links)

    model = {candidate: random_jump for candidate in pages}
    for linked_page in links:
        model[linked_page] += linked_probability
    return normalize_ranks(model)


def sample_pagerank(
    corpus: Mapping[str, set[str]],
    damping_factor: float = DEFAULT_DAMPING,
    sample_count: int = DEFAULT_SAMPLES,
    seed: int | None = None,
) -> Ranks:
    """Estimate PageRank by simulating a random surfer."""

    _validate_corpus(corpus)
    _validate_damping(damping_factor)
    if sample_count <= 0:
        raise ValueError("sample_count must be positive")

    rng = random.Random(seed)
    pages = sorted(corpus)
    current_page = rng.choice(pages)
    visits: Counter[str] = Counter()

    for _ in range(sample_count):
        visits[current_page] += 1
        model = transition_model(corpus, current_page, damping_factor)
        current_page = _weighted_choice(model, rng)

    return normalize_ranks({page: visits[page] / sample_count for page in pages})


def iterate_pagerank(
    corpus: Mapping[str, set[str]],
    damping_factor: float = DEFAULT_DAMPING,
    tolerance: float = CONVERGENCE_TOLERANCE,
    max_iterations: int = 10_000,
) -> PageRankResult:
    """Compute PageRank with iterative convergence."""

    _validate_corpus(corpus)
    _validate_damping(damping_factor)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")

    pages = sorted(corpus)
    page_count = len(pages)
    ranks = {page: 1 / page_count for page in pages}
    history = [ranks.copy()]
    deltas: list[float] = []

    for iteration in range(1, max_iterations + 1):
        updated = {}
        for page in pages:
            linked_rank_sum = 0.0
            for possible_page in pages:
                outgoing_links = corpus[possible_page] or set(pages)
                if page in outgoing_links:
                    linked_rank_sum += ranks[possible_page] / len(outgoing_links)
            updated[page] = (1 - damping_factor) / page_count + damping_factor * linked_rank_sum

        updated = normalize_ranks(updated)
        max_delta = max(abs(updated[page] - ranks[page]) for page in pages)
        deltas.append(max_delta)
        history.append(updated.copy())
        ranks = updated

        if max_delta < tolerance:
            return PageRankResult(ranks=ranks, iterations=iteration, deltas=deltas, history=history)

    raise RuntimeError(
        f"PageRank did not converge within {max_iterations} iterations "
        f"(last max delta: {deltas[-1]:.6f})"
    )


def normalize_ranks(ranks: Mapping[str, float]) -> Ranks:
    """Normalize a rank dictionary so values sum to one."""

    if not ranks:
        raise ValueError("Cannot normalize an empty rank dictionary")
    total = sum(ranks.values())
    if total <= 0:
        raise ValueError("Rank total must be positive")
    return {page: value / total for page, value in ranks.items()}


def explain_rank(page: str, corpus: Mapping[str, set[str]], ranks: Mapping[str, float]) -> str:
    """Generate a short explanation of why a page received its rank."""

    if page not in corpus:
        raise KeyError(f"Page is not in corpus: {page}")

    incoming = sorted(source for source, links in corpus.items() if page in links)
    if not incoming:
        return f"{page} has no direct incoming links, so its rank mainly comes from random jumps."

    strongest_source = max(incoming, key=lambda source: ranks.get(source, 0.0))
    return (
        f"{page} receives {len(incoming)} incoming link(s). Its strongest contributor is "
        f"{strongest_source} with PageRank {ranks.get(strongest_source, 0.0):.4f}."
    )


def _extract_links(path: Path) -> set[str]:
    contents = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(contents, "html.parser")
    links = {link.get("href") for link in soup.find_all("a")}
    return {Path(link).name for link in links if link and _looks_like_html(link)}


def _looks_like_html(link: str) -> bool:
    return bool(re.search(r"\.html?$", link, flags=re.IGNORECASE))


def _weighted_choice(distribution: Mapping[str, float], rng: random.Random) -> str:
    threshold = rng.random()
    cumulative = 0.0
    last_page = ""
    for page, probability in distribution.items():
        cumulative += probability
        last_page = page
        if threshold <= cumulative:
            return page
    return last_page


def _validate_corpus(corpus: Mapping[str, set[str]]) -> None:
    if not corpus:
        raise ValueError("corpus must contain at least one page")
    pages = set(corpus)
    for page, links in corpus.items():
        unknown_links = links - pages
        if unknown_links:
            raise ValueError(f"{page} links to unknown page(s): {sorted(unknown_links)}")


def _validate_damping(damping_factor: float) -> None:
    if not 0 <= damping_factor <= 1:
        raise ValueError("damping_factor must be between 0 and 1")
