"""TODO."""

from textwrap import dedent

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp


def write_build_read(app: SphinxTestApp, index_rst_contents: str) -> list[str]:
    """TODO."""
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
    confoverrides={"thumb_image_resize_width": 100, "thumb_image_target_format_substitutions": {"branch": "mock_branch"}},
)
def test_target_format(app: SphinxTestApp):
    """TODO."""
    # Just target (control).
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://github.com/Robpol86/sphinx-thumb-image/blob/%(branch)s/docs/%(fullsize_path)s
        """),
    )
    assert hrefs == [r"https://github.com/Robpol86/sphinx-thumb-image/blob/%(branch)s/docs/%(fullsize_path)s"]

    # Format via directive.
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://github.com/Robpol86/sphinx-thumb-image/blob/%(branch)s/docs/%(fullsize_path)s
                :target-format:
        """),
    )
    assert hrefs == [r"https://github.com/Robpol86/sphinx-thumb-image/blob/mock_branch/docs/_images/tux.png"]

    # Noop.
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target-format:
        """),
    )
    assert hrefs == [None]
    pytest.skip("TODO")

    # Format via conf.
    app.confoverride = {"thumb_image_target_format": True}
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://github.com/Robpol86/sphinx-thumb-image/blob/%(branch)s/docs/%(fullsize_path)s
        """),
    )
    assert hrefs == [r"https://github.com/Robpol86/sphinx-thumb-image/blob/mock_branch/docs/_images/tux.png"]
    app.confoverride = {}

    # Negate conf.
    app.confoverride = {"thumb_image_target_format": True}
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://github.com/Robpol86/sphinx-thumb-image/blob/%(branch)s/docs/%(fullsize_path)s
                :no-target-format:
        """),
    )
    assert hrefs == [r"https://github.com/Robpol86/sphinx-thumb-image/blob/%(branch)s/docs/%(fullsize_path)s"]
    app.confoverride = {}

    # Ignore unknown.
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://localhost/%(ignore)s/%(fullsize_path)s
                :target-format:
        """),
    )
    assert hrefs == [r"https://localhost/%(ignore)s/_images/tux.png"]

    # Warn on no format.
    app.warningiserror = False
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://localhost
                :target-format:
        """),
    )
    assert hrefs == [r"https://localhost"]
    assert app.warnings == ["TODO nothing formatted"]
