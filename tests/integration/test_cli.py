import subprocess
import sys


def test_cli_runs_against_sample_corpus() -> None:
    result = subprocess.run(
        [sys.executable, "pagerankpro.py", "corpus/corpus0", "--samples", "1000"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "PageRank Results from Sampling" in result.stdout
    assert "PageRank Results from Iteration" in result.stdout
    assert "Top Page:" in result.stdout
    assert "pagerank_run_completed" in result.stderr
