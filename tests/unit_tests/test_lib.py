"""Test the "target-format" directive option."""

from sphinx_thumb_image.lib import format_replacement


def test_simple():
    """Test simple string replacement."""
    string = "https://localhost/%(three)s/%(two)s/%(one)s"
    assert format_replacement(string, "none", "0") == string
    assert format_replacement(string, "three", "3") == "https://localhost/3/%(two)s/%(one)s"
