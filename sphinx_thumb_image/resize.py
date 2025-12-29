"""Image resizing module."""

from os.path import relpath
from pathlib import Path

import PIL.Image
from docutils.nodes import document
from portalocker import Lock, LockException
from sphinx.application import Sphinx
from sphinx.util import logging

from sphinx_thumb_image.lib import ThumbNodeRequest


class ThumbImageResize:
    """Resize images."""

    THUMBS_SUBDIR = "_thumbs"

    @classmethod
    def resize(cls, source: Path, target_dir: Path, request: ThumbNodeRequest) -> Path:
        """Resize one image.

        Output image saved with the same relative path as the source image but in the thumbs directory.

        :param source: Path to image file to resize.
        :param target_dir: Path to directory to write resized output image to.
        :param request: Image node's extension request object.

        :returns: Path to the output image.
        """
        log = logging.getLogger(__name__)
        with PIL.Image.open(source) as image:
            source_size = image.size
            image.thumbnail((request.width or source_size[0], request.height or source_size[1]))
            target_size = image.size
            thumb_file_name = f"{source.stem}.{target_size[0]}x{target_size[1]}{source.suffix}"
            target = target_dir / thumb_file_name
            if target.exists():
                return target
            target.parent.mkdir(exist_ok=True, parents=True)
            lock_file = target.parent / f"{target.name}.lock"
            try:
                with Lock(lock_file, timeout=0):
                    if target.exists():
                        return target
                    log.debug(f"resizing {source} ({source_size[0]}x{source_size[1]}) to {target}")
                    image.save(target)
            except LockException:
                return target
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
        doctree_subdir = doctree_source.parent.relative_to(app.srcdir)
        for node in doctree.findall(lambda n: ThumbNodeRequest.KEY in n):
            request: ThumbNodeRequest = node[ThumbNodeRequest.KEY]
            node_uri = Path(node["uri"])
            source = doctree_source.parent / node_uri
            target_dir = thumbs_dir / doctree_subdir / node_uri.parent
            target = cls.resize(source, target_dir, request)
            node["uri"] = relpath(target, start=doctree_source.parent)
