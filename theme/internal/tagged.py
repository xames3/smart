"""\
SMART Sphinx Theme Tagged Directive
===================================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Saturday, 9 August 2025
Last updated on: Saturday, 9 August 2025

This module defines a custom `tagged` directive for the SMART Sphinx
Theme. The directive extends the standard `figure` so it retains all of
its features, while adding one extra option `faces` to overlay clickable
face tags on the image.

The `tagged` directive is designed to extend reStructuredText (rST)
capabilities by injecting tagged faces metadata. The `tagged` directive
can be used in reStructuredText documents as follows::

    .. code-block:: rst

        .. tagged:: ../assets/my-students.jpg
            :alt: My students at NASA Open Science 2025
            :figclass: zoom
            :faces: [
            [
                :face: John Wick
                :coords: [108, 112, 57, 57]
            ],
            [
                :face: Winston Scott
                :link: https://www.linkedin.com/in/winston-continental
                :coords: [0.05, 0.05, 0.15, 0.15]
            ],
        ]

Coordinates are the pixels of the image where the face(s) are marked.
Only `face` and `coords` are mandatory; `link` is optional. If `link` is
omitted, the tag will render as a non-clickable marker. Labels are
applied to `title` and `aria-label` for accessibility.

.. note::

    This directive is exclusive to the SMART Sphinx Theme. If you switch
    to a different theme, the behaviour or availability of this directive
    may change. Please refer to the specific theme documentation for
    further information.
"""

from __future__ import annotations

import re
import typing as t

import docutils.nodes as nodes
import docutils.parsers.rst as rst
from docutils.parsers.rst.directives.images import Figure

if t.TYPE_CHECKING:
    from sphinx.writers.html import HTMLTranslator

name: t.Final[str] = "tagged"
pattern: t.Final[str] = (
    r":face:\s*(?P<face>.*?)\s*(?::link:\s*(?P<link>.*?)\s*)?:coords:\s*"
    r"\[(?P<coords>[^\]]+)\]"
)


class node(nodes.Element):
    """Class to represent a custom node in the document tree.

    This class extends the `nodes.Element` from `docutils`, serving as
    the container for the parsed information. The node will ultimately
    be transformed into HTML or other output formats by the relevant
    Sphinx translators.
    """

    pass


def parse_faces(metadata: str) -> list[dict[str, t.Any]]:
    """Parse the `faces` metadata from the directive options.

    This function parses the `faces` metadata string into a list of
    dictionaries, each representing a face tag with its coordinates and
    optional hyperlink.

    :param metadata: The raw string containing faces data.
    :return: A list of dictionaries representing the parsed faces, or an
        empty list if no valid data is found.
    """
    faces: list[dict[str, t.Any]] = []
    for person in re.finditer(pattern, metadata):
        face = (person.group("face") or "").strip()
        group = person.groupdict().get("link")
        link = group.strip() if group else ""
        coords = [coord for coord in person.group("coords").strip().split(",")]
        faces.append({"face": face, "link": link, "coords": coords})
    return faces


class directive(Figure):
    """Custom `tagged` figure directive for reStructuredText.

    This class defines the behavior of the `tagged` directive, including
    how it processes options and content, and how it generates nodes to
    be inserted into the document tree. This directive inherits from
    Sphinx's `Figure` to preserve all features such as `alt`, `align`,
    `width`, `figwidth`, and captions. It adds a single option `faces`
    which is a list of dictionaries with the following keys:

        - `face`: The visible face used for accessibility.
        - `link`: Optional hyperlink to wrap the tag.
        - `coords`: A list of four numbers representing the coordinates.
    """

    has_content = True
    option_spec = Figure.option_spec.copy()
    option_spec["faces"] = rst.directives.unchanged_required

    def run(self) -> list[nodes.Node]:
        """Parse directive options and create an `tagged` node.

        The method delegates most behaviour to `Figure.run` to build the
        figure node, then wraps the image element in a positioned span
        and appends overlay anchors based on the parsed `faces` data.
        The use of percentages ensures responsiveness as the image
        scales.

        The returned node is then placed into the document tree at the
        directive's location. Further processing will convert the node
        into HTML or other formats.

        :return: A list containing a single `node` element.
        """
        self.assert_has_content()
        figure = super().run()
        faces = parse_faces(self.options["faces"])
        if not faces:
            return figure
        try:
            fig = next(n for n in figure if isinstance(n, nodes.Element))
        except StopIteration:
            return figure
        images = list(fig.traverse(nodes.image))
        if not images:
            return figure
        image = images[0]
        node = image
        if isinstance(image.parent, nodes.reference):
            node = image.parent
        parent = node.parent
        try:
            index = parent.children.index(node)
        except ValueError:
            return figure
        start = nodes.raw(
            text=(
                '<span class="face-tag-wrap" style="position:relative;'
                'display:inline-block;line-height:0">'
            ),
            format="html",
        )
        anchors: list[str] = []
        for face in faces:
            label = face["face"].replace('"', "&quot;")
            href = face["link"]
            left, top, width, height = face["coords"]
            style = (
                f"left: {left}px; "
                f"top: {top}px; "
                f"width: {width}px; "
                f"height: {height}px; "
                "position: absolute; "
                "box-sizing: border-box; "
                "border: 1px solid hsl(0, 0%, 0%, 0.2); "
                "border-radius: 0.5rem; "
                "z-index: 2;"
            )
            if href:
                anchors.append(
                    f'<a class="face-tag" href="{href}" '
                    f'title="{label}" aria-label="{label}" '
                    f'style="{style}"></a>'
                )
            else:
                anchors.append(
                    f'<span class="face-tag" '
                    f'title="{label}" aria-label="{label}" '
                    f'style="{style}"></span>'
                )
        end = nodes.raw(text="".join(anchors) + "</span>", format="html")
        parent.insert(index, start)
        parent.insert(index + 2, end)
        return figure


def visit(self: HTMLTranslator, node: node) -> None:
    """Handle entry processing of the `tagged` node during HTML
    generation.

    The directive injects HTML directly in `run`, hence no additional
    processing is required at visit time.

    :param self: The HTML translator instance.
    :param node: The `tagged` node being processed.
    """
    pass


def depart(self: HTMLTranslator, node: node) -> None:
    """Handle exit processing of the `tagged` node during HTML
    generation.

    :param self: The HTML translator instance.
    :param node: The `tagged` node being processed.
    """
    pass
