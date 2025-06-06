"""\
SMART Sphinx Theme Utilities
============================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Friday, February 21 2025
Last updated on: Saturday, March 08 2025

This module defines a collection of utility functions used for
customising the SMART Sphinx Theme. These utilities focus on enhancing
the post-processing of the generated HTML output, as well as providing
additional support for interactive elements, theme options, and other
dynamic behaviors. The functionality provided includes handling
collapsible table of contents (ToC), scrollspy support, removal of
unnecessary elements, and custom event handling for theme-specific
features.

The goal of this module is to ensure that the SMART Sphinx Theme
produces clean, efficient, and interactive HTML documentation by
leveraging Sphinx's internal APIs and dynamic JavaScript bindings.
"""

from __future__ import annotations

import typing as t

import bs4
from docutils import nodes
from sphinx.environment.adapters.toctree import TocTree
from sphinx.util.display import status_iterator
from sphinx.util.docutils import new_document

if t.TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment


def findall(
    node: nodes.Node,
    element: type[nodes.reference] | type[nodes.bullet_list],
) -> t.Any:
    """Recursively search through the given docutils node to find all
    instances of a specified element type.

    This function abstracts the traversal method, ensuring
    compatibility across different versions of docutils. Depending on
    the version, it will either use the `findall` method or the older
    `traverse` method.

    :param node: The starting node from which the search will be
        performed.
    :param element: The type of node element to find, such as references
        or bullet lists.
    :return: An iterable containing all matching elements found within
        the given node.
    """
    findall = "findall" if hasattr(node, "findall") else "traverse"
    return getattr(node, findall)(element)


def make_toc_collapsible(tree: bs4.BeautifulSoup) -> None:
    """Enhance the left sidebar's table of contents (ToC) by making the
    child elements collapsible.

    This function identifies anchor tags within the left sidebar that
    have adjacent unordered lists (`ul`), indicating nested ToC items.
    It then modifies these elements by adding `Alpine.js`-based
    attributes to enable dynamic collapsing and expanding functionality.

    The function also appends a clickable button with an icon to trigger
    the collapse/expand action. This improves navigation by allowing
    users to hide or reveal sections of the ToC as needed.

    :param tree: The parsed HTML tree representing the document
        structure, used for DOM manipulation.
    """
    for link in tree.select("#left-sidebar a"):
        children = link.find_next_sibling("ul")
        if children:
            link.parent["x-data"] = (
                "{ expanded: $el.classList.contains('current') }"
            )
            link["@click"] = "expanded = !expanded"
            link["class"].append("expandable")
            link[":class"] = "{ 'expanded': expanded }"
            children["x-show"] = "expanded"
            button = tree.new_tag(
                "button",
                type="button",
                **{"@click.prevent.stop": "expanded = !expanded"},
            )
            label = tree.new_tag("span", attrs={"class": "sr-only"})
            button.append(label)
            svg = bs4.BeautifulSoup(
                (
                    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 '
                    '24" width="18px" height="18px" stroke="none" '
                    'fill="currentColor"><path d="M10 6L8.59 7.41 13.17 12l-4.'
                    '58 4.59L10 18l6-6z"/></svg>'
                ),
                "html.parser",
            ).svg
            button.append(svg)  # type:ignore[arg-type]
            link.append(button)


def add_scrollspy(tree: bs4.BeautifulSoup) -> None:
    """Implement a scrollspy feature for the right sidebar to highlight
    active sections during scrolling.

    Scrollspy is a visual aid that highlights links in the right sidebar
    corresponding to the current section visible in the viewport. This
    function leverages Alpine.js to track intersections between section
    headers and the viewport, updating the `activeSection` variable to
    reflect which section is currently in view.

    :param tree: The parsed HTML tree, used to attach the necessary
        attributes for scrollspy behavior.
    """
    for link in tree.select("a.headerlink"):
        if link.parent.name in ["h2", "h3"] or (
            link.parent.name == "dt" and "sig" in link.parent.get("class", "")
        ):
            active_link = link["href"]
            link["x-intersect.margin.0%.0%.-70%.0%"] = (
                f"activeSection = '{active_link}'"
            )
        for link in tree.select("#right-sidebar a"):
            active_link = link["href"]
            link[":data-current"] = f"activeSection === '{active_link}'"


def remove_title_from_scrollspy(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, t.Any],
    doctree: nodes.Node,
) -> None:
    """Remove redundant title nodes from the ToC to prevent duplicate
    entries in the scrollspy.

    During Sphinx builds, titles may sometimes appear at both the top
    level of the ToC and nested within their respective sections. This
    function traverses the ToC tree, removing nodes where the `refuri`
    attribute points to `#`, indicating a redundant title entry.

    :param app: The Sphinx application instance.
    :param pagename: The name of the page being processed.
    :param templatename: The name of the HTML template used for
        rendering.
    :param context: Context variables passed to the template.
    :param doctree: The document tree for the current page."""
    toc = TocTree(app.builder.env).get_toc_for(pagename, app.builder)
    for node in findall(toc, nodes.reference):
        if node["refuri"] == "#":
            node.parent.parent.remove(node.parent)
    doc = new_document("<partial node>")
    doc.append(toc)
    for node in findall(doc, nodes.bullet_list):
        if (
            len(node.children) == 1
            and isinstance(node.next_node(), nodes.list_item)
            and isinstance(node.next_node().next_node(), nodes.bullet_list)
        ):
            doc.replace(node, node.next_node().next_node())
    if hasattr(app.builder, "_publisher"):
        app.builder._publisher.set_source(doc)
        app.builder._publisher.publish()
        context["toc"] = app.builder._publisher.writer.parts["fragment"]


def remove_empty_toctree_divs(tree: bs4.BeautifulSoup) -> None:
    """Remove empty `toctree-wrapper` divs from the HTML tree.

    In Sphinx, `toctree-wrapper` divs may be generated even when no
    visible content is present, such as when a toctree is marked as
    `:hidden:`. These empty containers result in unnecessary whitespace
    and redundant elements in the final HTML output.

    This function scans the HTML tree, identifies empty toctree divs
    (those containing only whitespace or line breaks), and removes them
    to maintain a clean and optimised document structure.

    :param tree: Parsed HTML tree representing the document structure.
    """
    for div in tree.select("div.toctree-wrapper"):
        if len(div.contents) == 1 and not div.contents[0].strip():
            div.decompose()


def remove_comments(tree: bs4.BeautifulSoup) -> None:
    """Strip all HTML comments from the parsed HTML tree.

    HTML comments (enclosed in `<!-- -->`) are often used during
    development for debugging or documentation purposes but are not
    needed in the final output. This function iterates through the HTML
    tree and removes all comment nodes, resulting in a cleaner, more
    efficient HTML file.

    :param tree: Parsed HTML tree representing the document structure.
    """
    for comment in tree.find_all(string=lambda c: isinstance(c, bs4.Comment)):
        comment.extract()


def register_website_options(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, t.Any],
    doctree: nodes.Node,
) -> None:
    """Register custom website options and inject them into the Sphinx
    HTML context.

    This function updates the HTML context with any theme-specific
    options stored in the Sphinx application's configuration. The options
    are expected to be defined under the `website_options` key in the
    Sphinx config file (conf.py). These options can control various
    aspects of the theme's dynamic behavior, like enabling scrollspy,
    collapsible toctrees, or copying header links.
    """
    context.update(app.config.website_options)


def add_copy_to_headerlinks(tree: bs4.BeautifulSoup) -> None:
    """Add "copy to clipboard" functionality to header links.

    This function enhances all anchor tags with the `headerlink` class
    by binding a JavaScript event handler that copies the link's URL to
    the clipboard when clicked.

    :param tree: Parsed HTML tree representing the document structure.
    """
    for link in tree.select("a.headerlink"):
        link["@click.prevent"] = (
            "window.navigator.clipboard.writeText($el.href);"
        )
        del link["title"]
        link["aria-label"] = "Copy link"


def open_links_in_new_tab(tree: bs4.BeautifulSoup) -> None:
    """Ensure external links open in a new tab with proper security
    attributes.

    This function modifies all anchor tags marked with the class
    `reference external`, adding `rel="nofollow noopener"` attributes.
    These attributes prevent potential security risks such as reverse
    tabnabbing by ensuring that new tabs cannot manipulate the referring
    page.

    :param tree: Parsed HTML tree representing the document structure.
    """
    for link in tree("a", class_="reference external"):
        link["rel"] = "nofollow noopener"
        link["target"] = "_blank"


def postprocess(html: str, app: Sphinx) -> None:
    """Perform post-processing on an HTML document after the Sphinx
    build.

    This function reads an HTML file, parses it into a BeautifulSoup
    tree, applies various transformations — such as adding collapsible
    navigation, enabling scrollspy, cleaning up empty elements, and
    removing comments — and finally writes the modified content back to
    the file.

    Post-processing ensures that the generated HTML is not only
    functional but also clean, optimised, and dynamic according to the
    user's configuration options.

    :param html: Path to the HTML file to be post-processed.
    :param app: The Sphinx application instance, used to access the
        current build's options and environment.
    """
    with open(html, encoding="utf-8") as f:
        tree = bs4.BeautifulSoup(f, "html.parser")
    open_links_in_new_tab(tree)
    add_copy_to_headerlinks(tree)
    make_toc_collapsible(tree)
    remove_empty_toctree_divs(tree)
    add_scrollspy(tree)
    remove_comments(tree)
    with open(html, "w", encoding="utf-8") as f:
        f.write(str(tree))


def env_before_read_docs(
    app: Sphinx, _: BuildEnvironment, docnames: list[str]
) -> None:
    """Track the list of documents modified during the Sphinx build.

    This function captures the list of document names that have been
    added, updated, or deleted, and stores them in the Sphinx
    environment for later use. This ensures that post-processing only
    affects pages that have actually changed, optimising the build
    process by avoiding unnecessary rework.

    :param app: The Sphinx application instance.
    :param _: The current build environment (unused).
    :param docnames: A list of document names that were modified.
    """
    app.env.theme_htmls = docnames


def build_finished(app: Sphinx, exc: Exception | None) -> None:
    """Post-processes HTML documents after the Sphinx build, applying
    final modifications to the output files.

    This function is triggered after the build process is completed. It
    checks if there are any errors, and if the builder is set to produce
    `HTML` or `dirhtml` output. It then applies final transformations
    to the list of modified documents stored in the environment, such as
    collapsible navigation, and comment removal.

    :param app: Sphinx application object.
    :param exc: Any exception raised during the build process, or None
        if no exceptions occurred.

    Execute post-processing steps after the Sphinx build is complete.

    Once the Sphinx build process concludes — and if no errors occurred
    — this function processes each modified HTML file by applying the
    necessary transformations (collapsible ToCs, link adjustments,
    etc.). Only HTML or directory-style HTML (`dirhtml`) builds are
    considered.

    If an exception occurs during the build, post-processing is skipped
    to avoid further complications.

    :param app: The Sphinx application instance.
    :param exc: An exception raised during the build process, or `None`
        if the build was successful.
    """
    if exc or app.builder.name not in {"html", "dirhtml"}:
        return
    if app.builder is not None and app.builder.name not in ["html", "dirhtml"]:
        return
    htmls = [app.builder.get_outfilename(html) for html in app.env.theme_htmls]
    if not htmls:
        return
    for html in status_iterator(
        htmls,
        "Postprocessing... ",
        "darkgreen",
        len(htmls),
        app.verbosity,
    ):
        postprocess(html, app)
