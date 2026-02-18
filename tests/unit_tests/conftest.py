"""pytest fixtures."""

import re
import shutil
from pathlib import Path

import pytest
from bs4 import BeautifulSoup, element
from sphinx.testing.util import SphinxTestApp
from sphinx.util.console import nocolor

pytest_plugins = ("sphinx.testing.fixtures",)  # pylint: disable=invalid-name


def pytest_collection_modifyitems(items: list[pytest.Item]):
    """Modify tests before they run."""
    # Set srcdir to the test name so each test has a unique copy of test Sphinx docs.
    for item in items:
        mark_sphinx = item.get_closest_marker("sphinx")
        if mark_sphinx:
            if "srcdir" not in mark_sphinx.kwargs:
                mark_sphinx.kwargs["srcdir"] = re.sub(r"[^A-Za-z0-9_-]", "_", item.nodeid)


@pytest.fixture(scope="session")
def rootdir() -> Path:
    """Return the directory containing all test docs (used by sphinx.testing)."""
    return Path(__file__).parent / "test_docs"


@pytest.fixture(name="app_params")
def _app_params(app_params, request: pytest.FixtureRequest):
    """Inject Sphinx test app config before each test, including conf overrides (enabled with indirect=True)."""
    nocolor()
    app_params.kwargs.setdefault("exception_on_warning", True)
    app_params.kwargs.setdefault("warningiserror", True)
    app_params.kwargs.setdefault("freshenv", True)
    # app_params.kwargs["verbosity"] = 3
    srcdir: Path = app_params.kwargs["srcdir"]
    # Implement copy_files.
    for copy_files in (app_params.kwargs.get("copy_files", []), getattr(request, "param", {}).get("copy_files", [])):
        for copy_from, copy_to in copy_files:
            source: Path = srcdir / copy_from
            target: Path = srcdir / copy_to
            target.parent.mkdir(exist_ok=True, parents=True)
            shutil.copyfile(source, target)
    # Implement write_docs.
    for write_docs in (app_params.kwargs.get("write_docs", {}), getattr(request, "param", {}).get("write_docs", {})):
        for path, contents in write_docs.items():
            target: Path = srcdir / path
            target.write_text(contents, encoding="utf8")
    # Implement confoverrides.
    if hasattr(request, "param") and "confoverrides" in request.param:
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
