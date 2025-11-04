"""Utilities used by tests."""

from typing import Optional

from bs4 import element


def assert_image(image: element.Tag, src: str, href: Optional[str] = None):
    """Assert HTML image has the expected src and 'a href'."""
    assert image.get("src") == src
    target = image.parent
    if href is None:
        assert target.name != "a"
    else:
        assert target.name == "a"
        assert target.get("href") == href
