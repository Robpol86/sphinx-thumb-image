"""Test the "target-format" directive option."""

from pathlib import Path
from textwrap import dedent

import pytest
from bs4 import BeautifulSoup, element
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
    warningiserror=False,
    exception_on_warning=False,
    confoverrides={
        "thumb_image_resize_width": 100,
        "thumb_image_target_format_substitutions": {"branch": "mock_branch"},
    },
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
    assert hrefs == ["https://github.com/Robpol86/sphinx-thumb-image/blob/%(branch)s/docs/%(fullsize_path)s"]
    assert app.warning.getvalue() == ""

    # Format via directive.
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://github.com/Robpol86/sphinx-thumb-image/blob/%(branch)s/docs/%(fullsize_path)s
                :target-format:
        """),
    )
    assert hrefs == ["https://github.com/Robpol86/sphinx-thumb-image/blob/mock_branch/docs/_images/tux.png"]
    assert app.warning.getvalue() == ""

    # Noop.
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target-format:
        """),
    )
    assert hrefs == [None]
    assert app.warning.getvalue() == ""

    # Format via conf.
    monkeypatch.setattr(app.config, "thumb_image_target_format", True)
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://github.com/Robpol86/sphinx-thumb-image/blob/%(branch)s/docs/%(fullsize_path)s
        """),
    )
    assert hrefs == ["https://github.com/Robpol86/sphinx-thumb-image/blob/mock_branch/docs/_images/tux.png"]
    assert app.warning.getvalue() == ""
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
    assert hrefs == ["https://github.com/Robpol86/sphinx-thumb-image/blob/%(branch)s/docs/%(fullsize_path)s"]
    assert app.warning.getvalue() == ""
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
    assert hrefs == ["https://localhost/%(ignore)s/_images/tux.png"]
    assert app.warning.getvalue() == ""

    # Warn on no format.
    hrefs = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://localhost
                :target-format:
        """),
    )
    assert hrefs == ["https://localhost"]
    warnings = app.warning.getvalue()
    assert 'WARNING: no subtitutions made by "target-format" in "target"' in warnings


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    confoverrides={"thumb_image_resize_width": 100},
    copy_files=[
        ("_images/tux.png", "sub/pictures/tux.png"),
    ],
    write_docs={
        "sub/sub.rst": dedent("""
            :orphan:\n
            .. thumb-image:: pictures/tux.png
                :target: https://github.com/Robpol86/sphinx-thumb-image/blob/mock_branch/docs/%(fullsize_path)s
                :target-format:
        """),
    },
)
def test_subdir(outdir: Path):
    """Test path to an iamge in a subdirectory."""
    sub_html = outdir / "sub" / "sub.html"
    sub_html_contents = sub_html.read_text(encoding="utf8")
    sub_html_bs = BeautifulSoup(sub_html_contents, "html.parser")
    hrefs = [img.parent.get("href") for img in sub_html_bs.find_all("img")]
    assert hrefs == ["https://github.com/Robpol86/sphinx-thumb-image/blob/mock_branch/docs/sub/pictures/tux.png"]


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    confoverrides={
        "thumb_image_resize_width": 100,
        "thumb_image_target_format": True,
        "thumb_image_target_format_substitutions": {"fullsize_rel": lambda **kw: kw["substitutions"]["fullsize_path"][2:]},
    },
    write_docs={
        "index.rst": dedent("""
            .. thumb-image:: _images/tux.png
                :target: https://localhost/%(fullsize_rel)s
        """),
    },
)
def test_callable(img_tags: list[element.Tag]):
    """TODO."""
    hrefs = [t.parent.get("href") for t in img_tags]
    assert hrefs == ["https://localhost/mages/tux.png"]
