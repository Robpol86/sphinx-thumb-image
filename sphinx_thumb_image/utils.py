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
