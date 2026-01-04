"""Test support of different input image formats."""

from pathlib import Path

import PIL.Image
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


@pytest.mark.parametrize(
    "app_params,expected_fname,expected_format",
    [
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png"}}, "tux.50x59.png", "PNG"),
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/apple.jpg"}}, "apple.50x6.jpg", "JPEG"),
    ],
    indirect=["app_params"],
)
@pytest.mark.sphinx("html", testroot="defaults", confoverrides={"thumb_image_resize_width": 50})
def test_formats(outdir: Path, img_tags: list[element.Tag], expected_fname: str, expected_format: str):
    """Test with image of different non-animated formats."""
    # Confirm img src.
    img_src = [t["src"] for t in img_tags]
    assert img_src == [f"_images/{expected_fname}"]
    # Confirm image file's new dimensions.
    image_path = outdir / img_src[0]
    with PIL.Image.open(image_path) as image:
        assert image.format == expected_format


@pytest.mark.sphinx("html", testroot="defaults", confoverrides={"thumb_image_resize_width": 10})
def test_animated():
    """TODO."""
    pytest.skip("TODO")
