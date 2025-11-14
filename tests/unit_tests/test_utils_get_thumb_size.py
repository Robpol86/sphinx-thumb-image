"""Tests."""

from typing import Optional

import pytest

from sphinx_thumb_image.utils import get_thumb_size

TYPE_SIZE = tuple[int, int]
TYPE_SIZE_OPT = tuple[Optional[int], Optional[int]]


@pytest.mark.parametrize(
    "fullsize_size,thumb_width,thumb_height,expected",
    [
        # # Only one specified at a time.
        # [(200, 100), (100, None), (None, None), (100, 50)],
        # [(200, 100), (None, 50), (None, None), (100, 50)],
        # [(200, 100), (None, None), (100, None), (100, 50)],
        # [(200, 100), (None, None), (None, 50), (100, 50)],
        # # Both options specified.
        # [(200, 100), (100, 50), (None, None), (100, 50)],
        # [(200, 100), (100, 25), (None, None), (50, 25)],
        # [(200, 100), (50, 50), (None, None), (50, 25)],
        # [(200, 100), (None, None), (100, 50), (100, 50)],
        # [(200, 100), (None, None), (100, 25), (50, 25)],
        # [(200, 100), (None, None), (50, 50), (50, 25)],
        # # Config fallback.
        # [(400, 200), (200, None), (50, 50), (200, 100)],
        # [(400, 200), (None, 100), (50, 50), (200, 100)],
        # [(400, 200), (None, None), (50, 50), (50, 25)],
        # # Too small.
        # [(200, 100), (999, None), (None, None), (-1, -1)],
        # [(200, 100), (200, None), (None, None), (-1, -1)],
        # [(200, 100), (None, None), (999, None), (-1, -1)],
        # [(200, 100), (None, None), (200, None), (-1, -1)],
        # # Round down.
        # [(200, 100), (25, None), (None, None), (25, 12)],
        # # No options.
        # [(200, 100), (None, None), (None, None), (None, None)],
    ],
)
def test(fullsize_size: TYPE_SIZE, thumb_width: Optional[int], thumb_height: Optional[int], expected: TYPE_SIZE):
    """Test."""
    # TODO
    expected_w = expected[0]
    expected_h = expected[1]
    if expected_w is None:
        pytest.skip("TODO")
        with pytest.raises(ValueError):
            get_thumb_size(fullsize_size, *option_size, *config_size)
        return

    pytest.skip("TODO")
    actual_w, actual_h = get_thumb_size(fullsize_size, *option_size, *config_size)
    assert actual_w == expected_w
    assert actual_h == expected_h

    expected_w_i = expected[1]
    expected_h_i = expected[0]
    actual_w_i, actual_h_i = get_thumb_size(
        (fullsize_size[1], fullsize_size[0]),
        *(option_size[1], option_size[0]),
        *(config_size[1], config_size[0]),
    )
    assert actual_w_i == expected_w_i
    assert actual_h_i == expected_h_i
