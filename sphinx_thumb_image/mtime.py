"""TODO."""

import os
from pathlib import Path
from typing import Iterator

from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment


class ThumbBackReference:
    """TODO.

    Rewrite matching implementation signatures.
    """

    KEY = "thumb_image_back_ref"

    def __init__(self, env: BuildEnvironment):
        """Initialize the class.

        :param env: Sphinx build environment.
        """
        self.env = env
        if not hasattr(env, self.KEY):
            # TODO confirm this persist in cache
            setattr(env, self.KEY, {})

    def set(self, thumb_path: Path, source_path: Path):
        """TODO."""
        getattr(self.env, self.KEY)[thumb_path] = source_path

    def pop(self, thumb_path: Path) -> Path:
        """TODO."""
        return getattr(self.env, self.KEY).pop(thumb_path)

    def items(self) -> Iterator[tuple[Path, Path]]:
        """TODO."""
        yield from list(getattr(self.env, self.KEY).items())


def prune_outdated_thumbs(app: Sphinx):
    """TODO.

    TODO New config option to ignore mtime to noop this.

    TODO log
    """
    back_ref = ThumbBackReference(app.env)
    for thumb_path, source_path in back_ref.items():
        prune = False
        try:
            thumb_stat = thumb_path.stat()
        except IOError:
            back_ref.pop(thumb_path)
        try:
            source_stat = source_path.stat()
        except IOError:
            prune = True
        if thumb_stat.st_mtime_ns != source_stat.st_mtime_ns:
            prune = True
        if prune:
            os.unlink(thumb_path)  # TODO Sphinx has api for this?
            back_ref.pop(thumb_path)
