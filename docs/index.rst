==================
Sphinx Thumb Image
==================

Resize images in Sphinx documents/pages to thumbnails.

The purpose of this extension is to save on web storage costs and bandwidth fees, including data rates your visitors may
incur from image-heavy documentation. If the fullsize image is not referenced by another image directive it won't be copied
into your build's output directory.

``sphinx-thumb-image`` provides a ``thumb-image`` directive similar to the built in ``image`` directive. Set the thumbnail
size using the ``:resize-width:`` and/or ``:resize-height:`` options.

A ``list-table-thumbs`` directive is also provided to help reduce repetition when a lot of thumbnails are nested within a
`list-table`_. See the :rst:dir:`list-table-thumbs` usage document for more information.

.. _list-table: https://docutils.sourceforge.io/docs/ref/rst/directives.html#list-table

Project Links
=============

* Documentation: https://sphinx-thumb-image.readthedocs.io
* Source code: https://github.com/Robpol86/sphinx-thumb-image
* PyPI homepage: https://pypi.org/project/sphinx-thumb-image

.. toctree::
    :maxdepth: 2
    :caption: Contents

    install
    usage
    examples
