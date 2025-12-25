"""Image resizing module.

TODO::
- Log
- Cache
- Collisions
- Parallel
"""

from os.path import relpath
from pathlib import Path

import PIL.Image
from docutils.nodes import document
from sphinx.application import Sphinx

from sphinx_thumb_image.lib import ThumbNodeRequest


class ThumbImageResize:
    """Resize images."""

    THUMBS_SUBDIR = "_thumbs"

    @classmethod
    def resize(cls, doctree_source_parent: Path, node_uri: Path, request: ThumbNodeRequest, thumbs_dir: Path) -> Path:
        """Resize one image.

        Output image saved with the same relative path as the source image but in the thumbs directory.

        :param doctree_source_parent: Parent directory of the document's path.
        :param node_uri: Relative path to the image node, from the document's path.
        :param request: Image node's extension request object.
        :param thumbs_dir: Directory to write thumbnails to.

        :returns: Path to the output image.
        """
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
        """Resize all images in one Sphinx document.

        Called from the doctree-read event.

        :param app: Sphinx application object.
        :param doctree: Tree of docutils nodes.
        """
        thumbs_dir = app.env.doctreedir / cls.THUMBS_SUBDIR
        thumbs_dir.mkdir(exist_ok=True)
        doctree_source = Path(doctree["source"])
        for node in doctree.findall(lambda n: ThumbNodeRequest.KEY in n):
            request: ThumbNodeRequest = node[ThumbNodeRequest.KEY]
            node_uri = Path(node["uri"])
            target = cls.resize(doctree_source.parent, node_uri, request, thumbs_dir)
            node["uri"] = relpath(target, start=doctree_source.parent)
