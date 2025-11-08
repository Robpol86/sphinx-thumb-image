"""Tests."""

from typing import List

import pytest
from bs4 import element

from .utils import assert_image


@pytest.mark.sphinx("html", testroot="defaults")
def test_index_rst(img_tags: List[element.Tag]):
    """Test."""
    assert_image(img_tags[0], "_images/tux.png")
    assert_image(img_tags[1], "_images/tux.png")
    assert_image(img_tags[2], "_images/tux.png", "https://google.com")
    assert_image(img_tags[3], "_images/tux.png", "https://aol.com")
