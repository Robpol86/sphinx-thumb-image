"""Tests."""

import pytest

from sphinx_thumb_image.utils import get_new_dimensions


@pytest.mark.parametrize(
    "original_w_h,max_w_h,expected",
    [
        # Original larger than max.
        [(400, 200), (100, 100), (100, 50)],
        [(200, 400), (100, 100), (50, 100)],
        [(400, 200), (300, 300), (300, 150)],
        [(200, 400), (300, 300), (150, 300)],
        # Original smaller than or equal to max.
        [(100, 100), (200, 200), (-1, -1)],
        [(200, 200), (200, 200), (-1, -1)],
    ],
)
def test(original_w_h: tuple[int, int], max_w_h: tuple[int, int], expected: tuple[int, int]):
    """Test."""
    pytest.skip("TODO")
    actual = get_new_dimensions(original_w_h, max_w_h)
    assert actual == expected
