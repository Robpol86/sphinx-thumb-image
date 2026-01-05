"""Sphinx configuration file."""

# pylint: disable=invalid-name

import time
from pathlib import Path

import toml

PYPROJECT = toml.loads(Path(__file__).parent.parent.joinpath("pyproject.toml").read_text(encoding="utf8"))


# General configuration.
author = PYPROJECT["project"]["authors"][0]["name"]
copyright = f"{time.strftime('%Y')}, {author}"  # pylint: disable=redefined-builtin  # noqa
html_last_updated_fmt = f"%c {time.tzname[time.localtime().tm_isdst]}"
exclude_patterns = []
extensions = [
    "notfound.extension",  # https://sphinx-notfound-page.readthedocs.io
    "sphinx_copybutton",  # https://sphinx-copybutton.readthedocs.io
    "sphinx_design",  # https://sphinx-design.readthedocs.io
    "sphinx_thumb_image",
    "sphinxext.opengraph",  # https://sphinxext-opengraph.readthedocs.io
]
language = "en"
project = PYPROJECT["project"]["name"]
pygments_style = "sphinx"


# Options for HTML output.
html_copy_source = False
html_theme = "sphinx_rtd_theme"


# https://sphinxext-opengraph.readthedocs.io/en/latest/#options
ogp_site_name = project
ogp_type = "website"
ogp_use_first_image = True
