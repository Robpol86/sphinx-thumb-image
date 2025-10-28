"""Sphinx extension that resizes images into thumbnails on the fly.

https://sphinx-thumb-image.readthedocs.io
https://github.com/Robpol86/sphinx-thumb-image
https://pypi.org/project/sphinx-thumb-image
"""

from typing import Dict

from docutils.parsers.rst.directives import images
from sphinx.application import Sphinx

from sphinx_thumb_image import __version__


class ThumbImage(images.Image):
    """Thumb image directive."""

    option_spec = images.Image.option_spec.copy()


class ThumbFigure(images.Figure):
    """Thumb figure directive."""

    option_spec = images.Figure.option_spec.copy()


def setup(app: Sphinx) -> Dict[str, str]:
    """Called by Sphinx during phase 0 (initialization).

    :param app: Sphinx application object.

    :returns: Extension version.
    """
    app.add_directive("thumb-figure", ThumbFigure)
    app.add_directive("thumb-image", ThumbImage)
    return {"version": __version__}
