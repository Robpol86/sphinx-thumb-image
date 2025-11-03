"""Tests."""

import logging
import re
import subprocess

from _pytest.monkeypatch import MonkeyPatch


def test_lock(monkeypatch: MonkeyPatch):
    """Verify lock file is up to date."""
    monkeypatch.delenv("UV_FROZEN")
    output = subprocess.check_output(["uv", "lock", "--check"], stderr=subprocess.STDOUT).strip()
    assert output
    matches = re.findall(rb"The lockfile .+ needs to be updated", output, re.MULTILINE)
    if matches:
        logging.getLogger(__name__).warning(matches[0])
        raise RuntimeError("Update lock file with: make relock")
