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
    string = "https://localhost/%(fullsize_path)s"
    assert format_replacement(string, "fullsize_path", "_images/tux.png") == "https://localhost/" + "_images/tux.png"
    pytest.skip("TODO")
    # :target: https://localhost/%(fullsize_path)s
    # :target: https://localhost/%(fullsize_path:-4:)s
    # :target: https://localhost/%(fullsize_path:7:)s
    # :target: https://localhost/%(fullsize_path::-3)s
    # :target: https://localhost/%(fullsize_path::5)s
    # :target: https://localhost/%(fullsize_path:-5:-2)s
    # :target: https://localhost/%(fullsize_path:1:5)s
    # :target: https://localhost/%(fullsize_path:-8:-1:2)s
    # :target: https://localhost/%(fullsize_path:1:8:3)s
    # :target: https://localhost/%(fullsize_path:::-1)s
    # :target: https://localhost/%(fullsize_path:)s

    # "https://localhost/" + "_images/tux.png",
    # "https://localhost/" + "_images/tux.png"[-4:],
    # "https://localhost/" + "_images/tux.png"[7:],
    # "https://localhost/" + "_images/tux.png"[:-3],
    # "https://localhost/" + "_images/tux.png"[:5],
    # "https://localhost/" + "_images/tux.png"[-5:-2],
    # "https://localhost/" + "_images/tux.png"[1:5],
    # "https://localhost/" + "_images/tux.png"[-8:-1:2],
    # "https://localhost/" + "_images/tux.png"[1:8:3],
    # "https://localhost/" + "_images/tux.png"[::-1],
