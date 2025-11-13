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
    fullsize_width: int,
    fullsize_height: int,
    option_width: Optional[int],
    option_height: Optional[int],
    config_default_width: Optional[int],
    config_default_height: Optional[int],
):
    """TODO.

    Return -1,-1 if source image is too small.
    """
    if not any([option_width, option_height, config_default_width, config_default_height]):
        raise ValueError("At least one of width or height must be specified in option or config.")
    if fullsize_width and fullsize_height:
        return 0, 0  # TODO
    return -1, -1  # TODO
