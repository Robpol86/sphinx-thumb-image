"""Test re-creating the thumbnail when an image's mtime changes."""

import time
from datetime import timedelta
from textwrap import dedent

import pytest
from sphinx.testing.util import SphinxTestApp

DELAY = timedelta(seconds=1.5)


def build_return_log(app: SphinxTestApp) -> str:
    """Reset the test environment, Sphinx build, and return the log.

    :param app: Sphinx test app.

    :return: Entire log output for this build.
    """
    app.status.truncate(0)
    app.status.seek(0)
    app.build()
    return app.status.getvalue()


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
    track_files = dict(
        apple_src=app.srcdir / "_images" / "apple.jpg",
        tux_src=app.srcdir / "_images" / "tux.png",
        tux_intermed=app.doctreedir / "_thumbs" / "_images" / "tux.100x118.png",
        apple_out=app.outdir / "_images" / "apple.jpg",
        tux_out=app.outdir / "_images" / "tux.100x118.png",
        control_out=app.outdir / "control.html",
        index_out=app.outdir / "index.html",
        test_out=app.outdir / "test.html",
    )

    # Initial build.
    log = build_return_log(app)
    assert "\ndocnames to write: control, index, test\n" in log

    # No changes, confirm nothing on rebuild.
    mtimes_before = {k: v.stat().st_mtime for k, v in track_files.items()}
    log = build_return_log(app)
    assert "no targets are out of date" in log
    mtimes_after = {k: v.stat().st_mtime for k, v in track_files.items()}
    assert mtimes_before == mtimes_after

    # Change control, only control changes.
    time.sleep(DELAY.total_seconds())
    (app.srcdir / "control.rst").touch(exist_ok=True)
    log = build_return_log(app)
    assert "\ndocnames to write: control\n" in log
    pytest.skip("TODO")

    # Change thumb, only thumb changes.
    pytest.skip("TODO")

    # Confirm no changes again.
    pytest.skip("TODO")
