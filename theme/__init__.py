"""\
SMART Sphinx Theme
==================

Author: Akshay Mestry <xa@mes3.dev>
Created on: 21 February, 2025
Last updated on: 20 October, 2025

This module serves as the primary entry point for the SMART Sphinx
Theme. It is responsible for initialising the theme, configuring its
extensions, and integrating with Sphinx's build process. The SMART
Sphinx Theme extends the default Sphinx capabilities by adding::

    - Collapsible toctrees for better navigation.
    - Scrollspy functionality to highlight the active section.
    - Integration with various Sphinx extensions.
    - Post-processing HTML with dynamic options.

This module connects the theme's internal utilities and configurations
with the Sphinx application lifecycle, ensuring seamless interaction
between theme components and the final HTML output.

The SMART Sphinx Theme is registered through the `setup()` function,
which configures the theme, maps user-configurable options, and binds
event hooks for post-processing and dynamic content handling.

.. versionadded:: 21.2.2025

    [1] Added native support for `sphinx.ext-opengraph` extension.

.. versionadded:: 2.3.2025

    [1] Override styles for `sphinx_design` extension by using a
        custom CSS.
    [2] Override styles for `sphinx_docsearch` extension by using a
        custom CSS.

.. versionchanged:: 27.8.2025

    [1] Added support for `tagged` directive to overlay clickable
        face tags on images.
    [2] Added native support for injecting `last_updated` date just above
        the footer.

.. deprecated:: 19.10.2025

    [1] Use of `website_options` in favour of `html_context`. This
        removes the need of `register_website_options` function.
    [2] Custom website options are now replaced by default Sphinx's
        `html_theme_options`.
"""

from __future__ import annotations

import inspect
import os
import typing as t

import docutils.parsers.rst as rst
from sphinx.util import logging

from theme.internal import directives
from theme.internal import roles
from theme.internal.utils import build_finished
from theme.internal.utils import env_before_read_docs
from theme.internal.utils import last_updated_date
from theme.internal.utils import remove_title_from_scrollspy


if t.TYPE_CHECKING:
    import types

    import docutils.nodes as nodes
    from sphinx.application import Sphinx

logger = logging.getLogger(__name__)

version: str = "19.10.2025"
theme_name: t.Final[str] = "smart"
theme_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "base")
supported_extensions: t.Sequence[str] = (
    "sphinx_carousel.carousel",
    "sphinx_design",
    "sphinxext.opengraph",
)


def fix(module: types.ModuleType) -> type[nodes.Element]:
    """Correct the `__name__` attribute of a directive's node class.

    This function updates the `__name__` attribute of a node class
    defined within a directive's module. The `__name__` attribute is
    adjusted by converting hyphenated module names into PascalCase for
    consistency with the node's class naming conventions.

    This is particularly useful when dynamically registering nodes,
    ensuring their names match Sphinx's internal expectations.

    :param module: The module containing the node class.
    :return: The node class with an updated `__name__` attribute.
    """
    node: type[nodes.Element] = module.node
    node.__name__ = "".join(_.capitalize() for _ in module.name.split("-"))
    return node


def setup(app: Sphinx) -> dict[str, str | bool]:
    """Initialise and configure the SMART Sphinx Theme.

    This function serves as the main entry point for integrating the
    SMART Sphinx Theme with the Sphinx application. It performs the
    following tasks::

        [1] Registers the theme's supported extensions.
        [2] Maps standard Sphinx configuration options to the theme's
            internal structure.
        [3] Adds JavaScript and CSS assets to the HTML build.
        [4] Registers custom roles and directives to extend Sphinx's
            default capabilities.
        [5] Binds event hooks for pre-build and post-build processes,
            enabling dynamic content transformations like collapsible
            toctrees and scrollspy.

    :param app: The Sphinx application instance.
    :return: A dictionary indicating the theme's version and its
        compatibility with parallel read and write processes.

    .. deprecated:: 19.10.2025

        Custom website options are now replaced by default Sphinx's
        `html_theme_options`.
    """
    for extension in supported_extensions:
        app.setup_extension(extension)
    app.add_html_theme(theme_name, theme_path)
    app.add_css_file("sphinx-design.css", priority=900)
    app.add_css_file("doc-search.css", priority=900)
    app.add_js_file("theme.js", loading_method="defer")
    app.add_js_file("smart.js", loading_method="defer")
    for role in inspect.getmembers(roles, inspect.isfunction):
        rst.roles.register_local_role(*role)
    for directive in directives:
        app.add_node(fix(directive), html=(directive.visit, directive.depart))
        app.add_directive(directive.name, directive.directive)
        if hasattr(directive, "html_page_context"):
            app.connect("html-page-context", directive.html_page_context)
    app.connect("env-before-read-docs", env_before_read_docs)
    app.connect("source-read", last_updated_date)
    app.connect("html-page-context", remove_title_from_scrollspy)
    app.connect("build-finished", build_finished)
    return {
        "version": version,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
