"""Sphinx Thumb Image.

Sphinx extension that resizes images into thumbnails on the fly.

https://sphinx-thumb-image.readthedocs.io
https://github.com/Robpol86/sphinx-thumb-image
https://pypi.org/project/sphinx-thumb-image
"""

import os
import pdb

import PIL.Image
from sphinx.application import Sphinx
from sphinx.transforms.post_transforms import SphinxPostTransform

from sphinx_thumb_image.directives import ThumbFigure, ThumbImage
from sphinx_thumb_image.lib import ThumbRequest

__author__ = "@Robpol86"
__license__ = "BSD-2-Clause"
__version__ = "0.0.1"


def todo_write_started(app, builder):
    """TODO."""
    # TODO Builder.post_process_images() is what determines final image file names
    # TODO node["candidates"]?
    if os.environ.get("RP_PDB", ""):
        pdb.set_trace()


class TodoPostTransform(SphinxPostTransform):
    """TODO."""

    default_priority = 523

    def run(self, **kwargs):
        """TODO."""
        for node in self.document.findall(lambda n: ThumbRequest.KEY in n):
            request: ThumbRequest = node[ThumbRequest.KEY]
            source = self.env.srcdir / node["candidates"].pop("*")
            target = self.env.doctreedir / "_thumbs" / f"{source.stem}.th{source.suffix}"  # TODO collisions
            target.parent.mkdir(exist_ok=True)
            with PIL.Image.open(source) as image:
                image.thumbnail((request.width or image.size[0], request.height or image.size[1]))
                image.save(target)
                mimetype = image.get_format_mimetype()
            self.env.images.add_file(self.env.docname, str(target))
            node["candidates"][mimetype] = node["uri"] = str(target)
            if os.environ.get("RP_PDB", ""):
                pdb.set_trace()


def setup(app: Sphinx) -> dict[str, str]:
    """Register extension components with Sphinx (called by Sphinx during phase 0 [initialization]).

    :param app: Sphinx application object.

    :returns: Extension version.
    """
    app.add_config_value("thumb_image_scale_width", None, "html")
    app.add_config_value("thumb_image_scale_height", None, "html")
    app.add_directive("thumb-image", ThumbImage)
    app.add_directive("thumb-figure", ThumbFigure)
    app.connect("write-started", todo_write_started)
    app.add_post_transform(TodoPostTransform)
    return {
        "parallel_read_safe": False,  # TODO
        "parallel_write_safe": False,  # TODO
        "version": __version__,
    }
