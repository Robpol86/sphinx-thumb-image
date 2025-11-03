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
def _sphinx_app(app: SphinxTestApp):
    """Instantiate a new Sphinx app per test function."""
    app.build()
    yield app


@pytest.fixture(name="index_html")
def _index_html(sphinx_app: SphinxTestApp) -> BeautifulSoup:
    """Read and parse generated test index.html."""
    text = (Path(sphinx_app.outdir) / "index.html").read_text(encoding="utf8")
    return BeautifulSoup(text, "html.parser")


@pytest.fixture()
def img_tags(index_html: BeautifulSoup) -> List[element.Tag]:
    """Return all <img> tags in index.html."""
    return index_html.find_all("img")
