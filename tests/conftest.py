"""Shared fixtures: an in-process test client for the whole suite.

The app resolves data/ and tuftecms/static/ relative to the repo root,
so make sure tests run from there regardless of how pytest was invoked.
"""

import os
from pathlib import Path

import pytest

os.chdir(Path(__file__).resolve().parent.parent)

from engine import api  # noqa: E402


@pytest.fixture(scope="session")
def client():
    """Synchronous test client wired straight to the ASGI app."""
    return api.requests
