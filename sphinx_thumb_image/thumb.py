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
* Quality only set globally in conf.py. Not in directive options.
* Thumb filename:
    * image.jpg -> image-700x435-95pct.jpg (NO)
    * image.gif -> image-700x435.gif
* Space saving: don't write original image to _build if not referenced
* config and option for resample algorithm (nearest, bilinear, bicubic, lanczos)
* Should bmp file thumbs be bmp or jpg? Support apng? svg?
* What if source image is smaller than thumb size? What about quality == and != 100%?
* Support px unit suffix
"""

from pathlib import Path

from docutils.nodes import Element
from docutils.nodes import image as ImageNode  # noqa: N812
from docutils.parsers.rst.directives import flag, nonnegative_int
from docutils.parsers.rst.directives.images import Figure, Image
from sphinx.application import Sphinx

from sphinx_thumb_image import __version__
from sphinx_thumb_image.transforms import PostTransformThumbImages
from sphinx_thumb_image.utils import format_target, get_image_size, Keys


class ThumbCommon(Image):
    """Common methods for both thumb image/figure subclassed directives."""

    __option_spec = {}
    # Target options.
    __option_spec["no-target"] = flag
    __option_spec["target-original"] = flag
    __option_spec["target-thumb"] = flag
    # Dimension options.
    __option_spec["thumb-width"] = nonnegative_int
    __option_spec["thumb-height"] = nonnegative_int

    def __update_target(self):
        """Update the image's link target."""
        # Handle options specified in the directive first.
        img_src = self.arguments[0]
        format_kv = {
            "original": img_src,  # TODO s/original/fullsize/
            "basename": Path(img_src).name,
            "path": self.state.document.settings.env.relfn2path(img_src)[0],
        }
        if "no-target" in self.options:
            self.options.pop("target", None)
        elif "target-original" in self.options:
            self.options["target"] = img_src
        elif "target-thumb" in self.options:
            raise NotImplementedError("TOOD get thumb path")
        elif "target" in self.options:
            self.options["target"] = format_target(self.options["target"], **format_kv)
        else:
            # Apply defaults from conf.py.
            config = self.state.document.settings.env.config
            thumb_image_default_target = config["thumb_image_default_target"]
            if thumb_image_default_target == "original":
                self.options["target"] = img_src
            elif thumb_image_default_target == "thumb":
                raise NotImplementedError("TOOD get thumb path")
            elif thumb_image_default_target is None:
                self.options.pop("target", None)
            else:
                self.options["target"] = format_target(thumb_image_default_target, **format_kv)

    def __mark_image_nodes(self, nodes: list[Element]):
        """TODO."""
        config = self.state.document.settings.env.config
        thumb_image_default_width = config["thumb_image_default_width"]
        thumb_image_default_height = config["thumb_image_default_height"]
        fixed_size_in_options = "thumb-width" in self.options and "thumb-height" in self.options
        fixed_size_in_config = thumb_image_default_width is not None and thumb_image_default_height is not None
        one_size_in_options = "thumb-width" in self.options or "thumb-height" in self.options
        one_size_in_config = thumb_image_default_width is not None or thumb_image_default_height is not None
        if not one_size_in_options and not one_size_in_config:
            raise ValueError("TODO No thumb size specified in options or config.")
        for node in nodes:
            for image_node in node.findall(ImageNode):
                if fixed_size_in_options:
                    # User specifying custom thumb size, no need to worry about aspect ratio or original size.
                    image_node["set-thumb-width"] = int(self.options["thumb-width"])
                    image_node["set-thumb-height"] = int(self.options["thumb-height"])
                elif not one_size_in_options and fixed_size_in_config:
                    # No size in options, but both sizes in config.
                    image_node["set-thumb-width"] = int(thumb_image_default_width)
                    image_node["set-thumb-height"] = int(thumb_image_default_height)
                else:
                    


                elif ("thumb-width" not in self.options and "thumb-height" not in self.options) and :
                    pass  # TODO
                elif "thumb-width" in self.options or "thumb-height" in self.options:
                    pass  # TODO
                elif thumb_image_default_width is not None and thumb_image_default_height is not None:
                    pass  # TODO
                elif thumb_image_default_width is not None or thumb_image_default_height is not None:
                    pass
                else:
                    raise ValueError("TODO No thumb size specified in options or config.")

                image_path = self.state.document.settings.env.relfn2path(image_node["uri"])[1]
                width, height = get_image_size(image_path)

                image_node[f"{PREFIX}original-width"] = width
                # TODO if quality/size satisfies: _image_node["make-thumb"] = True
                image_node[f"{PREFIX}make-thumb"] = True
                # TODO image_node[thumb-uri] = _images/image-thumb
                # TODO option/conf default thumb fname: "{fileSansExt}..."


class ThumbImage(ThumbCommon):
    """Thumbnail image directive."""

    option_spec = Image.option_spec | ThumbCommon._ThumbCommon__option_spec

    def run(self) -> list[Element]:
        """Entrypoint."""
        self._ThumbCommon__update_target()
        nodes = super().run()
        self._ThumbCommon__mark_image_nodes(nodes)
        return nodes


class ThumbFigure(Figure, ThumbCommon):
    """Thumbnail figure directive."""

    option_spec = Figure.option_spec | ThumbCommon._ThumbCommon__option_spec

    def run(self) -> list[Element]:
        """Entrypoint."""
        self._ThumbCommon__update_target()
        nodes = super().run()
        self._ThumbCommon__mark_image_nodes(nodes)
        return nodes


def setup(app: Sphinx) -> dict[str, str]:
    """Register extension components with Sphinx (called by Sphinx during phase 0 [initialization]).

    :param app: Sphinx application object.

    :returns: Extension version.
    """
    app.add_config_value("thumb_image_default_target", "original", "html")
    app.add_config_value("thumb_image_default_width", None, "html")
    app.add_config_value("thumb_image_default_height", None, "html")
    app.add_directive("thumb-image", ThumbImage)
    app.add_directive("thumb-figure", ThumbFigure)
    app.add_post_transform(PostTransformThumbImages)
    return {
        "parallel_read_safe": False,  # TODO
        "parallel_write_safe": False,  # TODO
        "version": __version__,
    }
