"""Helpers."""

from typing import Optional

THUMB_REQUEST_KEY = "thumb-request"


def format_target(fmt: str, **kv) -> str:
    """Substitutes %(key)s formatted keys with their values.

    :param fmt: Input string formatter.
    :param kv: Key-value pairs of substitutions.

    :return: The formatted string.
    """
    for key, value in kv.items():
        fmt = fmt.replace(f"%({key})s", value)
    return fmt


def get_thumb_size(
    fullsize_size: tuple[int, int],
    thumb_width: Optional[int],
    thumb_height: Optional[int],
) -> tuple[int, int]:
    """Determine the thumbnail image's width and height.

    Return (-1, -1) if source image is too small. If width and height are specified then scale the thunbnail to fit within
    those dimensions (preserving aspect ratio).

    TODO params/returns/raises
    """
    if fullsize_size and thumb_width and thumb_height:
        return -1, -1
    return 0, 0
