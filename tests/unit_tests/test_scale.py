"""Test image scaling in the directive with dimensions specified in directive options and Sphinx configs.

TODO::
* If no thumbs are used (low res) then _thumbs shouldn't exist.
"""

import re
from pathlib import Path
from typing import Optional

import PIL.Image
import pytest
from bs4 import element
from sphinx.errors import SphinxWarning
from sphinx.testing.util import SphinxTestApp


@pytest.mark.parametrize(
    "app_params,expected",
    [
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :resize-width: 132"}}, [132, 156]),
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :resize-height: 78"}}, [66, 78]),
        (
            {
                "write_docs": {"index.rst": ".. thumb-image:: _images/tux.png"},
                "confoverrides": {"thumb_image_resize_width": 88},
            },
            [88, 104],
        ),
        (
            {
                "write_docs": {"index.rst": ".. thumb-image:: _images/tux.png"},
                "confoverrides": {"thumb_image_resize_height": 62},
            },
            [52, 62],
        ),
    ],
    indirect=["app_params"],
    ids=lambda param: str(param) if isinstance(param, list) else param,
)
@pytest.mark.sphinx("html", testroot="defaults")
def test_resize_width_height(outdir: Path, img_tags: list[element.Tag], expected: list[int, int]):
    """Test different ways to specify thumbnail size."""
    # Confirm img src.
    img_src = [t["src"] for t in img_tags]
    assert img_src == [f"_images/tux.{expected[0]}x{expected[1]}.png"]
    # Confirm image file's new dimensions.
    image_path = outdir / img_src[0]
    with PIL.Image.open(image_path) as image:
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
    """Confirm error is raised if user does not specify any dimensions."""
    with pytest.raises(SphinxWarning) as exc:
        app.build()
    assert '"resize-width" option is missing' in exc.value.args[0]


@pytest.mark.parametrize(
    "app_params,expected",
    [
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :resize-width: 100"}}, None),
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :resize-width: 100px"}}, None),
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :resize-width: 100%"}}, SphinxWarning),
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :resize-width: 100in"}}, SphinxWarning),
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :resize-width: 100.2"}}, SphinxWarning),
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :resize-width: -100"}}, SphinxWarning),
    ],
    indirect=["app_params"],
    ids=lambda param: m[0] if (m := re.findall(r':resize-width:\s*[^\'"]+', str(param))) else param,
)
@pytest.mark.sphinx("html", testroot="defaults")
def test_units(app: SphinxTestApp, expected: Optional[Exception]):
    """Test supported and unsupported scaling units.

    TODO::
    - Test height/option/config permutations.
    """
    if expected is None:
        app.build()
        return

    with pytest.raises(Exception) as exc:
        app.build()
    assert "invalid option value" in exc.value.args[0]
