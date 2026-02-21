"""Miscellaneous code."""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Iterator, Optional

from sphinx.environment import BuildEnvironment


@dataclass
class ThumbNodeRequest:
    """Request data to be attached to an image node's attribute list.

    Designed for messages to be passed from the image directives to the resizing class.
    """

    width: Optional[int] = None
    height: Optional[int] = None
    quality: Optional[int] = None
    no_resize: bool = False
    is_animated: bool = False

    KEY: ClassVar[str] = "thumb-request"


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
            setattr(env, self.KEY, {})

    def set(self, thumb_path: Path, source_path: Path):
        """TODO."""
        getattr(self.env, self.KEY)[thumb_path] = source_path

    def pop(self, thumb_path: Path) -> Path:
        """TODO."""
        return getattr(self.env, self.KEY).pop(thumb_path)

    def items(self) -> Iterator[tuple[Path, Path]]:
        """TODO."""
        yield from getattr(self.env, self.KEY).items()


def format_replacement(target: str, key: str, replacement: str) -> str:
    """Apply special formatting to the replacement string.

    :param target: The unformatted string to operate on.
    :param key: Format key (e.g. "key" in "%(key)s").
    :param replacement: The value to replace the key formatting with.

    :return: The formatted string.
    """
    # Simple slices.
    for search, a, b, c in re.findall(rf"(%\({key}:(-?\d+):(-?\d+):(-?\d+)\)s)", target):
        target = target.replace(search, replacement[int(a) : int(b) : int(c)])
    for search, a, b in re.findall(rf"(%\({key}:(-?\d+):(-?\d+)\)s)", target):
        target = target.replace(search, replacement[int(a) : int(b)])
    for search, a in re.findall(rf"(%\({key}:(-?\d+)\)s)", target):
        target = target.replace(search, replacement[int(a)])
    # Three slice permutations.
    for search, a, b in re.findall(rf"(%\({key}::(-?\d+):(-?\d+)\)s)", target):
        target = target.replace(search, replacement[: int(a) : int(b)])
    for search, a, b in re.findall(rf"(%\({key}:(-?\d+)::(-?\d+)\)s)", target):
        target = target.replace(search, replacement[int(a) :: int(b)])
    for search, a, b in re.findall(rf"(%\({key}:(-?\d+):(-?\d+):\)s)", target):
        target = target.replace(search, replacement[int(a) : int(b) :])
    for search, a in re.findall(rf"(%\({key}:(-?\d+)::\)s)", target):
        target = target.replace(search, replacement[int(a) : :])
    for search, a in re.findall(rf"(%\({key}::(-?\d+):\)s)", target):
        target = target.replace(search, replacement[: int(a) :])
    for search, a in re.findall(rf"(%\({key}:::(-?\d+)\)s)", target):
        target = target.replace(search, replacement[:: int(a)])
    # Two slice permutations.
    for search, a in re.findall(rf"(%\({key}::(-?\d+)\)s)", target):
        target = target.replace(search, replacement[: int(a)])
    for search, a in re.findall(rf"(%\({key}:(-?\d+):\)s)", target):
        target = target.replace(search, replacement[int(a) :])
    # No slice.
    return target.replace(f"%({key})s", replacement)
