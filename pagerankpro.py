"""Compatibility entrypoint for `python pagerankpro.py corpus`."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from pagerankpro.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
