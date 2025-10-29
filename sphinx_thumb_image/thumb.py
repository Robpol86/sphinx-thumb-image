"""Sphinx extension that resizes images into thumbnails on the fly.

https://sphinx-thumb-image.readthedocs.io
https://github.com/Robpol86/sphinx-thumb-image
https://pypi.org/project/sphinx-thumb-image

TODO:
* Support pdf and non-html builders
* If source image <= thumb size: noop
* Support parallel resizing, use lock files (one image may be referenced by multiple pages)
* Supported targets:
    * No target: just resize image, _build dir should not have source images, just thumbnails
    * Link original (default): embedded image is thumb, but source image should be in _build and linked to
    * Formatted link: Let user specify in config and/or directive a %s formatted link to original (e.g. GitHub blob)
    * :target: override as user expects
* thumb-image directive
    * Default scales down to default width
    * :thumb_width: 700px (unitless == px, no other units supported)
    * :no_target:
    * :target_fmt: https://localhost/images/%s
* config option to thumbisize all images/figures (sphinx directives)
    * No new directive options for ..image/..figure
* Remote/linked images unsupported
* Supported image formats: jpg png bmp gif gif[animated] apng svg webp
"""

from typing import Dict

from docutils.parsers.rst.directives import images
from sphinx.application import Sphinx

from sphinx_thumb_image import __version__


class ThumbImage(images.Image):
    """Thumbnail image directive."""

    option_spec = images.Image.option_spec.copy()


class ThumbFigure(images.Figure):
    """Thumbnail figure directive."""

    option_spec = images.Figure.option_spec.copy()


def setup(app: Sphinx) -> Dict[str, str]:
    """Called by Sphinx during phase 0 (initialization).

    :param app: Sphinx application object.

    :returns: Extension version.
    """
    app.add_directive("thumb-image", ThumbImage)
    app.add_directive("thumb-figure", ThumbFigure)
    return {"version": __version__}
