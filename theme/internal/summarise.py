"""\
SMART Sphinx Theme Summarise Directive
======================================

Author: Akshay Mestry <xa@mes3.dev>
Created on: 22 October, 2025
Last updated on: 22 October, 2025

This module defines a custom `ask` directive for the SMART Sphinx Theme.
The directive allows authors to embed a `Summarise` button directly
within their documentation.

The `ask` directive is designed to extend reStructuredText (rST)
capabilities by injecting structured metadata about the feedback of the
content, which can be styled or processed further using Jinja2
templates.

The `ask` directive can be used in reStructuredText documents as
follows::

    .. code-block:: rst

        .. feedback::
            :maintitle: Tell me what you think
            :subtitle: You can send me your feedback via email.
            :buttontext: Send feedback

The above snippet will be processed and rendered according to the
theme's Jinja2 template, producing a final HTML output.

.. note::

    This directive is exclusive to the SMART Sphinx Theme. If you
    switch to a different theme, the behavior or availability of this
    directive may change. Please refer to the specific theme's
    documentation for further information.
"""

from __future__ import annotations

import os.path as p
import typing as t

import docutils.nodes as nodes
import docutils.parsers.rst as rst
import jinja2


if t.TYPE_CHECKING:
    from sphinx.writers.html import HTMLTranslator

name: t.Final[str] = "feedback"
here: str = p.dirname(__file__)
html = p.join(p.abspath(p.join(here, "../base")), "feedback.html.jinja")

with open(html) as f:
    template = jinja2.Template(f.read())


class node(nodes.Element):
    """Class to represent a custom node in the document tree.

    This class extends the `nodes.Element` from `docutils`, serving as
    the container for the parsed information. The node will ultimately
    be transformed into HTML or other output formats by the relevant
    Sphinx translators.
    """


class directive(rst.Directive):
    """Custom `ask` directive for reStructuredText.

    This class defines the behavior of the `ask` directive,
    including how it processes options and content, and how it generates
    nodes to be inserted into the document tree.

    The directive supports the following options::

        - `maintitle`: Title of the feedback form.
        - `subtitle`: Subtitle for the feedback form.
        - `buttontext`: Text that appears on the button.
    """

    has_content = False
    option_spec = {  # noqa: RUF012
        "maintitle": rst.directives.unchanged,
        "subtitle": rst.directives.unchanged,
        "buttontext": rst.directives.unchanged,
    }

    def run(self) -> list[nodes.Node]:
        """Parse directive options and create an `ask` node.

        This method gathers all options provided by the user in the
        `ask` directive, constructs a new `node` instance, and
        returns it wrapped in a list.

        The returned node is then placed into the document tree at the
        directive's location. Further processing will convert the node
        into HTML or other formats.

        :return: A list containing a single `node` element.
        """
        ctx = self.state.document.settings.env.config.html_context
        self.options.update(ctx)
        attributes: dict[str, str] = {}
        attributes["text"] = template.render(**self.options)
        attributes["format"] = "html"
        return [nodes.raw(**attributes)]


def visit(self: HTMLTranslator, node: node) -> None:
    """Handle the entry processing of the `ask` node during HTML
    generation.

    This method is called when the HTML translator encounters the
    `ask` node in the document tree. It retrieves the relevant
    attributes from the node and uses Jinja2 templating to produce the
    final HTML output. Since the `ask` node does not require any
    actions, the method currently acts as a placeholder.

    :param self: The HTML translator instance.
    :param node: The `ask` node being processed.
    """


def depart(self: HTMLTranslator, node: node) -> None:
    """Handle the exit processing of the `ask` node during HTML
    generation.

    This method is invoked after the node's HTML representation has been
    fully processed and added to the output. Since the `ask` node
    does not require any closing actions, the method currently acts as a
    placeholder.

    :param self: The HTML translator instance.
    :param node: The `ask` node being processed.
    """
