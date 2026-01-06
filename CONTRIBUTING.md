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

## Thank You!

Thanks for fixing bugs or adding features to the project!
