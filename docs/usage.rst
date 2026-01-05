.. _usage:

=====
Usage
=====

Two directives are provided by the extension.

Images
======

.. tab-set::

    .. tab-item:: Thumbnail

        .. thumb-image:: _images/tux.png
            :resize-width: 100px

    .. tab-item:: Original

        .. image:: _images/tux.png

.. tab-set::

    .. tab-item:: reStructuredText

        .. code-block:: reStructuredText

            .. thumb-image:: _images/tux.png
                :resize-width: 100px

    .. tab-item:: Markdown

        .. code-block:: Markdown

            ```{thumb-image} _images/tux.png
            :resize-width: 100px
            ```

.. rst:directive:: thumb-image

    Equivalent to the built in `image directive <http://docutils.sourceforge.net/docs/ref/rst/directives.html#image>`_.
    Display a thumbnail image in the document the same way a regular image is displayed.

    .. attribute:: align/alt/height/width/scale/target

        Same as the image directive. No resizing performed by these options.

    .. rst:directive:option:: resize-width

        Resize the image into a thumbnail with this width (aspect ratio will be maintained). The resized image is only saved
        in the output directory (and the `doctreedir`_ for caching). A default width may be defined with
        :option:`thumb_image_resize_width` in ``conf.py``.

TODO

Figures
=======

TODO

Configuration
=============

Set defaults for the extension in your ``conf.py`` file:

.. option:: thumb_image_resize_width

    *Default:* None

    TODO or with the :rst:dir:`thumb-image:resize-width` option.

.. _doctreedir: https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.doctreedir
