# Contributing

Everyone that wants to contribute to the project should read this document.

## Bug Reports

If you're reporting a bug it's most helpful if you include steps to reproduce the issue. Include the following:

* Python version
* Sphinx version
* Your `conf.py`
* An example `rst` document that produces the bug

## Pull Requests

If you plan on submitting a pull request and you want to develop your contribution locally you can setup your local
environment using the steps below.

### Setup Development Environment

This project uses [uv](https://github.com/astral-sh/uv). After cloning this repo install `uv` and then run the following
before working on your code change:

```bash
make deps  # Installs Python dependencies in the ./.venv VirtualEnv.
make test  # Runs unit tests.
make lint  # Runs linters.
```

## Releases

These are the steps a maintainer will take to make a new release.

1. Create a new pull request with the following changes:
    1. Finalize the [CHANGELOG.md](CHANGELOG.md) file and resetting the **Unreleased** section to "N/A".
    2. Set the new version in the extension's [`__init__.py`](sphinx_thumb_image/__init__.py) file.
    3. Also set the new version in the [pyproject.toml](pyproject.toml) file.
    4. Run `make relock` to update the version in the `uv.lock` file.
2. After merging the PR manually draft a new release in: https://github.com/Robpol86/sphinx-thumb-image/releases
    1. Set a new tag using the `vX.X.X` convention.
    2. Set the release title using the `sphinx-thumb-image-X.X.X` convention.
    3. Click "Generate release notes".
3. Click "Publish release".
    1. https://github.com/Robpol86/sphinx-thumb-image/actions/workflows/pypi.yml will automatically run to publish to PyPI.
    1. Afterwards the workflow will also upload assets to the release you've just created.

## Thank You!

Thanks for fixing bugs or adding features to the project!
