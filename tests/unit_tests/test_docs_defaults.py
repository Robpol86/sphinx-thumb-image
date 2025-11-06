"""Tests."""

from typing import List

import pytest
from bs4 import element


@pytest.mark.parametrize(
        "sphinx_app",
        [{"thumb_image_default_target": v} for v in ["__omit__", "original", "None", "pfx/%(path)s", "invalid"]],
        indirect=True,
        ids=lambda param: param["thumb_image_default_target"],
    )
@pytest.mark.sphinx("html", testroot="defaults")
def test_target(img_tags: List[element.Tag], request: pytest.FixtureRequest):
    """Test thumb_image_default_target and directive overrides.

    # TODO thumb_image_default_target
    #       original
    #       None
    #       https://github.com/User/Repo/blob/%(path)s
    #       https://github.com/User/Repo/blob/docs/images/%(filename)s
    """
    assert img_tags[0].parent.get("href") == "https://google.com"
    assert img_tags[1].parent.get("href") == "https://aol.com"
    pytest.skip("TODO")
    assert img_tags[2].parent.get("href") == "_images/tux.png"
    assert img_tags[3].parent.get("href") == "_images/tux.png"
    assert img_tags[4].parent.name != "a"
    assert img_tags[5].parent.name != "a"
    assert img_tags[6].parent.get("href") == "https://github.com/User/Repo/blob/_images/tux.png"
    assert img_tags[7].parent.get("href") == "https://github.com/User/Repo/blob/docs/images/tux.png"
    thumb_image_default_target = request.node.callspec.params["sphinx_app"]["thumb_image_default_target"]
    if thumb_image_default_target in ["__omit__", "original"]:
        assert img_tags[8].parent.get("href") == "_images/tux.png"
        assert img_tags[9].parent.get("href") == "_images/tux.png"
    else:
        pytest.skip("TODO Not Implemented")


def test_img_src():
    """Test.

    TODO::
    * If original not linked by any directive then it should not be in the _build dir.
    * If no thumbs are used (low res) then _thumbs shouldn't exist.
    """
    pytest.skip("TODO")
