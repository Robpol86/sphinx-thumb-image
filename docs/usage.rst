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

    .. tab-item:: Fullsize

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
    Display a thumbnail image in the document the same way a regular image is displayed. The resized image is written to the
    Sphinx build working directory `doctreedir`_ and copied into the output image directory. If no other image directives
    reference the fullsize image it won't be copied into the output directory to save disk space.

    .. attribute:: align/alt/height/width/scale/target

        Same as the image directive. No resizing performed by these options.

    .. rst:directive:option:: resize-width

        Resize the image into a thumbnail with this width in pixels with the height automatically calculated to maintain the
        same aspect ratio. Can be an integer or a string such as :guilabel:`"100px"`. If :rst:dir:`thumb-image:resize-width`
        and :rst:dir:`thumb-image:resize-height` are both specified the thumbnail will retain its aspect ratio and will be
        scaled down to fit within both dimensions. A default width may be specified with :option:`thumb_image_resize_width`
        in ``conf.py``.

    .. rst:directive:option:: resize-height

        Resize the image into a thumbnail with this height in pixels with the width automatically calculated to maintain the
        same aspect ratio. Can be an integer or a string such as :guilabel:`"100px"`. If :rst:dir:`thumb-image:resize-width`
        and :rst:dir:`thumb-image:resize-height` are both specified the thumbnail will retain its aspect ratio and will be
        scaled down to fit within both dimensions. A default width may be specified with :option:`thumb_image_resize_width`
        in ``conf.py``.

Figures
=======

.. tab-set::

    .. tab-item:: Thumbnail

        .. thumb-figure:: _images/tux.png
            :resize-width: 100px

            This is a thumbnail.

    .. tab-item:: Fullsize

        .. figure:: _images/tux.png

            This is the fullsize original.

.. tab-set::

    .. tab-item:: reStructuredText

        .. code-block:: reStructuredText

            .. thumb-figure:: _images/tux.png
                :resize-width: 100px

                This is a thumbnail.

    .. tab-item:: Markdown

        .. code-block:: Markdown

            ```{thumb-figure} _images/tux.png
            :resize-width: 100px

            This is a thumbnail.
            ```

.. rst:directive:: thumb-figure

    Figures have the same options as the :rst:dir:`thumb-image` directive.

Configuration
=============

Set defaults for the extension in your ``conf.py`` file:

.. option:: thumb_image_resize_width

    *Default:* :guilabel:`None`

    Default width in pixels to use for all thumbnails. Can be an integer or a string such as :guilabel:`"100px"`. This can be
    overridden with the :rst:dir:`thumb-image:resize-width` option in the directive in document files. If
    :option:`thumb_image_resize_width` and :option:`thumb_image_resize_height` are both set the thumbnail will retain its
    aspect ratio and fit within both dimensions.

.. option:: thumb_image_resize_height

    *Default:* :guilabel:`None`

    Default height in pixels to use for all thumbnails. Can be an integer or a string such as :guilabel:`"100px"`. This can
    be overridden with the :rst:dir:`thumb-image:resize-height` option in the directive in document files. If
    :option:`thumb_image_resize_width` and :option:`thumb_image_resize_height` are both set the thumbnail will retain its
    aspect ratio and fit within both dimensions.

.. _doctreedir: https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.doctreedir
