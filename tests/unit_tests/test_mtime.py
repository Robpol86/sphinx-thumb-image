"""Test re-creating the thumbnail when an image's mtime changes."""

import sys
import time
from pathlib import Path
from textwrap import dedent

import pytest
from sphinx.testing.util import SphinxTestApp


def rebuild(
    app: SphinxTestApp, track_files: dict[str, Path], initial: bool = False
) -> tuple[dict[str, tuple], dict[str, tuple]]:
    """Reset the test environment, Sphinx build, and return before/after mtimes.

    :param app: Sphinx test app.
    :param track_files: Which files to get mtimes for.
    :param initial: If this is the first Sphinx build.

    :return: Before/after mtimes.
    """
    if initial:
        mtimes_before = {}
    else:
        mtimes_before = {k: v.stat().st_mtime for k, v in track_files.items()}
    app.build()
    mtimes_after = {k: v.stat().st_mtime for k, v in track_files.items()}
    return mtimes_before, mtimes_after


@pytest.mark.sphinx(
    "html",
    testroot="defaults",
    confoverrides={
        "thumb_image_resize_width": 100,
    },
    write_docs={
        "index.rst": dedent("""
            .. thumb-image:: _images/tux.png
        """),
    },
)
@pytest.mark.flaky(reruns=5, condition=sys.platform.startswith("win32"))  # Windows time precision issues.
def test_mtime(app: SphinxTestApp):
    """Test cases for the option."""
    track_files = dict(
        tux_src=app.srcdir / "_images" / "tux.png",
        tux_intermed=app.doctreedir / "_thumbs" / "_images" / "tux.100x118.png",
        tux_out=app.outdir / "_images" / "tux.100x118.png",
        index_out=app.outdir / "index.html",
    )

    # Initial build.
    rebuild(app, track_files, initial=True)

    # No changes, confirm nothing on rebuild.
    mtimes_before, mtimes_after = rebuild(app, track_files)
    assert mtimes_before == mtimes_after

    # Change mtime.
    time.sleep(1.5)  # TODO reduce
    track_files["tux_src"].touch(exist_ok=True)
    mtimes_before, mtimes_after = rebuild(app, track_files)

    tux_intermed_before = mtimes_before.pop("tux_intermed")
    tux_intermed_after = mtimes_after.pop("tux_intermed")
    pytest.skip("TODO implement")
    assert tux_intermed_before < tux_intermed_after

    # TODO uncomment below when resolved: https://github.com/sphinx-doc/sphinx/issues/14312
    # tux_out_before = mtimes_before.pop("tux_out")
    # tux_out_after = mtimes_after.pop("tux_out")
    # assert tux_out_before < tux_out_after

    index_out_before = mtimes_before.pop("index_out")
    index_out_after = mtimes_after.pop("index_out")
    assert index_out_before < index_out_after

    assert mtimes_before == mtimes_after

    # Confirm no changes again.
    mtimes_before, mtimes_after = rebuild(app, track_files)
    assert mtimes_before == mtimes_after
