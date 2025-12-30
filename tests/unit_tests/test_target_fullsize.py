"""TODO."""

from pathlib import Path
from typing import Optional

import pytest
from bs4 import element
from sphinx.testing.util import SphinxTestApp


@pytest.mark.parametrize(
    "app_params,expected_href,expected_files",
    [
        (
            {"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :target: google.com"}},
            "google.com",
            ["tux.100x118.png"],
        ),
        (
            {"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :target: google.com\n  :target-fullsize:"}},
            "_images/tux.png",
            ["tux.100x118.png", "tux.png"],
        ),
        (
            {"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :target-fullsize:"}},
            "_images/tux.png",
            ["tux.100x118.png", "tux.png"],
        ),
        (
            {"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png"}},
            None,
            ["tux.100x118.png"],
        ),
        (
            {
                "write_docs": {"index.rst": ".. thumb-image:: _images/tux.png"},
                "confoverrides": {"thumb_image_target_fullsize": True},
            },
            "_images/tux.png",
            ["tux.100x118.png", "tux.png"],
        ),
    ],
    indirect=["app_params"],
    ids=lambda param: str(param) if isinstance(param, list) else param,
)
@pytest.mark.sphinx("html", testroot="defaults", confoverrides={"thumb_image_resize_width": 100})
def test_target_fullsize(
    outdir: Path, img_tags: list[element.Tag], expected_href: Optional[str], expected_files: list[str], app: SphinxTestApp
):
    """TODO."""
    # Confirm href.
    img_hrefs = [t.parent.get("href") for t in img_tags]
    assert img_hrefs == [expected_href]
    # Confirm presence of original image.
    assert sorted(f.name for f in (outdir / "_images").iterdir()) == expected_files
