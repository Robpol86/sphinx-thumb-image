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
        "index.rst": ".. thumb-image:: does_not_exist.jpg",
    },
)
def test_file_not_found(app: SphinxTestApp, img_tags: list[element.Tag]):
    """Test with image that doesn't exist."""
    # Confirm img src.
    img_src = [t["src"] for t in img_tags]
    assert img_src == ["does_not_exist.jpg"]
    # Confirm warning was emitted.
    warnings = app.warning.getvalue()
    assert "WARNING: image file not readable: does_not_exist.jpg" in warnings


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    warningiserror=False,
    exception_on_warning=False,
    confoverrides={
        "thumb_image_resize_width": 100,
    },
    write_docs={
        "index.rst": ".. thumb-image:: _images",
    },
)
def test_not_a_file(app: SphinxTestApp, img_tags: list[element.Tag]):
    """Test with image that isn't a file."""
    # Confirm img src.
    img_src = [t["src"] for t in img_tags]
    assert img_src == ["_images/_images"]
    # Confirm warning was emitted.
    warnings = app.warning.getvalue()
    assert "[Errno 21] Is a directory" in warnings
