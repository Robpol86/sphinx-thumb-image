"""Miscellaneous code."""

from dataclasses import dataclass
from typing import ClassVar, Optional


@dataclass
class ThumbRequest:
    """TODO."""

    width: Optional[int]
    height: Optional[int]

    KEY: ClassVar[str] = "thumb-request"
