#!/usr/bin/env python3
"""Ensure Word-processing helpers run with a Python that has python-docx."""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path


BUNDLED_PYTHON = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "python" / "bin" / "python3"


def ensure_python_docx() -> None:
    if importlib.util.find_spec("docx") is not None:
        return
    if BUNDLED_PYTHON.exists() and Path(sys.executable).resolve() != BUNDLED_PYTHON.resolve():
        os.execv(str(BUNDLED_PYTHON), [str(BUNDLED_PYTHON), *sys.argv])
    raise ModuleNotFoundError(
        "python-docx is required. Run this helper with the bundled Codex Python "
        f"or install python-docx for {sys.executable}."
    )
