"""Sphinx extension that resizes images into thumbnails on the fly.

https://sphinx-thumb-image.readthedocs.io
https://github.com/Robpol86/sphinx-thumb-image
https://pypi.org/project/sphinx-thumb-image
"""

from sphinx.application import Sphinx

from sphinx_thumb_image import __version__
from sphinx_thumb_image.directives import ThumbFigure, ThumbImage


def setup(app: Sphinx) -> dict[str, str]:
    """Register extension components with Sphinx (called by Sphinx during phase 0 [initialization]).

    :param app: Sphinx application object.

    :returns: Extension version.
    """
    app.add_config_value("thumb_image_default_ext", "jpg", "html")
    app.add_config_value("thumb_image_default_format", None, "html")
    app.add_config_value("thumb_image_default_height", None, "html")
    app.add_config_value("thumb_image_default_quality", 100, "html")
    app.add_config_value("thumb_image_default_target", "fullsize", "html")
    app.add_config_value("thumb_image_default_width", None, "html")
    app.add_directive("thumb-image", ThumbImage)
    app.add_directive("thumb-figure", ThumbFigure)
    return {
        "parallel_read_safe": False,  # TODO
        "parallel_write_safe": False,  # TODO
        "version": __version__,
    }
