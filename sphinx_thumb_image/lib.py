"""Miscellaneous code."""

from dataclasses import dataclass
from typing import ClassVar, Optional


@dataclass
class ThumbNodeRequest:
    """Request data to be attached to an image node's attribute list.

    Designed for messages to be passed from the image directives to the resizing class.
    """

    width: Optional[int] = None
    height: Optional[int] = None
    no_resize: Optional[bool] = None

    KEY: ClassVar[str] = "thumb-request"


def format_replacement(string: str, key: str, replacement: str) -> str:
    """TODO."""
    return string.replace(f"%({key})s", replacement)
