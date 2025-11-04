"""Tests."""

from typing import List

import pytest
from bs4 import element

from .utils import assert_image


@pytest.mark.sphinx("html", testroot="defaults")
def test_index_rst(img_tags: List[element.Tag]):
    """Test."""
    assert_image(img_tags[0], "_images/tux-00.png")  # TODO _images/tux-00.png
    assert_image(img_tags[1], "_images/tux-01.png")  # TODO _images/tux-01.png
    assert_image(img_tags[2], "_images/tux-02.png", "https://google.com")
    assert_image(img_tags[3], "_images/tux-03.png", "https://aol.com")
    assert_image(img_tags[4], "_images/tux-04.png")
    assert_image(img_tags[5], "_images/tux-05.png")
