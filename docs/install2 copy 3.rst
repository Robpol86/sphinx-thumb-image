:orphan:

============
Installation
============

Getting started is pretty simple. The first step is to install the library.

.. tab-set::

    .. tab-item:: Install from PyPI

        .. code-block:: bash

            pip install sphinx-thumb-image

    .. tab-item:: Install from GitHub

        .. code-block:: bash

            pip install git+https://github.com/Robpol86/sphinx-thumb-image@main

Once the package is installed add this extension to your Sphinx extensions list in the ``conf.py`` file.

.. code-block:: python

    # conf.py
    extensions = [
         # ... other extensions here
         "sphinx_thumb_image",
    ]
