"""Test re-creating the thumbnail when an image's mtime changes."""

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
    write_docs={
        "control.rst": dedent("""
            :orphan:\n
            .. image:: _images/apple.jpg
        """),
        "test.rst": dedent("""
            :orphan:\n
            .. thumb-image:: _images/tux.png
        """),
    },
)
def test(app: SphinxTestApp):
    """Test cases for the option."""
    # Initial build.
    app.build()
    log = app.status.getvalue()
    assert "writing output... [ 33%] control" in log
    assert "writing output... [ 67%] index" in log
    assert "writing output... [100%] test" in log

    # No changes, confirm nothing on rebuild.
    pytest.skip("TODO")

    # Change control, only control changes.
    pytest.skip("TODO")

    # Change thumb, only thumb changes.
    pytest.skip("TODO")

    # Confirm no changes again.
    pytest.skip("TODO")
