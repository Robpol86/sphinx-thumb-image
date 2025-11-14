"""Tests."""

from typing import Optional

import pytest

from sphinx_thumb_image.utils import get_thumb_size

TYPE_SIZE = tuple[int, int]
TYPE_SIZE_OPTIONAL = tuple[Optional[int], Optional[int]]


@pytest.mark.parametrize(
    "fullsize_size,option_size,config_size,expected",
    [
        [(200, 100), (100, None), (None, None), (100, 50)],
    ],
)
def test(fullsize_size: TYPE_SIZE, option_size: TYPE_SIZE_OPTIONAL, config_size: TYPE_SIZE_OPTIONAL, expected: TYPE_SIZE):
    """Test."""
    pytest.skip("TODO")
    actual = get_thumb_size(fullsize_size, *option_size, *config_size)
    assert actual == expected
