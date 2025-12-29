"""Test thumbnail image file paths in HTML and on disk.

TODO::
- Test multiple directives same file same and different resizes.
    - Different size == different file e.g. tux2.png
- Also test in sub.
"""

from pathlib import Path
from textwrap import dedent

import PIL.Image
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
    """Confirm resized image paths keep their full relative path to srcdir to prevent collisions."""
    open_paths = []
    save_paths = []

    # Patch open.
    orig_pil_image_open = PIL.Image.open

    def spy_pil_open(path, *args, **kwargs):
        open_paths.append(path.relative_to(app.srcdir))
        return orig_pil_image_open(path, *args, **kwargs)

    monkeypatch.setattr(PIL.Image, "open", spy_pil_open)

    # Patch save.
    orig_pil_image_save = PIL.Image.Image.save

    def spy_pil_save(self, path, *args, **kwargs):
        save_paths.append(path.relative_to(app.srcdir))
        return orig_pil_image_save(self, path, *args, **kwargs)

    monkeypatch.setattr(PIL.Image.Image, "save", spy_pil_save)

    # Run.
    app.build()

    # Check.
    assert open_paths == [
        Path("_images/tux.png"),
        Path("sub/pictures/tux.png"),
    ]
    assert save_paths == [
        Path("_build/doctrees/_thumbs/_images/tux.100x118.png"),
        Path("_build/doctrees/_thumbs/sub/pictures/tux.100x118.png"),
    ]
