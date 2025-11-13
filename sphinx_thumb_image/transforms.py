"""TODO."""

from sphinx.transforms.post_transforms import SphinxPostTransform

from sphinx_thumb_image.utils import THUMB_REQUEST_KEY


class PostTransformThumbImages(SphinxPostTransform):
    """TODO."""

    default_priority = 500  # TODO make configurable

    def run(self, **kwargs):
        """TODO."""
        for node in self.document.findall(lambda n: THUMB_REQUEST_KEY in n):
            if node:
                pass  # TODO
