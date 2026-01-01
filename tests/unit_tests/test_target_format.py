"""Test the "target-format" directive option."""

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
    confoverrides={"thumb_image_resize_width": 100, "thumb_image_target_format_substitutions": {"branch": "mock_branch"}},
)
def test_target_format(monkeypatch: pytest.MonkeyPatch, app: SphinxTestApp):
    """Test cases for the option."""
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

    # Format via conf.
    monkeypatch.setattr(app.config, "thumb_image_target_format", True)
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://github.com/Robpol86/sphinx-thumb-image/blob/%(branch)s/docs/%(fullsize_path)s
        """),
    )
    assert hrefs == [r"https://github.com/Robpol86/sphinx-thumb-image/blob/mock_branch/docs/_images/tux.png"]
    monkeypatch.undo()

    # Negate conf.
    monkeypatch.setattr(app.config, "thumb_image_target_format", True)
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://github.com/Robpol86/sphinx-thumb-image/blob/%(branch)s/docs/%(fullsize_path)s
                :no-target-format:
        """),
    )
    assert hrefs == [r"https://github.com/Robpol86/sphinx-thumb-image/blob/%(branch)s/docs/%(fullsize_path)s"]
    monkeypatch.undo()

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
    monkeypatch.setattr(app, "warningiserror", False)
    app.warning.truncate(0)  # Clear warnings.
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://localhost
                :target-format:
        """),
    )
    assert hrefs == [r"https://localhost"]
    assert 'WARNING: no subtitutions made by "target-format" in "target"' in app.warning.getvalue()
