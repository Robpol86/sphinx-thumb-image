"""Image resizing module."""

from os.path import relpath
from pathlib import Path
from typing import Optional

import PIL.Image
import PIL.ImageFile
import PIL.ImageSequence
from docutils.nodes import Element, document
from portalocker import LockException, TemporaryFileLock
from sphinx.application import Sphinx
from sphinx.util import logging

from sphinx_thumb_image.lib import ThumbNodeRequest


class ThumbImageResize:
    """Resize images."""

    THUMBS_SUBDIR = "_thumbs"

    def __init__(self, source: Path, target_dir: Path, image: PIL.Image):
        """Instantiate class to resize one image.

        :param source: Path to image file to resize.
        :param target_dir: Path to directory to write resized output image to.
        :param image: TODO
        """
        self.source = source
        self.target_dir = target_dir
        self.image = image

    def save_animated(self, image: PIL.ImageFile.ImageFile, target: Path, target_size: tuple[int, int], **kwargs):
        """Save all frames in an animated image file to the target file.

        :param image: Opened source image.
        :param target: Path to target file.
        :param target_size: Image width and height to resize to.
        :param kwargs: Pass additional keyword arguments to PIL.save().
        """
        frames = []
        for frame in PIL.ImageSequence.Iterator(image):
            frame_resized = frame.resize(target_size)
            frames.append(frame_resized)
        disposal = 2  # https://github.com/Robpol86/sphinx-thumb-image/issues/43
        frames[0].save(target, save_all=True, append_images=frames[1:], disposal=disposal, **kwargs)

    def resize(self, request: ThumbNodeRequest, doctree: document, node: Element) -> Optional[Path]:
        """Resize one image.

        Output image saved with the same relative path as the source image but in the thumbs directory.

        :param request: Image node's extension request object.
        :param doctree: Current document.
        :param node: Current image node.

        :returns: Path to the output image or None if no resizing is done.
        """
        log = logging.getLogger(__name__)
        source_size = self.image.size
        # Get target size.
        if request.is_animated:
            image_copy = self.image.copy()
            image_copy.thumbnail((request.width or source_size[0], request.height or source_size[1]))
            target_size = image_copy.size
        else:
            self.image.thumbnail((request.width or source_size[0], request.height or source_size[1]))
            target_size = self.image.size
        if target_size[0] >= source_size[0]:
            paren = f"{node['uri']} {source_size[0]}x{source_size[1]}"
            message = f"requested thumbnail size is not smaller than source image ({paren})"
            doctree.reporter.warning(message, source=node.source, line=node.line)
            return None
        # Get target file path.
        if request.quality:
            thumb_file_name = f"{self.source.stem}.{target_size[0]}x{target_size[1]}.{request.quality}{self.source.suffix}"
        else:
            thumb_file_name = f"{self.source.stem}.{target_size[0]}x{target_size[1]}{self.source.suffix}"
        target = self.target_dir / thumb_file_name
        if target.exists():
            log.debug(f"skipping {self.source} ({target} exists)")
            return target
        # Write to target file path.
        target.parent.mkdir(exist_ok=True, parents=True)
        lock_file = target.parent / f"{target.name}.lock"
        try:
            with TemporaryFileLock(lock_file, timeout=0):
                if target.exists():
                    log.debug(f"skipping {self.source} ({target} exists after lock)")
                    return target
                log.debug(f"resizing {self.source} ({source_size[0]}x{source_size[1]}) to {target}")
                kwargs = dict(format=self.image.format)
                if request.quality:
                    kwargs["quality"] = request.quality
                if request.is_animated:
                    self.save_animated(self.image, target, target_size, **kwargs)
                else:
                    self.image.save(target, **kwargs)
        except LockException:
            log.debug(f"skipping {self.source} ({target} exists after race)")
            return target
        return target

    @classmethod
    def resize_images_in_document(cls, app: Sphinx, doctree: document):
        """Resize all images in one Sphinx document.

        Called from the doctree-read event.

        :param app: Sphinx application object.
        :param doctree: Current document.
        """
        log = logging.getLogger(__name__)
        thumbs_dir = app.env.doctreedir / cls.THUMBS_SUBDIR
        doctree_source = Path(doctree["source"])
        for node in doctree.findall(lambda n: ThumbNodeRequest.KEY in n):
            request: ThumbNodeRequest = node[ThumbNodeRequest.KEY]
            if request.no_resize:
                continue
            imguri = node["uri"]
            if imguri.startswith("data:"):
                doctree.reporter.warning("embedded images (data:...) are not supported", source=node.source, line=node.line)
                continue
            if imguri.find("://") != -1:
                doctree.reporter.warning("external images are not supported", source=node.source, line=node.line)
                continue
            path_rel, path_abs = app.env.relfn2path(imguri, app.env.docname)
            source = Path(path_abs)
            if not source.is_file():
                continue  # Subclassed Image directive already emits a warning in this case.
            target_dir = thumbs_dir / Path(path_rel).parent
            try:
                log.debug(f"opening {source}")
                with PIL.Image.open(source) as image:
                    instance = cls(source, target_dir, image)
                    target = instance.resize(request, doctree, node)
            except Exception as exc:
                doctree.reporter.error(f"failed to resize {source}: {exc}", source=node.source, line=node.line)
                raise
            if not target:
                continue
            node["uri"] = relpath(target, start=doctree_source.parent)
