"""\
SMART Sphinx Theme Picture Directive
====================================

picture: Akshay Mestry <xa@mes3.dev>
Created on: Tuesday, 2 September 2025
Last updated on: Wednesday, 3 September 2025

This module defines a custom `picture` directive for the SMART Sphinx
Theme. The directive allows a theme specific picture (image or figure) on
their documentation.

The `picture` directive is designed to extend reStructuredText (rST)
capabilities by injecting structured metadata about the colour scheme,
which can be styled or processed further using Jinja2 templates.

The `picture` directive can be used in reStructuredText documents as
follows::

    .. code-block:: rst

        .. picture:: ../assets/docker-internals
            :alt: Docker Internals

The above snippet will be processed and rendered according to the
theme's Jinja2 template, producing a theme specific picture in the final
HTML output.

.. note::

    This directive is exclusive to the SMART Sphinx Theme. If you
    switch to a different theme, the behavior or availability of this
    directive may change. Please refer to the specific theme's
    documentation for further information.
"""

from __future__ import annotations

import os
import os.path as p
import re
import shutil
import typing as t

import docutils.nodes as nodes
import jinja2
from docutils.parsers.rst.directives import images


if t.TYPE_CHECKING:
    from sphinx.writers.html import HTMLTranslator

name: t.Final[str] = "picture"
here: str = p.dirname(__file__)
html = p.join(p.abspath(p.join(here, "../base")), "picture.html.jinja")

relpath_re: t.Pattern[str] = re.compile(r"^(\.|\/)*")

with open(html) as f:
    template = jinja2.Template(f.read())

id_counter: int = 0


class node(nodes.Element):
    """Container node storing resolved light/dark image variant URIs."""


class directive(images.Figure):
    """Custom `picture` directive for reStructuredText.

    This class extends the standard `Figure` directive to provide
    theming-aware images that switch based on the current colour scheme.
    It inherits all the standard figure functionality while adding
    theme-specific image handling.
    """

    def run(self) -> list[nodes.Node]:
        """Parse directive options and create an `picture` node.

        This method processes the image path prefix provided as an
        argument and combines it with the directive options to create
        a theming-aware picture element.

        The directive expects a path prefix that will be combined with
        'light' and 'dark' suffixes to create the final image paths.

        :return: A list containing a single `node` element.
        """
        env = self.state.document.settings.env
        app = env.app
        doc_dir = p.dirname(env.doc2path(env.docname))
        build_dir = app.builder.outdir
        source_dir = env.srcdir
        content = self.arguments[0].strip()
        if content.startswith("/"):
            content = content.lstrip("/")
        if not p.isabs(content):
            candidate = p.normpath(p.join(doc_dir, content))
        else:
            candidate = content
        base, ext = p.splitext(candidate)
        if ext == "":
            ext = ".svg"
        for suffix in ("-light", "-dark"):
            base = base.removesuffix(suffix)
        light_src_rel = f"{base}-light{ext}"
        dark_src_rel = f"{base}-dark{ext}"
        light_src_abs = p.normpath(p.join(source_dir, light_src_rel))
        dark_src_abs = p.normpath(p.join(source_dir, dark_src_rel))
        missing: list[str] = []
        if not p.exists(light_src_abs):
            missing.append(light_src_rel)
        if not p.exists(dark_src_abs):
            missing.append(dark_src_rel)
        if missing:
            raise self.error(
                "picture directive could not find required "
                f"variant(s): {', '.join(missing)}"
            )
        env.note_dependency(light_src_abs)
        env.note_dependency(dark_src_abs)
        images_out_dir = p.join(build_dir, "_images")
        os.makedirs(images_out_dir, exist_ok=True)
        light_name = p.basename(light_src_rel)
        dark_name = p.basename(dark_src_rel)
        light_dest = p.join(images_out_dir, light_name)
        dark_dest = p.join(images_out_dir, dark_name)

        def _copy(src: str, dest: str) -> None:
            """Copy the source image to the destination if it doesn't
            already exist or is outdated.
            """
            try:
                if (
                    not p.exists(dest)
                    or os.stat(src).st_mtime > os.stat(dest).st_mtime
                ):
                    shutil.copy2(src, dest)
            except OSError as exc:
                raise self.error(
                    f"Failed to copy {src!r} to {dest!r}: {exc}"
                ) from exc

        _copy(light_src_abs, light_dest)
        _copy(dark_src_abs, dark_dest)
        depth = env.docname.count("/")
        rel_prefix = "../" * depth if depth else ""
        attributes = {
            "light": f"{rel_prefix}_images/{light_name}",
            "dark": f"{rel_prefix}_images/{dark_name}",
            "alt": self.options.get("alt", ""),
            "width": self.options.get("width", ""),
            "height": self.options.get("height", ""),
            "align": self.options.get("align", ""),
            "figclass": self.options.get("figclass", ""),
            "caption": "\n".join(self.content) if self.content else "",
            "pid": self._next_id(),
        }
        element = node("", **attributes)
        return [element]

    @staticmethod
    def _next_id() -> str:
        """Generate a unique ID for each `picture` node instance."""
        global id_counter
        id_counter += 1
        return f"tp-{id_counter}"


def visit(self: HTMLTranslator, node: node) -> None:
    """Handle the entry processing of the `picture` node during HTML
    generation.

    This method is called when the HTML translator encounters the
    `picture` node in the document tree. It retrieves the relevant
    attributes from the node and uses Jinja2 templating to produce the
    final HTML output.

    :param self: The HTML translator instance responsible for rendering
        nodes into HTML.
    :param node: The `picture` node containing parsed attributes.
    """
    self.body.append(template.render(**node.attributes))


def depart(self: HTMLTranslator, node: node) -> None:
    """Handle the exit processing of the `picture` node during HTML
    generation.

    This method is invoked after the node's HTML representation has been
    fully processed and added to the output. Since the `picture` node
    does not require any closing actions, the method currently acts as a
    placeholder.

    :param self: The HTML translator instance.
    :param node: The `picture` node being processed.
    """
