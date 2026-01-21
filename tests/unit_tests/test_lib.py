"""Test the "target-format" directive option."""

import pytest

from sphinx_thumb_image.lib import format_replacement


def test_simple():
    """Test simple string replacement."""
    string = "https://localhost/%(three)s/%(two)s/%(one)s"
    assert format_replacement(string, "none", "0") == string
    assert format_replacement(string, "three", "3") == "https://localhost/3/%(two)s/%(one)s"


def test_slicing():
    """Test string slicing."""
    def go(target: str, expected: str = None):
        if expected is None:
            expected = target
        actual = format_replacement(target, "fullsize_path", "_images/tux.png")
        assert actual == expected
    go("https://localhost/%(fullsize_path)s", "https://localhost/" + "_images/tux.png")
    pytest.skip("TODO")
    go("https://localhost/%(fullsize_path:-4:)s", "https://localhost/" + "_images/tux.png"[-4:])
    go("https://localhost/%(fullsize_path:7:)s", "https://localhost/" + "_images/tux.png"[7:])
    go("https://localhost/%(fullsize_path::-3)s", "https://localhost/" + "_images/tux.png"[:-3])
    go("https://localhost/%(fullsize_path::5)s", "https://localhost/" + "_images/tux.png"[:5])
    go("https://localhost/%(fullsize_path:-5:-2)s", "https://localhost/" + "_images/tux.png"[-5:-2])
    go("https://localhost/%(fullsize_path:1:5)s", "https://localhost/" + "_images/tux.png"[1:5])
    go("https://localhost/%(fullsize_path:-8:-1:2)s", "https://localhost/" + "_images/tux.png"[-8:-1:2])
    go("https://localhost/%(fullsize_path:1:8:3)s", "https://localhost/" + "_images/tux.png"[1:8:3])
    go("https://localhost/%(fullsize_path:::-1)s", "https://localhost/" + "_images/tux.png"[::-1])
    go("https://localhost/%(fullsize_path:)s")  # No-op, same as input.
