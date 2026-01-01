"""TODO."""

from textwrap import dedent

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp


def write_build_read(app: SphinxTestApp, index_rst_contents: str) -> str:
    """TODO."""
    index_rst = app.srcdir / "index.rst"
    index_html = app.outdir / "index.html"

    index_rst.write_text(index_rst_contents)
    app.build()

    index_html_contents = index_html.read_text(encoding="utf8")
    index_html_bs = BeautifulSoup(index_html_contents, "html.parser")
    return index_html_bs.find_all("img")[0].parent.get("href")


# @pytest.mark.parametrize(
#     "app_params,expected",
#     [
#         (
#             {
#                 "write_docs": {
#                     "index.rst": dedent(r"""
#                         .. thumb-image:: _images/tux.png
#                             :target: https://github.com/Robpol86/sphinx-thumb-image/blob/{branch}/docs/{fullsize_path}
#                     """),
#                 }
#             },
#             r"https://github.com/Robpol86/sphinx-thumb-image/blob/{branch}/docs/{fullsize_path}",
#         ),
#         (
#             {
#                 "write_docs": {
#                     "index.rst": dedent(r"""
#                         .. thumb-image:: _images/tux.png
#                             :target: https://github.com/Robpol86/sphinx-thumb-image/blob/{branch}/docs/{fullsize_path}
#                             :target-format:
#                     """),
#                 }
#             },
#             "https://github.com/Robpol86/sphinx-thumb-image/blob/mock_branch/docs/_images/tux.png",
#         ),
#         (
#             {
#                 "write_docs": {
#                     "index.rst": dedent(r"""
#                         .. thumb-image:: _images/tux.png
#                             :target: https://localhost/{ignore}/{fullsize_path}
#                             :target-format:
#                     """),
#                 }
#             },
#             "https://github.com/Robpol86/sphinx-thumb-image/blob/mock_branch/docs/_images/tux.png",
#         ),
#     ],
#     indirect=["app_params"],
#     ids=lambda param: str(param) if isinstance(param, list) else param,
# )
@pytest.mark.sphinx("html", testroot="defaults", confoverrides={"thumb_image_resize_width": 100})
def test_target_format(app: SphinxTestApp):
    """TODO."""
    # Just target (control).
    href = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://github.com/Robpol86/sphinx-thumb-image/blob/{branch}/docs/{fullsize_path}
        """),
    )
    assert href == r"https://github.com/Robpol86/sphinx-thumb-image/blob/{branch}/docs/{fullsize_path}"

    pytest.skip("TODO")

    # Format via directive.
    href = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://github.com/Robpol86/sphinx-thumb-image/blob/{branch}/docs/{fullsize_path}
                :target-format:
        """),
    )
    assert href == r"https://github.com/Robpol86/sphinx-thumb-image/blob/mock_branch/docs/_images/tux.png"

    # Format via conf.
    app.confoverride = {"thumb_image_target_format": True}
    href = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://github.com/Robpol86/sphinx-thumb-image/blob/{branch}/docs/{fullsize_path}
        """),
    )
    assert href == r"https://github.com/Robpol86/sphinx-thumb-image/blob/mock_branch/docs/_images/tux.png"

    # Negate conf.
    app.confoverride = {"thumb_image_target_format": True}
    href = write_build_read(
        app,
        dedent(r"""\
            .. thumb-image:: _images/tux.png
                :target: https://github.com/Robpol86/sphinx-thumb-image/blob/{branch}/docs/{fullsize_path}
                :no-target-format:
        """),
    )
    assert href == r"https://github.com/Robpol86/sphinx-thumb-image/blob/{branch}/docs/{fullsize_path}"

    # Ignore unknown.
    # TODO

    # Warn on no format.
    # TODO
