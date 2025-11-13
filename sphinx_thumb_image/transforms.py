"""TODO."""

import PIL.Image
from sphinx.addnodes import document
from sphinx.application import Sphinx
from sphinx.transforms.post_transforms import SphinxPostTransform

from sphinx_thumb_image.utils import THUMB_REQUEST_KEY, get_thumb_size


def determine_thumb_file_names(app: Sphinx, doctree: document):
    """TODO.

    PIL read image sizes, determine file names. Handle collisions.

    If quality == 100 and source <= thumb size then pop thumb-request.
    Else set thumb file name in node attr dict.

    TODO::
    * Confirm this runs only once even with -j
    """
    thumb_image_default_height = app.config["thumb_image_default_height"]
    thumb_image_default_width = app.config["thumb_image_default_width"]

    for node in doctree.findall(lambda n: THUMB_REQUEST_KEY in n):
        option_width = node[THUMB_REQUEST_KEY]["width"]
        option_height = node[THUMB_REQUEST_KEY]["height"]
        # Get fullsize image size.
        image_path = node[THUMB_REQUEST_KEY]["fullsize-path"]
        with PIL.Image.open(image_path) as image:
            thumb_width, thumb_height = get_thumb_size(
                image.size,
                option_width,
                option_height,
                thumb_image_default_width,
                thumb_image_default_height,
            )
        # TODO
        if thumb_width and thumb_height:
            pass  # TODO


class PostTransformThumbImages(SphinxPostTransform):
    """TODO.

    Just PIL resize/save. No collisions guaranteed.

    Handle rebuild without clean. If file exists noop?
    """

    default_priority = 500  # TODO make configurable

    def run(self, **kwargs):
        """TODO."""
        for node in self.document.findall(lambda n: THUMB_REQUEST_KEY in n):
            if node:
                pass  # TODO
