"""\
SMART Sphinx Theme Custom Roles
===============================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Friday, February 21 2025
Last updated on: Friday, February 21 2025

This module provides custom roles for the SMART Sphinx Theme, that
allows me, the author to add features to the documentation.

.. note::

    This module is designed specifically for the SMART Sphinx Theme,
    hence the role may not be available or may be implemented
    differently for different themes. Please consult the documentation
    for more information.
"""

from __future__ import annotations

import typing as t

import docutils.nodes as nodes


# TODO (xames3): Add example usage of the role. Explain how this role
# will be used in a reStructuredText document with some suitable
# examples.
def stylize(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: t.Any,
    options: dict[str, t.Any] | None = None,
    content: list[t.Any] | None = None,
) -> tuple[list[nodes.Node], list[nodes.system_message]]:
    """Apply inline styling to text.

    This function allows for applying a CSS style to a piece of text
    within reStructuredText using a role syntax. The expected input
    format is `text <style>`. If the input format is invalid, an error
    is reported.

    :param role: The role name used in the source text.
    :param rawtext: The entire markup text representing the role.
    :param text: The text by the user.
    :param lineno: The line number where the role was encountered in the
        source text.
    :param inliner: The inliner instance that called the role function.
    :param options: Additional options passed to the role function,
        defaults to `None`.
    :param content: Content passed to the role function, defaults
        to `None`.
    :return: A tuple of list with a single `nodes.raw` object
        representing the styled text and a list of system messages
        generated during processing (typically empty if no errors).
    :raises: None, but will report an error message if the input format
        is invalid.
    """
    try:
        element, style = map(str.strip, text.split("<", 1))
        style = style.rstrip(">")
    except ValueError:
        msg = inliner.reporter.error(
            f"Invalid style: {text!r}",
            nodes.literal_block(rawtext, rawtext),
            line=lineno,
        )
        return [inliner.problematic(rawtext, rawtext, msg)], [msg]
    raw = f'<span style="{style}">{element}</span>'
    return [nodes.raw(text=raw, format="html")], []
