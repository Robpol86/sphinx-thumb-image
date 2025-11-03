"""Tests."""

import subprocess
from pathlib import Path


def test_version():
    """Verify multi-sourced versions are synchronized."""
    # Get version from Poetry.
    output = subprocess.check_output(["uv", "version", "--short"]).strip()
    version_uv = output.decode("utf8")

    # Get version from project.
    output = subprocess.check_output(
        ["uv", "run", "python", "-c", "from sphinx_thumb_image import __version__; print(__version__)"]
    ).strip()
    version_project = output.decode("utf8")

    assert version_uv == version_project


def test_changelog():
    """Verify current version is included in the changelog file."""
    version = subprocess.check_output(["uv", "version", "--short"]).strip().decode("utf8")
    changelog = Path(__file__).parent.parent.parent / "CHANGELOG.md"

    with changelog.open("r") as handle:
        changelog_head = handle.read(1024).splitlines()

    assert [line for line in changelog_head if line.startswith(f"## [{version}] - ")]
