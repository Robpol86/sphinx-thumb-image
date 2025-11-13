"""TODO."""

from sphinx.addnodes import document
from sphinx.application import Sphinx
from sphinx.transforms.post_transforms import SphinxPostTransform

from sphinx_thumb_image.utils import THUMB_REQUEST_KEY


def determine_thumb_file_names(app: Sphinx, doctree: document):
    """TODO.

    PIL read image sizes, determine file names. Handle collisions.

    If quality == 100 and source <= thumb size then pop thumb-request.
    Else set thumb file name in node attr dict.
    """
    for node in doctree.findall(lambda n: THUMB_REQUEST_KEY in n):
        if node:
            if app:
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
