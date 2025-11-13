"""Tests."""

import pytest
from bs4 import element


@pytest.mark.parametrize(
    "app_params",
    [
        {"thumb_image_default_target": v}
        for v in [
            "__omit__",  # Handled in conftest.py.
            "fullsize",
            "google.com",
            "pfx/%s",
            "pfx/%(ignore)s",
            "pfx/%(fullsize)s",
            None,
        ]
    ],
    indirect=True,
    ids=lambda param: param["thumb_image_default_target"],
)
@pytest.mark.sphinx("html", testroot="defaults", confoverrides={"master_doc": "target"})
def test_target(request: pytest.FixtureRequest, img_tags: list[element.Tag]):
    """Test thumb_image_default_target and directive overrides."""
    assert img_tags[0].parent.get("href") == "https://google.com"
    assert img_tags[1].parent.get("href") == "https://aol.com/?x=%sample"
    assert img_tags[2].parent.get("href") == "_images/tux.png"
    assert img_tags[3].parent.get("href") == "_images/tux.png"
    assert img_tags[4].parent.name != "a"
    assert img_tags[5].parent.name != "a"
    assert img_tags[6].parent.get("href") == "https://github.com/User/Repo/blob/_images/tux.png"
    assert img_tags[7].parent.get("href") == "https://cloudflare.com/cdn/tux.png"
    thumb_image_default_target = request.node.callspec.params["app_params"]["thumb_image_default_target"]
    if thumb_image_default_target in ["__omit__", "fullsize"]:
        assert img_tags[8].parent.get("href") == "_images/tux.png"
        assert img_tags[9].parent.get("href") == "_images/tux.png"
    elif thumb_image_default_target in ["google.com", "pfx/%s", "pfx/%(ignore)s"]:
        assert img_tags[8].parent.get("href") == thumb_image_default_target
        assert img_tags[9].parent.get("href") == thumb_image_default_target
    elif thumb_image_default_target == "pfx/%(fullsize)s":
        assert img_tags[8].parent.get("href") == "pfx/_images/tux.png"
        assert img_tags[9].parent.get("href") == "pfx/_images/tux.png"
    elif thumb_image_default_target is None:
        assert img_tags[8].parent.name != "a"
        assert img_tags[9].parent.name != "a"
    else:
        pytest.fail("Unhandled thumb_image_default_target value")


@pytest.mark.sphinx("html", testroot="defaults", confoverrides={"master_doc": "sub/target"})
def test_sub_target(img_tags: list[element.Tag]):
    """Test with pages in subdirectories referencing images n directories up."""
    assert img_tags[0].parent.get("href") == "../_images/tux.png"
    assert img_tags[1].parent.get("href") == "https://github.com/User/Repo/blob/_images/tux.png"
    assert img_tags[2].parent.get("href") == "/_images/tux.png"
    assert img_tags[3].parent.get("href") == "https://github.com/User/Repo/blob/_images/tux.png"


def test_img_src():
    """Test.

    TODO::
    * If fullsize not linked by any directive then it should not be in the _build dir.
    * If no thumbs are used (low res) then _thumbs shouldn't exist.
    * REMEMBER: not all images in _images, can be in arbitrary locations.
    * Test two thumb-image:: using the same image but different resolutions.
    """
    pytest.skip("TODO")
