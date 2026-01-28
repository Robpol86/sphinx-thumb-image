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
            .. list-table-thumbs::
                :resize-width: 132

                * - .. thumb-image:: _images/tux.png
                        :no-resize:
                  - .. thumb-image:: _images/tux.png
                * - .. thumb-image:: _images/tux.png
                  - .. thumb-image:: _images/tux.png
                        :resize-height: 78

            .. list-table-thumbs::
                :resize-width: 90

                * - .. thumb-image:: _images/tux.png
                        :no-resize:
                  - .. thumb-image:: _images/tux.png
                * - .. thumb-image:: _images/tux.png
                  - .. thumb-image:: _images/tux.png
                        :resize-height: 78

            .. list-table-thumbs::

                * - .. thumb-image:: _images/tux.png
                        :no-resize:
                  - .. thumb-image:: _images/tux.png
                * - .. thumb-image:: _images/tux.png
                  - .. thumb-image:: _images/tux.png
                        :resize-height: 78
        """),
    },
)
def test_list_table(img_tags: list[element.Tag]):
    """Test setting default widths in list-table."""
    img_src = [t["src"] for t in img_tags]
    assert img_src == [
        "_images/tux.png",
        "_images/tux.132x156.png",
        "_images/tux.132x156.png",
        "_images/tux.66x78.png",
        # sep
        "_images/tux.png",
        "_images/tux.90x107.png",
        "_images/tux.90x107.png",
        "_images/tux.66x78.png",
        # sep
        "_images/tux.png",
        "_images/tux.100x118.png",
        "_images/tux.100x118.png",
        "_images/tux.66x78.png",
    ]
