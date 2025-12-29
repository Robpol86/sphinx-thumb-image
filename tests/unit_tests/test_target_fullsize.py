"""TODO."""

from pathlib import Path

import pytest
from bs4 import element


@pytest.mark.parametrize(
    "app_params,expected",
    [
        (
            {
                "write_docs": {"index.rst": ".. thumb-image:: _images/tux.png"},
                "confoverrides": {"thumb_image_resize_width": 100},
            },
            None,
        ),
        (
            {
                "write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :target-fullsize:"},
                "confoverrides": {"thumb_image_resize_width": 100},
            },
            "_images/tux.png",
        ),
        (
            {
                "write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :target: google.com"},
                "confoverrides": {"thumb_image_resize_width": 100},
            },
            "google.com",
        ),
        (
            {
                "write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :target: google.com\n  :target-fullsize:"},
                "confoverrides": {"thumb_image_resize_width": 100},
            },
            "_images/tux.png",
        ),
        (
            {
                "write_docs": {"index.rst": ".. thumb-image:: _images/tux.png"},
                "confoverrides": {"thumb_image_resize_width": 100, "thumb_image_target_fullsize": True},
            },
            "_images/tux.png",
        ),
    ],
    indirect=["app_params"],
    ids=lambda param: param,  # TODO
)
@pytest.mark.sphinx("html", testroot="defaults", srcdir="test_target_original")
def test_target_original(outdir: Path, img_tags: list[element.Tag], expected: list[int, int]):
    """TODO."""
    pytest.skip("TODO assert listdir")  # TODO TDD first, then uncomment to confirm :target: works, then implement.
