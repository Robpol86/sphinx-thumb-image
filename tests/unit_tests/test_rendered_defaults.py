"""Tests."""

from typing import List

import pytest
from bs4 import element


@pytest.mark.sphinx("html", testroot="defaults")
def test_index_rst(img_tags: List[element.Tag]):
    """Test."""
    image = img_tags[0]
    assert image.get("src") == "_images/tux.png"
    target = image.parent
    assert target.name == "a"
    assert target.get("href") == "https://google.com"

    image = img_tags[1]
    assert image.get("src") == "_images/tux.png"
    target = image.parent
    assert target.name == "a"
    assert target.get("href") == "https://google.com"
    caption = image.find_parent("figure").figcaption.text
    assert "This is the caption." in caption
