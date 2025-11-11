"""Sphinx extension that resizes images into thumbnails on the fly.

https://sphinx-thumb-image.readthedocs.io
https://github.com/Robpol86/sphinx-thumb-image
https://pypi.org/project/sphinx-thumb-image

TODO::
* Support pdf and non-html builders
* If source image <= thumb size: still compress, unless 100% then noop and link to original
* Support parallel resizing, use lock files (one image may be referenced by multiple pages)
* thumb-image directive
    * Default scales down to default width
    * :thumb_width: 700px (unitless == px, no other units supported)
* config option to thumbisize all images/figures (sphinx directives)
    * No new directive options for ..image/..figure
* Remote/linked images unsupported
* Supported image formats: jpg png bmp gif gif[animated] apng svg webp
* Overridable option for thumb jpeg compression (e.g. 0-100 numerical?)
* Thumb filename:
    * image.jpg -> image-700x435-95pct.jpg
    * image.gif -> image-700x435.gif
* Space saving: don't write original image to _build if not referenced
* config and option for resample algorithm (nearest, bilinear, bicubic, lanczos)
"""

from pathlib import Path

from docutils.nodes import Element
from docutils.parsers.rst.directives import flag, images
from sphinx.application import Sphinx

from sphinx_thumb_image import __version__
from sphinx_thumb_image.utils import format_target


class ThumbCommon(images.Image):
    """Common methods for both thumb image/figure subclassed directives."""

    __option_spec = {}
    # Target options.
    __option_spec["no-target"] = flag
    __option_spec["target-original"] = flag

    def __update_target(self):
        """Update the image's link target."""
        # Handle options specified in the directive first.
        img_src = self.arguments[0]
        format_kv = {
            "original": img_src,
            "basename": Path(img_src).name,
            "path": self.state.document.settings.env.relfn2path(img_src)[0],
        }
        if "no-target" in self.options:
            self.options.pop("target", None)
        elif "target-original" in self.options:
            self.options["target"] = img_src
        elif "target" in self.options:
            self.options["target"] = format_target(self.options["target"], **format_kv)
        else:
            # Apply defaults from conf.py.
            config = self.state.document.settings.env.config
            thumb_image_default_target = config["thumb_image_default_target"]
            if thumb_image_default_target == "original":
                self.options["target"] = img_src
            elif thumb_image_default_target is None:
                self.options.pop("target", None)
            else:
                self.options["target"] = format_target(thumb_image_default_target, **format_kv)


class ThumbImage(ThumbCommon):
    """Thumbnail image directive."""

    option_spec = images.Image.option_spec | ThumbCommon._ThumbCommon__option_spec

    def run(self) -> list[Element]:
        """Entrypoint."""
        self._ThumbCommon__update_target()
        return super().run()


class ThumbFigure(images.Figure, ThumbCommon):
    """Thumbnail figure directive."""

    option_spec = images.Figure.option_spec | ThumbCommon._ThumbCommon__option_spec

    def run(self) -> list[Element]:
        """Entrypoint."""
        self._ThumbCommon__update_target()
        return super().run()


def setup(app: Sphinx) -> dict[str, str]:
    """Register extension components with Sphinx (called by Sphinx during phase 0 [initialization]).

    :param app: Sphinx application object.

    :returns: Extension version.
    """
    app.add_config_value("thumb_image_default_target", "original", "html")
    app.add_directive("thumb-image", ThumbImage)
    app.add_directive("thumb-figure", ThumbFigure)
    return {
        "parallel_read_safe": False,  # TODO
        "parallel_write_safe": False,  # TODO
        "version": __version__,
    }
