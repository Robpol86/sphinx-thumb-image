"""Test support for setting resize-width in a list-table and having it apply to all thumb images within."""

from textwrap import dedent

import pytest
from bs4 import element


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    confoverrides={
        "thumb_image_resize_width": 100,  # ignored
    },
    write_docs={
        "index.rst": dedent("""
            .. list-table::
                :resize-width: 132
                * - .. thumb-image:: _images/tux.png
                  - .. thumb-image:: _images/tux.png
                        :no-resize:
                * - .. thumb-image:: _images/tux.png
                        :resize-height: 78
                  - .. thumb-image:: _images/tux.png
        """),
    },
)
def test_list_table(img_tags: list[element.Tag]):
    """Test setting default widths in list-table."""
    img_src = [t["src"] for t in img_tags]
    assert img_src == [
        f"_images/tux.132x156.png",
        f"_images/tux.png",
        f"_images/tux.66x78.png",
        f"_images/tux.132x156.png",
    ]
