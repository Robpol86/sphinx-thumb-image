"""Sphinx extension that resizes images into thumbnails on the fly.

https://sphinx-thumb-image.readthedocs.io
https://github.com/Robpol86/sphinx-thumb-image
https://pypi.org/project/sphinx-thumb-image

TODO::
* Support pdf and non-html builders
* If source image <= thumb size: still compress, unless 100% then noop and link to original
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
* Overridable option for thumb jpeg compression (e.g. 0-100 numerical?)
* Thumb file type (jpg, png, gif)
* Support animated gif thumbnails
* Thumb filename:
    * image.jpg -> image-700x435-95pct.jpg
    * image.gif -> image-700x435.gif
* Space saving: don't write original image to _build if not referenced
"""

from typing import Dict, List

from docutils.nodes import Element
from docutils.parsers.rst.directives import flag, images
from sphinx.application import Sphinx

from sphinx_thumb_image import __version__


class ThumbCommon(images.Image):
    """Common methods for both thumb image/figure subclassed directives."""

    def __update_target(self):
        """Update the image's link target."""
        # Handle options specified in the directive first.
        img_src = self.arguments[0]
        if "no-target" in self.options:
            self.options.pop("target", None)
            return
        if "target-original" in self.options:
            self.options["target"] = img_src
            return
        if "target" in self.options:
            # TODO self.options["target"] %= {"path": "path/todo.jpg", "filename": "todo.jpg"}
            return
        # Apply defaults from conf.py.
        config = self.state.document.settings.env.config
        if "thumb_image_default_target" not in config:
            return
        thumb_image_default_target = config["thumb_image_default_target"]
        if thumb_image_default_target == "original":
            self.options["target"] = img_src
        elif thumb_image_default_target is None:
            self.options.pop("target", None)
        # else:
        # TODO self.options["target"] = thumb_image_default_target % {"path": "path/todo.jpg", "filename": "todo.jpg"}


class ThumbImage(ThumbCommon):
    """Thumbnail image directive."""

    option_spec = images.Image.option_spec.copy()
    option_spec["no-target"] = flag
    option_spec["target-original"] = flag

    def run(self) -> List[Element]:
        """Entrypoint."""
        self._ThumbCommon__update_target()
        return super().run()


class ThumbFigure(images.Figure, ThumbCommon):
    """Thumbnail figure directive."""

    option_spec = images.Figure.option_spec.copy()
    option_spec["no-target"] = flag
    option_spec["target-original"] = flag

    def run(self) -> List[Element]:
        """Entrypoint."""
        self._ThumbCommon__update_target()
        return super().run()


def setup(app: Sphinx) -> Dict[str, str]:
    """Register extension components with Sphinx (called by Sphinx during phase 0 [initialization]).

    :param app: Sphinx application object.

    :returns: Extension version.
    """
    app.add_config_value("thumb_image_default_target", "original", "env", ["original", None, str])
    app.add_directive("thumb-image", ThumbImage)
    app.add_directive("thumb-figure", ThumbFigure)
    return {"version": __version__}
