"""Helpers."""

from pathlib import Path
from typing import Optional

from PIL import Image

MAX_QUALITY = 100


def format_target(fmt: str, **kv) -> str:
    """Substitutes %(key)s formatted keys with their values.

    :param fmt: Input string formatter.
    :param kv: Key-value pairs of substitutions.

    :return: The formatted string.
    """
    for key, value in kv.items():
        fmt = fmt.replace(f"%({key})s", value)
    return fmt


def get_new_dimensions(original_w_h, max_w_h) -> tuple[int, int]:
    """Return the scaled down size of the image, to be the thumbnail size.

    :param original_w_h: Tuple of (width, height) of the original image.
    :param max_w_h: Tuple of (max width, max height) for the thumbnail.

    :return: Tuple of (new width, new height) or (-1, -1) if no resizing needed.
    """
    original_w, original_h = original_w_h
    max_w, max_h = max_w_h

    if original_w <= max_w and original_h <= max_h:
        return -1, -1  # No resizing needed.

    aspect_ratio = original_w / original_h
    if original_w < max_w:
        pass
    return aspect_ratio  # TODO


def create_thumbnail(
    source_original_image: Path,
    target_thumb_image: Path,
    width: Optional[int] = None,
    height: Optional[int] = None,
    quality: int = MAX_QUALITY,
    **kwargs,
) -> bool:
    """TODO.

    Caller handles lock and target path determination.

    # TODO param resample, param reducing_gap

    :return: If the thumbnail was created.
    """
    if width is None and height is None:
        raise ValueError("At least one of width or height must be specified.")

    with Image.open(source_original_image) as image:
        # If keeping full quality and source image is smaller than or equal to target size then don't create a thumbnail.
        if quality == MAX_QUALITY:
            if (width is not None and height is not None) and image.width <= width and image.height <= height:
                return False
            elif width is not None and image.width <= width:
                return False
            elif height is not None and image.height <= height:
                return False
        # Determine new size (dimensions).
        if width is None:
            width = int(height * (image.width / image.height))
        elif height is None:
            height = int(width * (image.width / image.height))
        size = (width, height)
        # Resize and save.
        image.thumbnail(size, **kwargs)
        image.save(target_thumb_image)

    return True
