"""Utilities used by tests."""

from typing import Optional

from bs4 import element


def assert_image(image: element.Tag, src: str, href: Optional[str] = None):
    """Assert HTML image has the expected src and 'a href'."""
    # Assert src and href in HTML.
    assert image.get("src") == src
    target = image.parent
    if href is None:
        assert target.name != "a"
    else:
        assert target.name == "a"
        assert target.get("href") == href

    # Assert thumb file exists.
    # all_thumnbs = []  # TODO ls _thumbs in output
    # assert src in all_thumnbs

    # # Assert original files (not)exists.
    # all_images = []  # TODO ls _images in output
    # if target_exists:
    #     pass  # TODO assert exists(href)
