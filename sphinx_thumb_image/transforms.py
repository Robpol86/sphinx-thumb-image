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
    for node in doctree.findall(lambda n: THUMB_REQUEST_KEY in n):
        width = node[THUMB_REQUEST_KEY]["width"]
        height = node[THUMB_REQUEST_KEY]["height"]
        # Get fullsize image size.
        image_path = node[THUMB_REQUEST_KEY]["fullsize-path"]
        with PIL.Image.open(image_path) as image:
            thumb_width, thumb_height = get_thumb_size(image.size, width, height)
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
