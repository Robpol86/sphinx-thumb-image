"""Test thumbnail image file paths in HTML and on disk."""

from pathlib import Path
from textwrap import dedent

import pytest
from bs4 import element


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    write_docs={
        "index.rst": dedent("""
            .. image:: _images/tux.png
            .. thumb-image:: _images/tux.png
                :scale-width: 100
            .. thumb-image:: _images/tux.png
                :scale-width: 50
        """),
    },
)
def test_no_collisions(outdir: Path, img_tags: list[element.Tag]):
    """Confirm extension does not clobber non-thumbed image files."""
    # Confirm img src.
    img_src = [t["src"] for t in img_tags]
    pytest.skip("TODO")
    assert img_src == [
        "_images/tux.png",
        "_images/tux.th.png",
        "_images/tux.th2.png",
    ]
    # Confirm files on disk.
    assert sorted((outdir / "_images").listdir()) == [
        "tux.png",
        "tux.th.png",
        "tux.th2.png",
    ]


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    write_docs={
        "index.rst": dedent("""
            .. thumb-image:: _images/tux.png
                :scale-width: 100
            .. thumb-image:: _images/tux.png
                :scale-width: 50
        """),
    },
)
def test_efficient(outdir: Path, img_tags: list[element.Tag]):
    """Confirm original image files not in output directory if not needed."""
    # Confirm img src.
    img_src = [t["src"] for t in img_tags]
    pytest.skip("TODO")
    assert img_src == [
        "_images/tux.th.png",
        "_images/tux.th2.png",
    ]
    # Confirm files on disk.
    assert sorted((outdir / "_images").listdir()) == [
        "tux.th.png",
        "tux.th2.png",
    ]
