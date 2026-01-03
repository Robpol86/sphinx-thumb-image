"""Test support of different input image formats."""

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
        "index.rst": ".. thumb-image:: https://i.imgur.com/Ouih4Z1.jpeg",
    },
)
def test_hotlinked(app: SphinxTestApp, img_tags: list[element.Tag]):
    """Test with external image."""
    # Confirm img src.
    img_src = [t["src"] for t in img_tags]
    assert img_src == ["https://i.imgur.com/Ouih4Z1.jpeg"]
    # Confirm warning was emitted.
    warnings = app.warning.getvalue()
    assert "WARNING: external images are not supported" in warnings


# TODO jpeg test

# TODO gif TDD
