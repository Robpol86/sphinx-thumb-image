"""Tests."""

from typing import List

import pytest
from bs4 import element

from .utils import assert_image


@pytest.mark.sphinx("html", testroot="defaults")
def test_index_rst(img_tags: List[element.Tag]):
    """Test."""
    pytest.skip("TODO")
    assert_image(img_tags[0], "_thumbs/tux-00.png", "_images/tux-00.png")
    assert_image(img_tags[1], "_thumbs/tux-01.png", "_images/tux-01.png")
    assert_image(img_tags[2], "_thumbs/tux-02.png", "https://google.com")
    assert_image(img_tags[3], "_thumbs/tux-03.png", "https://aol.com")
    assert_image(img_tags[4], "_thumbs/tux-04.png")
    assert_image(img_tags[5], "_thumbs/tux-05.png")

    thumbs = []  # TODO dir listing of _build/_thumbs output
    assert thumbs == [
        "_thumbs/tux-00.png",
        "_thumbs/tux-01.png",
        "_thumbs/tux-02.png",
        "_thumbs/tux-03.png",
        "_thumbs/tux-04.png",
        "_thumbs/tux-05.png",
    ]

    images = []  # TODO dir listing of _build/_images output
    assert images == [
        "_images/tux-00.png",
        "_images/tux-01.png",
    ]
