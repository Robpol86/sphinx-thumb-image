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
    "app_params,expected_name,expected_format",
    [
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png"}}, "tux.50x59.png", "PNG"),
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/apple.jpg"}}, "apple.50x6.jpg", "JPEG"),
    ],
    indirect=["app_params"],
)
@pytest.mark.sphinx("html", testroot="defaults", confoverrides={"thumb_image_resize_width": 50})
def test_formats(outdir: Path, img_tags: list[element.Tag], expected_name: str, expected_format: str):
    """Test with image of different non-animated formats."""
    # Confirm img src.
    img_src = [t["src"] for t in img_tags]
    assert img_src == [f"_images/{expected_name}"]
    # Confirm image file's new dimensions.
    image_path = outdir / img_src[0]
    with PIL.Image.open(image_path) as image:
        assert image.format == expected_format
        assert getattr(image, "is_animated", False) is False


@pytest.mark.parametrize(
    "app_params,expected_name,expected_format,expected_frames",
    [
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/goku.gif"}}, "goku.10x3.gif", "GIF", 20),
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/ball.apng"}}, "ball.10x10.apng", "PNG", 10),
    ],
    indirect=["app_params"],
)
@pytest.mark.sphinx("html", testroot="defaults", confoverrides={"thumb_image_resize_width": 10})
def test_animated(outdir: Path, img_tags: list[element.Tag], expected_name: str, expected_format: str, expected_frames: int):
    """Test with image of different non-animated formats."""
    # Confirm img src.
    img_src = [t["src"] for t in img_tags]
    assert img_src == [f"_images/{expected_name}"]
    # Confirm image file's new dimensions.
    image_path = outdir / img_src[0]
    with PIL.Image.open(image_path) as image:
        assert image.format == expected_format
        pytest.skip("TODO")
        assert image.is_animated is True
        assert image.frames == expected_frames
