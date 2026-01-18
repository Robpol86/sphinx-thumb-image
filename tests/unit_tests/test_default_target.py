"""Test the "thumb_image_default_target" Sphinx config."""

from textwrap import dedent

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp


def write_build_read(app: SphinxTestApp, index_rst_contents: str) -> list[str]:
    """Overwrite index.rst and build the index.html.

    :param app: Sphinx test app.
    :param index_rst_contents: Write this to the file.

    :return: Parent a.href for each image in index.html.
    """
    index_rst = app.srcdir / "index.rst"
    index_html = app.outdir / "index.html"

    index_rst.write_text(index_rst_contents)
    app.build()

    index_html_contents = index_html.read_text(encoding="utf8")
    index_html_bs = BeautifulSoup(index_html_contents, "html.parser")
    return [img.parent.get("href") for img in index_html_bs.find_all("img")]


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    confoverrides={
        "thumb_image_resize_width": 100,
    },
)
def test_no_target(app: SphinxTestApp):
    """Test without option (control)."""
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
        """),
    )
    assert hrefs == [None]


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    confoverrides={
        "thumb_image_resize_width": 100,
        "thumb_image_default_target": "https://localhost/%(fullsize_path)s",
    },
)
def test_default_target(app: SphinxTestApp):
    """Test cases for the option."""
    # Just config.
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
        """),
    )
    assert hrefs == ["https://localhost/%(fullsize_path)s"]

    # Format.
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target-format:
        """),
    )
    assert hrefs == ["https://localhost/_images/tux.png"]

    # Negate.
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :no-default-target:
        """),
    )
    assert hrefs == [None]

    # Target specified.
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://github.com
        """),
    )
    assert hrefs == ["https://github.com"]
