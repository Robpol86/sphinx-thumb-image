"""TODO."""

from sphinx.transforms.post_transforms import SphinxPostTransform


class PostTransformThumbImages(SphinxPostTransform):
    """TODO."""

    default_priority = 500  # TODO make configurable

    def run(self, **kwargs):
        """TODO."""
        for node in self.document.findall(lambda n: "thumb-request" in n):
            if node:
                pass  # TODO
