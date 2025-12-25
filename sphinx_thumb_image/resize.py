"""TODO.

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

from sphinx_thumb_image.lib import ThumbRequest


class ThumbImageResize:
    """Resize images."""

    THUMBS_SUBDIR = "_thumbs"

    @classmethod
    def resize(cls, doctree_source_parent: Path, node_uri: Path, request: ThumbRequest, thumbs_dir: Path) -> Path:
        """Resize one image. Output image saved in TODO.

        :param doctree_source_parent: TODO
        :param node_uri: TODO
        :param request: TODO
        :param thumbs_dir: Directory to write thumbnails to.

        :returns: TODO
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
        for node in doctree.findall(lambda n: ThumbRequest.KEY in n):
            request: ThumbRequest = node[ThumbRequest.KEY]
            node_uri = Path(node["uri"])
            target = cls.resize(doctree_source.parent, node_uri, request, thumbs_dir)
            node["uri"] = relpath(target, start=doctree_source.parent)
