"""Test thumbnail image file paths in HTML and on disk."""

from pathlib import Path
from textwrap import dedent

import PIL.Image
import pytest
from bs4 import element
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    write_docs={
        "index.rst": dedent("""
            .. image:: _images/tux.png
            .. thumb-image:: _images/tux.png
                :resize-width: 100
            .. thumb-image:: _images/tux.png
                :resize-width: 50
        """),
    },
)
def test_no_collisions(outdir: Path, img_tags: list[element.Tag]):
    """Confirm extension does not clobber non-thumbed image files."""
    # Confirm img src.
    img_src = sorted(t["src"] for t in img_tags)
    assert img_src == [
        "_images/tux.100x118.png",
        "_images/tux.50x59.png",
        "_images/tux.png",
    ]
    # Confirm files on disk.
    assert sorted(f.name for f in (outdir / "_images").iterdir()) == [
        "tux.100x118.png",
        "tux.50x59.png",
        "tux.png",
    ]


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    write_docs={
        "index.rst": dedent("""
            .. thumb-image:: _images/tux.png
                :resize-width: 100
            .. thumb-image:: _images/tux.png
                :resize-width: 50
        """),
    },
)
def test_efficient(outdir: Path, img_tags: list[element.Tag]):
    """Confirm original image files not in output directory if not needed."""
    # Confirm img src.
    img_src = [t["src"] for t in img_tags]
    assert img_src == [
        "_images/tux.100x118.png",
        "_images/tux.50x59.png",
    ]
    # Confirm files on disk.
    assert sorted(f.name for f in (outdir / "_images").iterdir()) == [
        "tux.100x118.png",
        "tux.50x59.png",
    ]


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    copy_files=[
        ("_images/tux.png", "sub/pictures/tux.png"),
        ("_images/tux.png", "sub/pictures/x_no_ext"),
    ],
    write_docs={
        "index.rst": dedent("""
            .. thumb-image:: _images/tux.png
                :resize-width: 100
        """),
        "sub/sub.rst": dedent("""
            :orphan:\n
            .. thumb-image:: pictures/tux.png
                :resize-width: 100
            .. thumb-image:: pictures/x_no_ext
                :resize-width: 100
        """),
    },
)
def test_doctrees_paths(monkeypatch: pytest.MonkeyPatch, app: SphinxTestApp):
    """Confirm resized image paths keep their full relative path to srcdir to prevent collisions."""
    open_paths = []
    save_paths = []

    # Patch open.
    orig_pil_image_open = PIL.Image.open

    def spy_pil_open(path, *args, **kwargs):
        open_paths.append(path.relative_to(app.srcdir))
        return orig_pil_image_open(path, *args, **kwargs)

    monkeypatch.setattr(PIL.Image, "open", spy_pil_open)

    # Patch save.
    orig_pil_image_save = PIL.Image.Image.save

    def spy_pil_save(self, path, *args, **kwargs):
        save_paths.append(path.relative_to(app.srcdir))
        return orig_pil_image_save(self, path, *args, **kwargs)

    monkeypatch.setattr(PIL.Image.Image, "save", spy_pil_save)

    # Run.
    app.build()

    # Check patched.
    assert open_paths == [
        Path("_images/tux.png"),
        Path("sub/pictures/tux.png"),
        Path("sub/pictures/x_no_ext"),
    ]
    assert save_paths == [
        Path("_build/doctrees/_thumbs/_images/tux.100x118.png"),
        Path("_build/doctrees/_thumbs/sub/pictures/tux.100x118.png"),
        Path("_build/doctrees/_thumbs/sub/pictures/x_no_ext.100x118"),
    ]

    # Check doctreedir contents.
    doctreedir_thumbs = app.doctreedir / "_thumbs"
    assert sorted(f.relative_to(doctreedir_thumbs) for f in doctreedir_thumbs.rglob("*")) == [
        Path("_images"),
        Path("_images/tux.100x118.png"),
        Path("sub"),
        Path("sub/pictures"),
        Path("sub/pictures/tux.100x118.png"),
        Path("sub/pictures/x_no_ext.100x118"),
    ]


@pytest.mark.sphinx("html", testroot="defaults")
def test_absolut_path(monkeypatch: pytest.MonkeyPatch, app: SphinxTestApp):
    """Test with absolute path to image."""
    open_paths = []
    save_paths = []

    # Patch open.
    orig_pil_image_open = PIL.Image.open

    def spy_pil_open(path, *args, **kwargs):
        open_paths.append(path.relative_to(app.srcdir))
        return orig_pil_image_open(path, *args, **kwargs)

    monkeypatch.setattr(PIL.Image, "open", spy_pil_open)

    # Patch save.
    orig_pil_image_save = PIL.Image.Image.save

    def spy_pil_save(self, path, *args, **kwargs):
        save_paths.append(path.relative_to(app.srcdir))
        return orig_pil_image_save(self, path, *args, **kwargs)

    monkeypatch.setattr(PIL.Image.Image, "save", spy_pil_save)

    # Write test document.
    tux_png_path = app.srcdir / "_images" / "tux.png"
    index_rst_contents = dedent(f"""\
        .. thumb-image:: {tux_png_path.absolute().as_posix()}
            :resize-width: 100
    """)
    assert "tests_unit_tests_test_paths_py__test_absolut_path" in index_rst_contents
    index_rst = app.srcdir / "index.rst"
    index_rst.write_text(index_rst_contents, encoding="utf8")

    # Run.
    app.build()

    # Check patched.
    assert open_paths == [
        Path("_images/tux.png"),
    ]
    assert save_paths == [
        Path("_build/doctrees/_thumbs/_images/tux.100x118.png"),
    ]

    # Check doctreedir contents.
    doctreedir_thumbs = app.doctreedir / "_thumbs"
    assert sorted(f.relative_to(doctreedir_thumbs) for f in doctreedir_thumbs.rglob("*")) == [
        Path("_images"),
        Path("_images/tux.100x118.png"),
    ]
