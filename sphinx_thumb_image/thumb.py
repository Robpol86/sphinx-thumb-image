"""Sphinx extension that resizes images into thumbnails on the fly.

https://sphinx-thumb-image.readthedocs.io
https://github.com/Robpol86/sphinx-thumb-image
https://pypi.org/project/sphinx-thumb-image

TODO::
* Support pdf and non-html builders
* If source image <= thumb size: still compress, unless 100% then noop and link to fullsize
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
    * /_images/dog.jpg -> /_images/dog.th700.jpg [quality collision: dog.th700.2.jpg]
    * /posts/2025-11-23/cat.jpg -> /posts/2025-11-23/cat.th700.jpg
* Space saving: don't write fullsize image to _build if not referenced
* config and option for resample algorithm (nearest, bilinear, bicubic, lanczos)
* Handle smaller than thumb images.
"""

from pathlib import Path

from docutils.nodes import Element
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.images import Figure, Image
from sphinx.application import Sphinx

from sphinx_thumb_image import __version__
from sphinx_thumb_image.utils import format_target


class ThumbCommon(Image):
    """Common methods for both thumb image/figure subclassed directives."""

    __option_spec = {}
    # Target options.
    __option_spec["no-target"] = directives.flag
    __option_spec["target-fullsize"] = directives.flag
    __option_spec["target-thumb"] = directives.flag
    # Thumb options.
    __option_spec["thumb-width"] = directives.nonnegative_int  # TODO better validator? Use same as Figur?
    __option_spec["thumb-height"] = directives.nonnegative_int
    __option_spec["thumb-quality"] = directives.percentage
    __option_spec["thumb-file-ext"] = directives.unchanged
    __option_spec["thumb-format"] = directives.unchanged


    def __update_target(self):
        """Update the image's link target."""
        # Handle options specified in the directive first.
        img_src = self.arguments[0]
        format_kv = {
            "fullsize": img_src,
            "basename": Path(img_src).name,
            "path": self.state.document.settings.env.relfn2path(img_src)[0],
        }
        if "no-target" in self.options:
            self.options.pop("target", None)
        elif "target-fullsize" in self.options:
            self.options["target"] = img_src
        elif "target-thumb" in self.options:
            raise NotImplementedError("TOOD get thumb path")
        elif "target" in self.options:
            self.options["target"] = format_target(self.options["target"], **format_kv)
        else:
            # Apply defaults from conf.py.
            config = self.state.document.settings.env.config
            thumb_image_default_target = config["thumb_image_default_target"]
            if thumb_image_default_target == "fullsize":
                self.options["target"] = img_src
            elif thumb_image_default_target == "thumb":
                raise NotImplementedError("TOOD get thumb path")
            elif thumb_image_default_target is None:
                self.options.pop("target", None)
            else:
                self.options["target"] = format_target(thumb_image_default_target, **format_kv)


class ThumbImage(ThumbCommon):
    """Thumbnail image directive."""

    option_spec = Image.option_spec | ThumbCommon._ThumbCommon__option_spec

    def run(self) -> list[Element]:
        """Entrypoint."""
        self._ThumbCommon__update_target()
        return super().run()


class ThumbFigure(Figure, ThumbCommon):
    """Thumbnail figure directive."""

    option_spec = Figure.option_spec | ThumbCommon._ThumbCommon__option_spec

    def run(self) -> list[Element]:
        """Entrypoint."""
        self._ThumbCommon__update_target()
        return super().run()


def setup(app: Sphinx) -> dict[str, str]:
    """Register extension components with Sphinx (called by Sphinx during phase 0 [initialization]).

    :param app: Sphinx application object.

    :returns: Extension version.
    """
    app.add_config_value("thumb_image_default_ext", "jpg", "html")
    app.add_config_value("thumb_image_default_format", None, "html")
    app.add_config_value("thumb_image_default_height", None, "html")
    app.add_config_value("thumb_image_default_quality", 100, "html")
    app.add_config_value("thumb_image_default_target", "fullsize", "html")
    app.add_config_value("thumb_image_default_width", None, "html")
    app.add_directive("thumb-image", ThumbImage)
    app.add_directive("thumb-figure", ThumbFigure)
    return {
        "parallel_read_safe": False,  # TODO
        "parallel_write_safe": False,  # TODO
        "version": __version__,
    }
