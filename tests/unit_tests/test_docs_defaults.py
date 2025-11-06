"""Tests."""

from typing import List, Optional

import pytest
from bs4 import element


@pytest.mark.parametrize(
        "sphinx_app",
        [{"thumb_image_default_target": v} for v in ["_omit", "original", "None", "pfx/%(path)s", "invalid"]],
        indirect=True,
    )
@pytest.mark.sphinx("html", testroot="defaults")
def test_target(img_tags: List[element.Tag]):
    """Test thumb_image_default_target and directive overrides.

    # TODO thumb_image_default_target
    #       original
    #       None
    #       https://github.com/User/Repo/blob/%(path)s
    #       https://github.com/User/Repo/blob/docs/images/%(filename)s
    """
    def do_assert(image: element.Tag, href: Optional[str] = None):
        """Assert HTML image has the expected link or lack thereof."""
        target = image.parent
        if href is None:
            assert target.name != "a"
        else:
            assert target.name == "a"
            assert target.get("href") == href
    do_assert(img_tags[0], "https://google.com")
    do_assert(img_tags[1], "https://aol.com")
    pytest.skip("TODO")
    do_assert(img_tags[2], "_images/tux.png")
    do_assert(img_tags[3], "_images/tux.png")
    do_assert(img_tags[4], None)
    do_assert(img_tags[5], None)
    do_assert(img_tags[6], "https://github.com/User/Repo/blob/_images/tux.png")
    do_assert(img_tags[7], "https://github.com/User/Repo/blob/docs/images/tux.png")
    do_assert(img_tags[8], "_images/tux.png")
    do_assert(img_tags[9], "_images/tux.png")


def test_img_src():
    """Test.

    TODO::
    * If original not linked by any directive then it should not be in the _build dir.
    * If no thumbs are used (low res) then _thumbs shouldn't exist.
    """
    pytest.skip("TODO")
