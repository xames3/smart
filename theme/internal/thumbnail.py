"""\
SMART Sphinx Theme YouTube Thumbnail Directive
==============================================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Saturday, 6 September 2025
Last updated on: Sunday, 7 September 2025

This module defines a custom `thumbnail` directive for the SMART Sphinx
Theme. The directive allows authors to embed a YouTube video thumbnail
card directly within their documentation.

The `thumbnail` directive is designed to extend reStructuredText (rST)
capabilities by fetching metadata from a YouTube URL and rendering a
styled card.

The `thumbnail` directive can be used in reStructuredText documents as
follows::

    .. thumbnail:: https://www.youtube.com/watch?v=dQw4w9WgXcQ
        :title: Never Gonna Give You Up
        :channel: Rick Astley

The above snippet will be processed and rendered according to the
theme's Jinja2 template, producing a consistent thumbnail card in the
final HTML output.

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
import requests
from bs4 import BeautifulSoup as Soup


if t.TYPE_CHECKING:
    from sphinx.writers.html import HTMLTranslator

name: t.Final[str] = "thumbnail"
here: str = p.dirname(__file__)
html = p.join(p.abspath(p.join(here, "../base")), "thumbnail.html.jinja")

with open(html) as f:
    template = jinja2.Template(f.read())


class node(nodes.Element):
    """Class to represent a custom node in the document tree.

    This class extends the `nodes.Element` from `docutils`, serving as
    the container for the parsed information. The node will
    ultimately be transformed into HTML or other output formats by the
    relevant Sphinx translators.
    """


class directive(rst.Directive):
    """Custom `thumbnail` directive for reStructuredText.

    This class defines the behavior of the `thumbnail` directive,
    including how it processes arguments and options, fetches video
    metadata, and generates nodes to be inserted into the document tree.
    """

    has_content = True
    option_spec = {  # noqa: RUF012
        "title": rst.directives.unchanged,
        "channel": rst.directives.unchanged,
    }

    def run(self) -> list[nodes.Node]:
        """Parse the directive content, fetch metadata, and create a
        node tree.

        This method processes the YouTube URL from the directive's
        content, fetches metadata, and constructs a `thumbnail.node`
        containing parsed `docutils` nodes for the title and caption.
        This allows Sphinx to render them correctly.

        :return: A list containing a single `thumbnail.node` element.
        """
        self.assert_has_content()
        src = rst.directives.uri(self.content.pop())
        vid = src
        if "youtu.be/" in src:
            vid = src.rsplit("/", 1)[-1].split("?", 1)[0]
        elif "watch?v=" in src:
            vid = src.split("v=", 1)[-1].split("&", 1)[0]
        if "title" not in self.options:
            soup = Soup(requests.get(src, timeout=1).text, "html.parser")
            self.options["title"] = soup.find("title").text
        self.options["src"] = src
        self.options["thumbnail"] = (
            f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
        )
        attributes: dict[str, str] = {}
        attributes["text"] = template.render(**self.options)
        attributes["format"] = "html"
        return [nodes.raw(**attributes)]


def visit(self: HTMLTranslator, node: node) -> None:
    """Handle the entry processing of the `thumbnail` node during HTML
    generation.

    This method is called when the HTML translator encounters the
    `thumbnail` node in the document tree. It retrieves the relevant
    attributes from the node (like title and channel) and uses Jinja2
    templating to produce the final HTML output. Since the `thumbnail`
    node does not require any actions, the method currently acts as a
    placeholder.

    :param self: The HTML translator instance.
    :param node: The `thumbnail` node being processed.
    """


def depart(self: HTMLTranslator, node: node) -> None:
    """Handle the exit processing of the `thumbnail` node during HTML
    generation.

    This method is invoked after the node's HTML representation has been
    fully processed and added to the output. Since the `thumbnail` node
    does not require any closing actions, the method currently acts as a
    placeholder.

    :param self: The HTML translator instance.
    :param node: The `thumbnail` node being processed.
    """
