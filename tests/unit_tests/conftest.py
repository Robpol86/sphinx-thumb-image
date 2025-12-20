"""pytest fixtures."""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup, element
from sphinx.testing.util import SphinxTestApp

pytest_plugins = ("sphinx.testing.fixtures",)  # pylint: disable=invalid-name


@pytest.fixture(scope="session")
def rootdir() -> Path:
    """Return the directory containing all test docs (used by sphinx.testing)."""
    return Path(__file__).parent / "test_docs"


@pytest.fixture(name="app_params")
def _app_params(app_params, request: pytest.FixtureRequest):
    """Inject Sphinx test app config before each test, including conf overrides (enabled with indirect=True)."""
    app_params.kwargs["exception_on_warning"] = True
    app_params.kwargs["warningiserror"] = True
    app_params.kwargs["freshenv"] = True
    # Implement write_docs.
    if "write_docs" in app_params.kwargs:
        srcdir = app_params.kwargs["srcdir"]
        for path, contents in app_params.kwargs["write_docs"].items():
            (srcdir / path).write_text(contents, encoding="utf8")
    # Implement parametrized confoverrides/write_docs.
    if hasattr(request, "param"):
        if "write_docs" in request.param:
            srcdir = app_params.kwargs["srcdir"]
            for path, contents in request.param["write_docs"].items():
                (srcdir / path).write_text(contents, encoding="utf8")
        if "confoverrides" in request.param:
            for key, value in request.param["confoverrides"].items():
                app_params.kwargs.setdefault("confoverrides", {})[key] = value
    return app_params


@pytest.fixture(name="sphinx_app")
def _sphinx_app(app: SphinxTestApp):
    """Instantiate a new Sphinx app per test function. Capture exceptions if sphinx_errors fixture used."""
    app.build()
    yield app


@pytest.fixture(name="outdir")
def _outdir(sphinx_app: SphinxTestApp) -> Path:
    """Return the Sphinx build output directory."""
    return Path(sphinx_app.outdir)


@pytest.fixture(name="master_html")
def _master_html(sphinx_app: SphinxTestApp, outdir: Path) -> BeautifulSoup:
    """Read and parse generated html."""
    text = (outdir / f"{sphinx_app.config.master_doc}.html").read_text(encoding="utf8")
    return BeautifulSoup(text, "html.parser")


@pytest.fixture()
def img_tags(master_html: BeautifulSoup) -> list[element.Tag]:
    """Return all <img> tags in html."""
    return master_html.find_all("img")
