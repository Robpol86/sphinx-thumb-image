"""pytest fixtures."""

from pathlib import Path
from typing import List

import pytest
from bs4 import BeautifulSoup, element
from sphinx.testing.util import SphinxTestApp

pytest_plugins = ("sphinx.testing.fixtures",)  # pylint: disable=invalid-name


@pytest.fixture(scope="session")
def rootdir() -> Path:
    """Return the directory containing all test docs (used by sphinx.testing)."""
    return Path(__file__).parent / "test_docs"


@pytest.fixture(name="sphinx_app")
def _sphinx_app(app: SphinxTestApp, request: pytest.FixtureRequest):
    """Instantiate a new Sphinx app per test function."""
    if hasattr(request, "param"):
        for key, value in request.param.items():
            app.config[key] = value
    app.warningiserror = True
    app.build()
    yield app


@pytest.fixture(name="master_html")
def _master_html(sphinx_app: SphinxTestApp) -> BeautifulSoup:
    """Read and parse generated html."""
    text = (Path(sphinx_app.outdir) / f"{sphinx_app.config.master_doc}.html").read_text(encoding="utf8")
    return BeautifulSoup(text, "html.parser")


@pytest.fixture()
def img_tags(master_html: BeautifulSoup) -> List[element.Tag]:
    """Return all <img> tags in html."""
    return master_html.find_all("img")
