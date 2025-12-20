"""Test image scaling in the directive with dimensions specified in directive options and Sphinx configs.

TODO::
* If fullsize not linked by any directive then it should not be in the _build dir.
* If no thumbs are used (low res) then _thumbs shouldn't exist.
* REMEMBER: not all images in _images, can be in arbitrary locations.
* Test two thumb-image:: using the same image but different quality.
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
    """Confirm error is raised if user does not specify any dimensions."""
    app.warningiserror = True
    with pytest.raises(SphinxWarning) as exc:
        app.build()
    assert '"scale-width" option is missing' in exc.value.args[0]


@pytest.mark.parametrize(
    "app_params,expected",
    [
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :scale-width: 100"}}, None),
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :scale-width: 100px"}}, None),
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :scale-width: 100%"}}, SphinxWarning),
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :scale-width: 100in"}}, SphinxWarning),
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :scale-width: 100.2"}}, SphinxWarning),
        ({"write_docs": {"index.rst": ".. thumb-image:: _images/tux.png\n  :scale-width: -100"}}, SphinxWarning),
    ],
    indirect=["app_params"],
    ids=lambda param: m[0] if (m := re.findall(r':scale-width:\s*[^\'"]+', str(param))) else param,
)
@pytest.mark.sphinx("html", testroot="defaults")
def test_units(app: SphinxTestApp, expected: Optional[Exception]):
    """Test supported and unsupported scaling units."""
    app.warningiserror = True

    if expected is None:
        app.build()
        return

    with pytest.raises(expected) as exc:
        app.build()
    assert "invalid option value" in exc.value.args[0]
