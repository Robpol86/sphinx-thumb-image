"""Test re-creating the thumbnail when an image's mtime changes."""

import time
from datetime import timedelta
from pathlib import Path
from textwrap import dedent

import pytest
from sphinx.testing.util import SphinxTestApp

DELAY = timedelta(seconds=1.5)


def build_return(app: SphinxTestApp, track_files: dict[str, Path]) -> tuple[str, dict[str, tuple], dict[str, tuple]]:
    """Reset the test environment, Sphinx build, and return the log and before/after mtimes.

    :param app: Sphinx test app.

    :return: Entire log output for this build and before/after mtimes.
    """
    mtimes_before = {k: v.stat().st_mtime for k, v in track_files.items()}
    app.status.truncate(0)
    app.status.seek(0)
    app.build()
    mtimes_after = {k: v.stat().st_mtime for k, v in track_files.items()}
    return app.status.getvalue(), mtimes_before, mtimes_after


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
    app.build()
    log = app.status.getvalue()
    assert "\ndocnames to write: control, index, test\n" in log

    # No changes, confirm nothing on rebuild.
    log, mtimes_before, mtimes_after = build_return(app, track_files)
    assert "\nno targets are out of date.\n" in log
    assert mtimes_before == mtimes_after

    # Change control, only control changes.
    time.sleep(DELAY.total_seconds())
    track_files["apple_src"].touch(exist_ok=True)
    log, mtimes_before, mtimes_after = build_return(app, track_files)
    assert "\ndocnames to write: control\n" in log
    apple_out_before = mtimes_before.pop("apple_out")
    apple_out_after = mtimes_after.pop("apple_out")
    assert apple_out_before < apple_out_after
    pytest.skip("TODO fix below")
    control_out_before = mtimes_before.pop("control_out")
    control_out_after = mtimes_after.pop("control_out")
    assert control_out_before < control_out_after
    assert mtimes_before == mtimes_after

    # Change thumb, only thumb changes.
    pytest.skip("TODO")

    # Confirm no changes again.
    pytest.skip("TODO")
