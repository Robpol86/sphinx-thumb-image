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
    option_width: Optional[int],
    option_height: Optional[int],
    config_default_width: Optional[int],
    config_default_height: Optional[int],
) -> tuple[int, int]:
    """Determine the thumbnail image's width and height.

    Return (-1, -1) if source image is too small. If with and height are specified then scale the thunbnail to fit within
    those dimensions (preserving aspect ratio).

    TODO params/returns/raises
    """
    # TODO reimplement, this was AI
    fullsize_width, fullsize_height = fullsize_size

    if option_width is not None:
        thumb_width = option_width
    elif config_default_width is not None:
        thumb_width = config_default_width
    else:
        thumb_width = None

    if option_height is not None:
        thumb_height = option_height
    elif config_default_height is not None:
        thumb_height = config_default_height
    else:
        thumb_height = None

    if thumb_width is None and thumb_height is None:
        return -1, -1  # TODO raise ValueError("At least one of width or height must be specified.")

    if thumb_width is not None and thumb_height is not None:
        scale_w = thumb_width / fullsize_width
        scale_h = thumb_height / fullsize_height
        scale = min(scale_w, scale_h)
        thumb_width = int(fullsize_width * scale)
        thumb_height = int(fullsize_height * scale)
    elif thumb_width is not None:
        scale = thumb_width / fullsize_width
        thumb_height = int(fullsize_height * scale)
    elif thumb_height is not None:
        scale = thumb_height / fullsize_height
        thumb_width = int(fullsize_width * scale)

    if fullsize_width <= thumb_width or fullsize_height <= thumb_height:
        return -1, -1

    return thumb_width, thumb_height