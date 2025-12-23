"""Test thumbnail image file paths in HTML and on disk.

TODO::
- Test multiple directives same file same and different resizes.
    - Different size == different file e.g. tux2.png
- Also test in sub.
"""

from pathlib import Path
from textwrap import dedent

import pytest
from bs4 import element


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    write_docs={
        "index.rst": dedent("""
            .. image:: pictures/tux.png
            .. thumb-image:: pictures/tux.png
                :scale-width: 100
            .. thumb-image:: pictures/tux.png
                :scale-width: 50
        """),
    },
)
def test_no_collisions(outdir: Path, img_tags: list[element.Tag]):
    """Confirm extension does not clobber non-thumbed image files."""
    # Confirm img src.
    img_src = sorted(t["src"] for t in img_tags)
    assert img_src == [
        "_images/tux.100x118.png",
        "_images/tux.50x59.png",
        "_images/tux.png",
    ]
    # Confirm files on disk.
    assert sorted(f.name for f in (outdir / "_images").iterdir()) == [
        "tux.100x118.png",
        "tux.50x59.png",
        "tux.png",
    ]


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    write_docs={
        "index.rst": dedent("""
            .. thumb-image:: pictures/tux.png
                :scale-width: 100
            .. thumb-image:: pictures/tux.png
                :scale-width: 50
        """),
    },
)
def test_efficient(outdir: Path, img_tags: list[element.Tag]):
    """Confirm original image files not in output directory if not needed."""
    # Confirm img src.
    img_src = [t["src"] for t in img_tags]
    assert img_src == [
        "_images/tux.100x118.png",
        "_images/tux.50x59.png",
    ]
    # Confirm files on disk.
    pytest.skip("TODO")  # TESTS ARE LEAKING
    assert sorted(f.name for f in (outdir / "_images").iterdir()) == [
        "tux.100x118.png",
        "tux.50x59.png",
    ]
