import socket
import subprocess
import sys
import time
from collections.abc import Iterator

import pytest
import requests


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


@pytest.fixture(scope="module")
def streamlit_url() -> Iterator[str]:
    port = _free_port()
    url = f"http://127.0.0.1:{port}"
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
            f"--server.port={port}",
            "--server.address=127.0.0.1",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            if process.poll() is not None:
                stdout, stderr = process.communicate(timeout=5)
                raise RuntimeError(f"Streamlit exited early\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")
            try:
                response = requests.get(f"{url}/_stcore/health", timeout=2)
                if response.status_code == 200:
                    yield url
                    return
            except requests.RequestException:
                time.sleep(1)
        raise TimeoutError("Timed out waiting for Streamlit dashboard")
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()


def test_dashboard_renders_core_sections(page, streamlit_url: str) -> None:
    page.goto(streamlit_url, wait_until="networkidle")

    page.get_by_text("PageRankPro", exact=True).wait_for()
    page.get_by_text("Controls", exact=True).wait_for()
    page.get_by_text("Corpus source", exact=True).wait_for()
    page.get_by_text("Web Graph", exact=True).wait_for()
    page.get_by_text("Ranking Table", exact=True).wait_for()
    page.get_by_text("Sampling vs Iteration", exact=True).wait_for()
    page.get_by_text("Convergence", exact=True).wait_for()
    page.get_by_text("Ranking Analysis", exact=True).wait_for()
    page.get_by_text("Export", exact=True).wait_for()
    page.get_by_text("Download ranking CSV", exact=True).wait_for()


def test_dashboard_manual_graph_workflow(page, streamlit_url: str) -> None:
    page.goto(streamlit_url, wait_until="networkidle")

    page.get_by_text("Manual graph", exact=True).click()
    page.get_by_text("Build Corpus", exact=True).wait_for()
    page.get_by_text("Web Graph", exact=True).wait_for()
    page.get_by_text("Ranking Table", exact=True).wait_for()
