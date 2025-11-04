"""Tests."""

from typing import List, Optional

import pytest
from bs4 import element


def assert_image(image: element.Tag, src: str, href: Optional[str]):
    """TODO."""
    assert image.get("src") == src
    target = image.parent
    if href is None:
        assert target.name != "a"
    else:
        assert target.name == "a"
        assert target.get("href") == href


@pytest.mark.sphinx("html", testroot="defaults")
def test_index_rst(img_tags: List[element.Tag]):
    """Test."""
    assert_image(img_tags[2], "_images/tux.png", "https://google.com")
    assert_image(img_tags[3], "_images/tux.png", "https://aol.com")
