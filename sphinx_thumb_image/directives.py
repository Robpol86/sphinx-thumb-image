"""Sphinx directives.

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

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.images import Figure, Image

from sphinx_thumb_image.lib import ThumbNodeRequest


class ThumbCommon(Image):
    """Common methods for both thumb image/figure subclassed directives."""

    __option_spec = {}
    __option_spec["resize-width"] = lambda arg: directives.nonnegative_int(arg.replace("px", ""))
    __option_spec["resize-height"] = __option_spec["resize-width"]

    def __add_request(self, sphinx_nodes: list[nodes.Element]) -> list[nodes.Element]:
        """Build and add a ThumbRequest to the image node.

        :param sphinx_nodes: List of nodes returned by super().run(), one of which contains an image node to be modified.

        :return: The same node list as the input with an annotated image node.
        """
        config = self.state.document.settings.env.config

        # Read width/height from directive options first.
        if "resize-width" in self.options or "resize-height" in self.options:
            request = ThumbNodeRequest(
                width=self.options.get("resize-width", None),
                height=self.options.get("resize-height", None),
            )
        else:
            # Read width/height from Sphinx config.
            thumb_image_resize_width = config["thumb_image_resize_width"]
            thumb_image_resize_height = config["thumb_image_resize_height"]
            if thumb_image_resize_width is not None or thumb_image_resize_height is not None:
                request = ThumbNodeRequest(
                    width=thumb_image_resize_width,
                    height=thumb_image_resize_height,
                )
            else:
                # User has not provided the width/height.
                raise self.error('Error in %r directive: "resize-width" option is missing.' % self.name)

        # Add request to the node.
        for node in sphinx_nodes:
            for image_node in node.findall(nodes.image):
                image_node[request.KEY] = request

        return sphinx_nodes


class ThumbImage(ThumbCommon):
    """Thumbnail image directive."""

    option_spec = Image.option_spec | ThumbCommon._ThumbCommon__option_spec

    def run(self) -> list[nodes.Element]:
        """Entrypoint."""
        return self._ThumbCommon__add_request(super().run())


class ThumbFigure(Figure, ThumbCommon):
    """Thumbnail figure directive."""

    option_spec = Figure.option_spec | ThumbCommon._ThumbCommon__option_spec

    def run(self) -> list[nodes.Element]:
        """Entrypoint."""
        return self._ThumbCommon__add_request(super().run())
