"""Sphinx Thumb Image.

Resize images in Sphinx documents/pages to thumbnails.

https://sphinx-thumb-image.readthedocs.io
https://github.com/Robpol86/sphinx-thumb-image
https://pypi.org/project/sphinx-thumb-image
"""

import os

from sphinx.application import Sphinx

from sphinx_thumb_image.directives import ListTableThumbs, ThumbFigure, ThumbImage
from sphinx_thumb_image.lib import ThumbBackReference
from sphinx_thumb_image.resize import ThumbImageResize

__author__ = "@Robpol86"
__license__ = "BSD-2-Clause"
__version__ = "0.4.0"


def prune_outdated_thumbs(app: Sphinx):
    """TODO.

    TODO New config option to ignore mtime to noop this.

    TODO log
    """
    env = app.builder.env
    back_ref = ThumbBackReference(env)
    for thumb_path, source_path in back_ref.items():
        prune = False
        try:
            thumb_stat = thumb_path.stat()
        except IOError:
            back_ref.pop(thumb_path)
        try:
            source_stat = source_path.stat()
        except IOError:
            prune = True
        if thumb_stat.st_mtime_ns != source_stat.st_mtime_ns:
            prune = True
        if prune:
            os.unlink(thumb_path)  # TODO Sphinx has api for this?
            back_ref.pop(thumb_path)


def get_outdated(app: Sphinx, env, added, changed, removed) -> list[str]:
    """TODO.

    Get source/target and docname from env and if atime/mtime changes then return docnames.
    """
    return []  # e.g. ["index"]


def setup(app: Sphinx) -> dict[str, str]:
    """Register extension components with Sphinx (called by Sphinx during phase 0 [initialization]).

    :param app: Sphinx application object.

    :returns: Extension version.
    """
    app.add_config_value("thumb_image_resize_width", None, "env")
    app.add_config_value("thumb_image_resize_height", None, "env")
    app.add_config_value("thumb_image_resize_quality", None, "env")
    app.add_config_value("thumb_image_is_animated", False, "env")
    app.add_config_value("thumb_image_target_format", False, "env")
    app.add_config_value("thumb_image_target_format_substitutions", {}, "env")
    app.add_config_value("thumb_image_default_target", None, "env")
    app.add_directive("thumb-image", ThumbImage)
    app.add_directive("thumb-figure", ThumbFigure)
    app.add_directive("list-table-thumbs", ListTableThumbs)
    app.connect("builder-inited", prune_outdated_thumbs)
    app.connect("env-get-outdated", get_outdated)
    app.connect("doctree-read", ThumbImageResize.resize_images_in_document, priority=499)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": __version__,
    }
