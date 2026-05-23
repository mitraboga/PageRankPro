from pathlib import Path

import pytest

from pagerankpro.core import (
    crawl,
    iterate_pagerank,
    normalize_ranks,
    sample_pagerank,
    transition_model,
)


def test_crawl_discards_external_and_self_links(tmp_path: Path) -> None:
    (tmp_path / "1.html").write_text(
        '<a href="1.html">Self</a><a href="2.html">Two</a>'
        '<a href="https://example.com/x.html">External</a>',
        encoding="utf-8",
    )
    (tmp_path / "2.html").write_text('<a href="1.html">One</a>', encoding="utf-8")

    assert crawl(tmp_path) == {"1.html": {"2.html"}, "2.html": {"1.html"}}


def test_transition_model_for_linked_page() -> None:
    corpus = {"1.html": {"2.html"}, "2.html": {"1.html"}}

    model = transition_model(corpus, "1.html", 0.85)

    assert model["1.html"] == pytest.approx(0.075)
    assert model["2.html"] == pytest.approx(0.925)
    assert sum(model.values()) == pytest.approx(1.0)


def test_transition_model_for_dead_end_links_to_every_page() -> None:
    corpus = {"1.html": set(), "2.html": {"1.html"}}

    model = transition_model(corpus, "1.html", 0.85)

    assert model["1.html"] == pytest.approx(0.5)
    assert model["2.html"] == pytest.approx(0.5)


def test_iterate_pagerank_converges_and_normalizes() -> None:
    corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}

    result = iterate_pagerank(corpus, damping_factor=0.85)

    assert result.iterations > 0
    assert sum(result.ranks.values()) == pytest.approx(1.0)
    assert result.top_page == "2.html"


def test_sampling_is_deterministic_with_seed() -> None:
    corpus = {"1.html": {"2.html"}, "2.html": {"1.html"}}

    first = sample_pagerank(corpus, sample_count=1000, seed=123)
    second = sample_pagerank(corpus, sample_count=1000, seed=123)

    assert first == second
    assert sum(first.values()) == pytest.approx(1.0)


def test_normalize_rejects_empty_input() -> None:
    with pytest.raises(ValueError):
        normalize_ranks({})
