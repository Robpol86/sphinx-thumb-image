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
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html", testroot="defaults")
def test(outdir: Path):
    """Test."""
    image_path = outdir / "_images" / "tux.png"
    with PIL.Image.open(image_path) as image:
        assert image.size == (265, 314)  # TODO


@pytest.mark.sphinx("html", testroot="defaults")
def test_missing_width(app: SphinxTestApp):
    """Test."""
    pytest.skip("TODO")
    app.warningiserror = True
    with pytest.raises(ValueError) as exc:
        app.build()
    assert exc.value.args[0] == "Missing option 'scale-width'"
