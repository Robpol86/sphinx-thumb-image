"""Tests."""

import pytest

from sphinx_thumb_image.thumb import format_target


@pytest.mark.parametrize(
        "string_fmt,expected",
        [
            ["untouched", "untouched"],
            ["%s ignored", "%s ignored"],
            ["%(ignored)s ignored", "%(ignored)s ignored"],
            ["%(one)s not-ignored", "ONE not-ignored"],
            ["%(one)s %(two)s", "ONE TWO"],
        ],
    )
def test(string_fmt: str, expected: str):
    """Test."""
    actual = format_target(string_fmt, one="ONE", two="TWO")
    assert actual == expected
