"""Test image scaling in the directive with dimensions specified in directive options and Sphinx configs.

TODO::
* If fullsize not linked by any directive then it should not be in the _build dir.
* If no thumbs are used (low res) then _thumbs shouldn't exist.
* REMEMBER: not all images in _images, can be in arbitrary locations.
* Test two thumb-image:: using the same image but different quality.
"""

from pathlib import Path

import PIL.Image
import pytest
from bs4 import element
from sphinx.testing.util import SphinxTestApp


@pytest.mark.parametrize(
    "app_params,expected",
    [
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :scale-width: 132"}}, [132, 157]),
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :scale-height: 78"}}, [66, 78]),
        (
            {
                "write_docs": {"index.rst": ".. thumb-image:: _images/tux.png"},
                "confoverrides": {"thumb_image_scale_width": 88},
            },
            [88, 104],
        ),
        (
            {
                "write_docs": {"index.rst": ".. thumb-image:: _images/tux.png"},
                "confoverrides": {"thumb_image_scale_height": 62},
            },
            [53, 62],
        ),
    ],
    indirect=["app_params"],
    ids=lambda param: str(param) if isinstance(param, list) else param,  # Show "expected" values instead of expected0.
)
@pytest.mark.sphinx("html", testroot="defaults")
def test_scale_width_height(outdir: Path, img_tags: list[element.Tag], expected: list[int, int]):
    """Test different ways to specify thumbnail size."""
    # Confirm img src.
    img_src = [t["src"] for t in img_tags]
    assert img_src == ["_images/tux.png"]
    # Confirm image file's new dimensions.
    image_path = outdir / img_src[0]
    with PIL.Image.open(image_path) as image:
        pytest.skip("TODO unskip after implementing scaling")
        assert image.size[0] == expected[0]
        assert image.size[1] == expected[1]


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    write_docs={
        "index.rst": ".. thumb-image:: _images/tux.png",
    },
)
def test_missing_width(app: SphinxTestApp):
    """Test."""
    with pytest.raises(ValueError) as exc:
        app.build()
    assert exc.value.args[0] == "Missing option 'scale-width'"
