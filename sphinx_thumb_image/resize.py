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


def append(outdir: Path, msg: str):
    """TODO remove."""
    log_file: Path = outdir / "sphinx-thumb-image-log.log"
    with log_file.open("a") as f:
        f.write(msg + "\n")


class ThumbImageResize:
    """Resize images."""

    THUMBS_SUBDIR = "_thumbs"

    @classmethod
    def resize(cls, source: Path, target_dir: Path, request: ThumbNodeRequest, app: Sphinx) -> Path:
        """Resize one image.

        Output image saved with the same relative path as the source image but in the thumbs directory.

        :param source: Path to image file to resize.
        :param target_dir: Path to directory to write resized output image to.
        :param request: Image node's extension request object.
        :param app: TODO REMOVE

        :returns: Path to the output image.
        """
        append(app.builder.outdir, f"SOURCE {source}")
        with PIL.Image.open(source) as image:
            image.thumbnail((request.width or image.size[0], request.height or image.size[1]))
            thumb_file_name = f"{source.stem}.{image.size[0]}x{image.size[1]}{source.suffix}"
            target = target_dir / thumb_file_name
            # TODO if file exists return target
            # TODO get lock
            # TODO if lock failed return target
            append(app.builder.outdir, f"TARGET {target}")
            target.parent.mkdir(exist_ok=True, parents=True)
            image.save(target)
            # TODO release lock
        append(app.builder.outdir, f"DONE {target}")
        return target

    @classmethod
    def resize_images_in_document(cls, app: Sphinx, doctree: document):
        """Resize all images in one Sphinx document.

        Called from the doctree-read event.

        :param app: Sphinx application object.
        :param doctree: Tree of docutils nodes.
        """
        append(app.builder.outdir, f"START START START START START START {doctree['source']}")
        thumbs_dir = app.env.doctreedir / cls.THUMBS_SUBDIR
        thumbs_dir.mkdir(exist_ok=True)
        doctree_source = Path(doctree["source"])
        doctree_subdir = doctree_source.parent.relative_to(app.srcdir)
        for node in doctree.findall(lambda n: ThumbNodeRequest.KEY in n):
            request: ThumbNodeRequest = node[ThumbNodeRequest.KEY]
            node_uri = Path(node["uri"])
            source = doctree_source.parent / node_uri
            target_dir = thumbs_dir / doctree_subdir / node_uri.parent
            target = cls.resize(source, target_dir, request, app)
            node["uri"] = relpath(target, start=doctree_source.parent)
        append(app.builder.outdir, f"END END END END END END END END END END {doctree['source']}")
