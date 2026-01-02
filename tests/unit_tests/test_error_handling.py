"""Verify error handling of common scenarios."""

import pytest
from bs4 import element
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    warningiserror=False,
    exception_on_warning=False,
    confoverrides={
        "thumb_image_resize_width": 100,
    },
    write_docs={
        "index.rst": ".. image:: does_not_exist.jpg",
    },
)
def test_file_not_found(app: SphinxTestApp, img_tags: list[element.Tag]):
    """Test with external image."""
    # Confirm img src.
    img_src = [t["src"] for t in img_tags]
    assert img_src == ["does_not_exist.jpg"]
    # Confirm warning was emitted.
    assert "WARNING: image file not readable: does_not_exist.jpg" in app.warning.getvalue()
