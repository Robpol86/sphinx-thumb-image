"""TODO."""

from sphinx.transforms.post_transforms import SphinxPostTransform


class PostTransformThumbImages(SphinxPostTransform):
    """TODO."""

    default_priority = 500  # TODO make configurable

    def run(self, **kwargs):
        """TODO."""
        # import pdb; pdb.set_trace()  # TODO remove
        # TODO if make-thumb
