"""Sphinx Thumb Image.

Sphinx extension that resizes images into thumbnails on the fly.

https://sphinx-thumb-image.readthedocs.io
https://github.com/Robpol86/sphinx-thumb-image
https://pypi.org/project/sphinx-thumb-image
"""

from os.path import relpath
from pathlib import Path

import PIL.Image
from docutils.nodes import document
from sphinx.application import Sphinx

from sphinx_thumb_image.directives import ThumbFigure, ThumbImage
from sphinx_thumb_image.lib import ThumbRequest

__author__ = "@Robpol86"
__license__ = "BSD-2-Clause"
__version__ = "0.0.1"


class ThumbImageResize:
    """TODO."""

    @classmethod
    def resize(cls, doctree_source_parent: Path, node_uri: Path, request :ThumbRequest, thumbs_dir: Path) -> Path:
        """TODO."""
        source = doctree_source_parent / node_uri
        with PIL.Image.open(source) as image:
            image.thumbnail((request.width or image.size[0], request.height or image.size[1]))
            thumb_file_name = f"{source.stem}.{image.size[0]}x{image.size[1]}{source.suffix}"
            target = thumbs_dir / node_uri.parent / thumb_file_name
            target.parent.mkdir(exist_ok=True)
            image.save(target)
        return target

    @classmethod
    def resize_images_in_document(cls, app: Sphinx, doctree: document):
        """TODO.

        - Log
        - Cache
        - Collisions
        - Parallel
        """
        thumbs_dir = app.env.doctreedir / "_thumbs"
        thumbs_dir.mkdir(exist_ok=True)
        doctree_source = Path(doctree["source"])
        for node in doctree.findall(lambda n: ThumbRequest.KEY in n):
            request: ThumbRequest = node[ThumbRequest.KEY]
            node_uri = Path(node["uri"])
            target = cls.resize(doctree_source.parent, node_uri, request, thumbs_dir)
            node["uri"] = relpath(target, start=doctree_source.parent)


def setup(app: Sphinx) -> dict[str, str]:
    """Register extension components with Sphinx (called by Sphinx during phase 0 [initialization]).

    :param app: Sphinx application object.

    :returns: Extension version.
    """
    app.add_config_value("thumb_image_resize_width", None, "html")
    app.add_config_value("thumb_image_resize_height", None, "html")
    app.add_directive("thumb-image", ThumbImage)
    app.add_directive("thumb-figure", ThumbFigure)
    app.connect("doctree-read", ThumbImageResize.resize_images_in_document, priority=499)
    return {
        "parallel_read_safe": False,  # TODO
        "parallel_write_safe": False,  # TODO
        "version": __version__,
    }
