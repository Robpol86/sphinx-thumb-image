"""Test image scaling in the directive with dimensions specified in directive options and Sphinx configs.

TODO::
* If fullsize not linked by any directive then it should not be in the _build dir.
* If no thumbs are used (low res) then _thumbs shouldn't exist.
* REMEMBER: not all images in _images, can be in arbitrary locations.
* Test two thumb-image:: using the same image but different quality.
"""

from pathlib import Path
from textwrap import dedent

import PIL.Image
import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.parametrize(
    "app_params,expected",
    [
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :scale-width: 100"}}, [265, 314]),  # TODO
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :scale-height: 100"}}, [265, 314]),
        (
            {
                "write_docs": {"index.rst": ".. thumb-image:: _images/tux.png"},
                "confoverrides": {"thumb_image_scale_width": 100},
            },
            [265, 314],
        ),
        (
            {
                "write_docs": {"index.rst": ".. thumb-image:: _images/tux.png"},
                "confoverrides": {"thumb_image_scale_height": 100},
            },
            [265, 314],
        ),
    ],
    indirect=["app_params"],
    ids=lambda param: str(param) if isinstance(param, list) else param,  # Show "expected" values instead of expected0.
)
@pytest.mark.sphinx("html", testroot="defaults")
def test_scale_width_height(outdir: Path, expected: list[int, int]):
    """Test different ways to specify thumbnail size."""
    image_path = outdir / "_images" / "tux.png"
    with PIL.Image.open(image_path) as image:
        assert image.size[0] == expected[0]
        assert image.size[1] == expected[1]


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    write_docs={
        "index.rst": dedent("""
            .. thumb-image:: _images/tux.png
        """),
    },
)
def test_missing_width(app: SphinxTestApp):
    """Test."""
    with pytest.raises(ValueError) as exc:
        app.build()
    assert exc.value.args[0] == "Missing option 'scale-width'"
