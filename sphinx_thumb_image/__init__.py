"""Sphinx Thumb Image.

Sphinx extension that resizes images into thumbnails on the fly.

https://sphinx-thumb-image.readthedocs.io
https://github.com/Robpol86/sphinx-thumb-image
https://pypi.org/project/sphinx-thumb-image
"""

from sphinx.application import Sphinx
from sphinx.builders import Builder

from sphinx_thumb_image.directives import ThumbFigure, ThumbImage
from sphinx_thumb_image.resize import ThumbImageResize

__author__ = "@Robpol86"
__license__ = "BSD-2-Clause"
__version__ = "0.0.1"


def todo_write_started(app: Sphinx, builder: Builder):
    """TODO."""
    # builder.images.update({'_images/tux.png': 'tux.png'})
    # TODO but then I need to deal with collisions, etc.
    import pdb; pdb.set_trace()


def todo_doctree_resolved(app: Sphinx, doctree, docname: str):
    """TODO."""
    import pdb; pdb.set_trace()


def todo_missing_reference(app: Sphinx, env, node, contnode):
    """TODO."""
    import pdb; pdb.set_trace()


def setup(app: Sphinx) -> dict[str, str]:
    """Register extension components with Sphinx (called by Sphinx during phase 0 [initialization]).

    :param app: Sphinx application object.

    :returns: Extension version.
    """
    app.add_config_value("thumb_image_resize_width", None, "html")
    app.add_config_value("thumb_image_resize_height", None, "html")
    app.add_config_value("thumb_image_target_fullsize", False, "html")
    app.add_directive("thumb-image", ThumbImage)
    app.add_directive("thumb-figure", ThumbFigure)
    app.connect("doctree-read", ThumbImageResize.resize_images_in_document, priority=499)
    # app.connect("write-started", todo_write_started)
    # app.connect("doctree-resolved", todo_doctree_resolved)
    # app.connect("missing-reference", todo_missing_reference)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": __version__,
    }
