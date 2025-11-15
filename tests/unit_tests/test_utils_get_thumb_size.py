"""Tests."""

from typing import Optional

import pytest

from sphinx_thumb_image.utils import get_thumb_size

TYPE_SIZE = tuple[int, int]
TYPE_SIZE_OPT = tuple[Optional[int], Optional[int]]


@pytest.mark.parametrize(
    "fullsize_size,thumb_width,thumb_height,expected",
    [
        # Only one dimension specified at a time.
        [(200, 100), 100, None, (100, 50)],
        [(200, 100), None, 50, (100, 50)],
        # Both dimensions specified.
        [(200, 100), 100, 50, (100, 50)],
        [(200, 100), 100, 25, (50, 25)],
        [(200, 100), 50, 50, (50, 25)],
        # Too small.
        [(200, 100), 999, None, (-1, -1)],
        [(200, 100), None, 200, (-1, -1)],
        [(200, 100), 200, 100, (-1, -1)],
        # Round down.
        [(200, 100), 25, None, (25, 12)],
        # Neither.
        [(200, 100), None, None, (None, None)],
    ],
)
def test(fullsize_size: TYPE_SIZE, thumb_width: Optional[int], thumb_height: Optional[int], expected: TYPE_SIZE_OPT):
    """Test."""
    expected_w = expected[0]
    expected_h = expected[1]
    if expected_w is None:
        with pytest.raises(ValueError):
            get_thumb_size(fullsize_size, thumb_width, thumb_height)
        return

    pytest.skip("TODO")
    actual_w, actual_h = get_thumb_size(fullsize_size, thumb_width, thumb_height)
    assert actual_w == expected_w
    assert actual_h == expected_h

    fullsize_size_i = (fullsize_size[1], fullsize_size[0])
    expected_w_i = expected[1]
    expected_h_i = expected[0]
    actual_w_i, actual_h_i = get_thumb_size(fullsize_size_i, thumb_height, thumb_width)
    assert actual_w_i == expected_w_i
    assert actual_h_i == expected_h_i
