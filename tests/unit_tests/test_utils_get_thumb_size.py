"""Tests."""

from typing import Optional

import pytest

from sphinx_thumb_image.utils import get_thumb_size

TYPE_SIZE = tuple[int, int]
TYPE_SIZE_OPT = tuple[Optional[int], Optional[int]]


@pytest.mark.parametrize(
    "fullsize_size,option_size,config_size,expected",
    [
        # Only one specified at a time.
        [(200, 100), (100, None), (None, None), (100, 50)],
        [(200, 100), (None, 50), (None, None), (100, 50)],
        [(200, 100), (None, None), (100, None), (100, 50)],
        [(200, 100), (None, None), (None, 50), (100, 50)],

        # Both options specified.
        [(200, 100), (100, 50), (None, None), (100, 50)],
        [(200, 100), (100, 25), (None, None), (50, 25)],
        [(200, 100), (50, 50), (None, None), (50, 25)],
        [(200, 100), (None, None), (100, 50), (100, 50)],
        [(200, 100), (None, None), (100, 25), (50, 25)],
        [(200, 100), (None, None), (50, 50), (50, 25)],

        # Config fallback.
        [(400, 200), (200, None), (50, 50), (200, 100)],
        [(400, 200), (None, 100), (50, 50), (200, 100)],
        [(400, 200), (None, None), (50, 50), (50, 25)],

        # Too small.
        [(200, 100), (999, None), (None, None), (-1, -1)],
        [(200, 100), (200, None), (None, None), (-1, -1)],
        [(200, 100), (None, None), (999, None), (-1, -1)],
        [(200, 100), (None, None), (200, None), (-1, -1)],

        # Round down.
        [(200, 100), (25, None), (None, None), (25, 12)],

        # No options.
        [(200, 100), (None, None), (None, None), (None, None)],
    ],
)
def test(fullsize_size: TYPE_SIZE, option_size: TYPE_SIZE_OPT, config_size: TYPE_SIZE_OPT, expected: TYPE_SIZE_OPT):
    """Test."""
    pytest.skip("TODO")
    if expected[0] is None:
        with pytest.raises(ValueError):
            get_thumb_size(fullsize_size, *option_size, *config_size)
        return

    actual = get_thumb_size(fullsize_size, *option_size, *config_size)
    assert actual == expected
