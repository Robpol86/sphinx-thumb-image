"""Helpers."""

import PIL.Image

PREFIX = "sti-"


def format_target(fmt: str, **kv) -> str:
    """Substitutes %(key)s formatted keys with their values.

    :param fmt: Input string formatter.
    :param kv: Key-value pairs of substitutions.

    :return: The formatted string.
    """
    for key, value in kv.items():
        fmt = fmt.replace(f"%({key})s", value)
    return fmt


def get_image_size(image_path: str) -> tuple[int, int]:
    """Return the width and height of an image."""
    with PIL.Image.open(image_path) as image:
        return image.size
