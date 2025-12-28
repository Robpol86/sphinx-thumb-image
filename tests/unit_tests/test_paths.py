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
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    srcdir="test_no_collisions",
    write_docs={
        "index.rst": dedent("""
            .. image:: _images/tux.png
            .. thumb-image:: _images/tux.png
                :resize-width: 100
            .. thumb-image:: _images/tux.png
                :resize-width: 50
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
    srcdir="test_efficient",
    write_docs={
        "index.rst": dedent("""
            .. thumb-image:: _images/tux.png
                :resize-width: 100
            .. thumb-image:: _images/tux.png
                :resize-width: 50
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
    assert sorted(f.name for f in (outdir / "_images").iterdir()) == [
        "tux.100x118.png",
        "tux.50x59.png",
    ]


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    srcdir="test_doctrees_paths",
    copy_files={
        "_images/tux.png": "sub/pictures/tux.png",
    },
    write_docs={
        "index.rst": dedent("""
            .. thumb-image:: _images/tux.png
                :resize-width: 100
        """),
        "sub/sub.rst": dedent("""
            :orphan:\n
            .. thumb-image:: pictures/tux.png
                :resize-width: 100
        """),
    },
)
def test_doctrees_paths(monkeypatch: pytest.MonkeyPatch, app: SphinxTestApp):
    """TODO.

    - Monkeypatch PIL.Image.open() and image.save() to record paths, then run app.build()
    - Assert doctrees/_thumbs/sub/_images/tux.XxX.png
    - Probably need to bring conftest.py changes from cache-collision-parallel branch
    """
    pytest.skip("TODO")
