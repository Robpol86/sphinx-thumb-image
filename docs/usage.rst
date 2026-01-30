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
    reference the fullsize image it won't be copied into the output documentation directory to save disk space.

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

    .. rst:directive:option:: no-resize

        Does not resize the image and instead just copies it to the output documentation directory. Useful when you want to
        use the other features in the extension for images that are already small.

    .. rst:directive:option:: resize-quality

        An integer between 1 and 100 that overrides the
        [default image save quality](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html) used by PIL.

    .. rst:directive:option:: no-resize-quality

        Boolean option to ignore :option:`thumb_image_resize_quality` if it is set.

    .. rst:directive:option:: is-animated

        Boolean option that indicates the image is animated (e.g. an animated GIF).

    .. rst:directive:option:: no-is-animated

        Boolean option to negate :rst:dir:`thumb-image:is-animated` if :option:`thumb_image_is_animated` is ``True``.

    .. rst:directive:option:: target-format

        Boolean option to enable substitutions in the built in ``:target:`` option. Built in substitutions:

        * ``%(raw_path)s``: Replaced with the path to the original fullsize image as given in the directive
        * ``%(fullsize_path)s``: Replaced with the path to the original fullsize image taking into account subdirectories

        Additional substitutions may be provided with the :option:`thumb_image_target_format_substitutions` option in your
        ``conf.py``.

        Here's an example for the file ``docs/posts/2026/guide.rst`` (``conf.py`` is located at ``docs/conf.py`` in this
        example):

        .. code-block:: reStructuredText

            .. thumb-image:: assets/tux.png
                :target: https://cdn/account/docs/%(fullsize_path)s
                :target-format:

        The thumbnail image will link to ``https://cdn/account/docs/posts/2026/assets/tux.png``.

        Substitutions can also incorporate string slicing:

        .. code-block:: reStructuredText

            .. thumb-image:: assets/tux.png
                :target: https://cdn/account/docs/%(fullsize_path:6:-4)s
                :target-format:

        The thumbnail image will link to ``https://cdn/account/docs/2026/assets/tux``.

    .. rst:directive:option:: no-target-format

        Boolean option to negate :rst:dir:`thumb-image:target-format` if :option:`thumb_image_target_format` is ``True``.

    .. rst:directive:option:: no-default-target

        Boolean option to ignore :option:`thumb_image_default_target` and leave the target unmodified.

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

List Table Thumbs
=================

.. list-table-thumbs::
    :resize-width: 90px

    * - .. thumb-image:: _images/tux.png
      - .. thumb-image:: _images/tux.png
    * - .. thumb-image:: _images/tux.png
      - .. thumb-image:: _images/tux.png

.. tab-set::

    .. tab-item:: reStructuredText

        .. code-block:: reStructuredText

            .. list-table-thumbs::
                :resize-width: 90px

                * - .. thumb-image:: _images/tux.png
                  - .. thumb-image:: _images/tux.png
                * - .. thumb-image:: _images/tux.png
                  - .. thumb-image:: _images/tux.png

    .. tab-item:: Markdown

        .. code-block:: Markdown

            ```{list-table-thumbs}
            :resize-width: 90px

            * - :::{thumb-image} _images/tux.png
                :::
              - :::{thumb-image} _images/tux.png
                :::
            * - :::{thumb-image} _images/tux.png
                :::
              - :::{thumb-image} _images/tux.png
                :::
            ```

.. rst:directive:: list-table-thumbs

    Equivalent to the built in `list-table`_ directive. The difference is that it supports additional options that are passed
    to thumbnails in the table. This helps reduce repeated lines in your documentation such as if all the thumbnails have the
    same width.

    .. rst:directive:option:: resize-width
    .. rst:directive:option:: resize-height

        Applied to each :rst:dir:`thumb-image` and :rst:dir:`thumb-figure` directives used in the table.

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

.. option:: thumb_image_resize_quality

    *Default:* :guilabel:`None`

    Sets :rst:dir:`thumb-image:resize-quality` by default for all thumb directives if set.

.. option:: thumb_image_is_animated

    *Default:* :guilabel:`False`

    Sets :rst:dir:`thumb-image:is-animated` by default for all thumb directives if True.

.. option:: thumb_image_target_format

    *Default:* :guilabel:`False`

    Sets :rst:dir:`thumb-image:target-format` by default for all thumb directives if True.

.. option:: thumb_image_target_format_substitutions

    *Default:* :guilabel:`dict()`

    Provide additional substitutions with this option. Example:

    .. code-block:: python

        thumb_image_target_format_substitutions = {"key": "value"}

    Will replace ``%(key)s`` with ``value``.

    You can also specify functions or callables as values:

    .. code-block:: python

        def formatter(self, substitutions, target, env):
            return substitutions["fullsize_path"][2:]
        thumb_image_target_format_substitutions = {"key": formatter}

.. option:: thumb_image_default_target

    *Default:* :guilabel:`None`

    Sets a thumb's `target`_ URL by default for all thumb directives if set to a string. Use this if all thumb images should
    link to files in the same location, such as an image host or another git repository's web interface. Supports formatting
    like :rst:dir:`thumb-image:target-format`.

.. _doctreedir: https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.doctreedir
.. _list-table: https://docutils.sourceforge.io/docs/ref/rst/directives.html#list-table
.. _target: https://docutils.sourceforge.io/docs/ref/rst/directives.html#target
