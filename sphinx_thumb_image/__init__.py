"""Sphinx Thumb Image.

Sphinx extension that resizes images into thumbnails on the fly.

https://sphinx-thumb-image.readthedocs.io
https://github.com/Robpol86/sphinx-thumb-image
https://pypi.org/project/sphinx-thumb-image
"""

from sphinx.application import Sphinx

from sphinx_thumb_image.directives import ThumbFigure, ThumbImage

__author__ = "@Robpol86"
__license__ = "BSD-2-Clause"
__version__ = "0.0.1"


def setup(app: Sphinx) -> dict[str, str]:
    """Register extension components with Sphinx (called by Sphinx during phase 0 [initialization]).

    :param app: Sphinx application object.

    :returns: Extension version.
    """
    app.add_config_value("thumb_image_scale_width", None, "html")
    app.add_config_value("thumb_image_scale_height", None, "html")
    app.add_directive("thumb-image", ThumbImage)
    app.add_directive("thumb-figure", ThumbFigure)
    return {
        "parallel_read_safe": False,  # TODO
        "parallel_write_safe": False,  # TODO
        "version": __version__,
    }
