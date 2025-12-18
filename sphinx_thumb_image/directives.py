"""TODO.

TODO::
* Support pdf and non-html builders such as pdf, epub, etc.
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
* Investigate transformer approach. Can all thumb file paths be determined before multiprocessed resampling?
"""

from docutils.nodes import Element
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.images import Figure, Image


class ThumbCommon(Image):
    """Common methods for both thumb image/figure subclassed directives."""

    __option_spec = {}
    __option_spec["scale-width"] = directives.nonnegative_int  # TODO better validator? Use same as Figur?
    __option_spec["scale-height"] = directives.nonnegative_int

    def __get_scale_size(self):
        """TODO."""
        config = self.state.document.settings.env.config
        thumb_image_scale_width = config["thumb_image_scale_width"]
        thumb_image_scale_height = config["thumb_image_scale_height"]

        if "scale-width" not in self.options and "scale-height" not in self.options:
            # No dimensions specified in directive as options. Checking config for defaults.
            if thumb_image_scale_width is None and thumb_image_scale_height is None:
                raise ValueError("Missing option 'scale-width'")

        # TODO return


class ThumbImage(ThumbCommon):
    """Thumbnail image directive."""

    option_spec = Image.option_spec | ThumbCommon._ThumbCommon__option_spec

    def run(self) -> list[Element]:
        """Entrypoint."""
        self._ThumbCommon__get_scale_size()
        return super().run()


class ThumbFigure(Figure, ThumbCommon):
    """Thumbnail figure directive."""

    option_spec = Figure.option_spec | ThumbCommon._ThumbCommon__option_spec

    def run(self) -> list[Element]:
        """Entrypoint."""
        self._ThumbCommon__get_scale_size()
        return super().run()
