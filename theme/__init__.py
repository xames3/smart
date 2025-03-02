"""\
SMART Sphinx Theme
==================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Friday, February 21 2025
Last updated on: Sunday, March 02 2025

This module serves as the primary entry point for the SMART Sphinx
Theme. It is responsible for initializing the theme, configuring its
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
"""

from __future__ import annotations

import inspect
import os
import types
import typing as t

import docutils.parsers.rst as rst
from sphinx.util import logging

from theme.internal import directives
from theme.internal import roles
from theme.internal.utils import build_finished
from theme.internal.utils import env_before_read_docs
from theme.internal.utils import register_website_options
from theme.internal.utils import remove_title_from_scrollspy

if t.TYPE_CHECKING:
    import docutils.nodes as nodes
    from sphinx.application import Sphinx

logger = logging.getLogger(__name__)

version: str = "21.2.2025"
theme_name: t.Final[str] = "smart"
theme_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "base")
supported_extensions: t.Sequence[str] = (
    "sphinx_carousel.carousel",
    "sphinx_design",
    "sphinxext.opengraph",
)
theme_mapping: dict[str, str] = {
    "html_baseurl": "website_url",
    "html_favicon": "website_favicon",
    "html_logo": "website_logo",
    "copyright": "website_copyright",
    "html_permalinks_icon": "website_permalinks_icon",
    "html_theme_options": "website_options",
    "html_title": "website_title",
}


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
    """Initialize and configure the SMART Sphinx Theme.

    This function serves as the main entry point for integrating the
    SMART Sphinx Theme with the Sphinx application. It performs the
    following tasks::

        [1] Registers the theme's supported extensions.
        [2] Defines user-configurable options for the theme.
        [3] Maps standard Sphinx configuration options to the theme's
            internal structure.
        [4] Adds JavaScript and CSS assets to the HTML build.
        [5] Registers custom roles and directives to extend Sphinx's
            default capabilities.
        [6] Binds event hooks for pre-build and post-build processes,
            enabling dynamic content transformations like collapsible
            toctrees and scrollspy.

    :param app: The Sphinx application instance.
    :return: A dictionary indicating the theme's version and its
        compatibility with parallel read and write processes.
    """
    for extension in supported_extensions:
        app.setup_extension(extension)
    config = app.config
    configurations: dict[str, tuple[t.Any, ...]] = {
        "website_author": (config.author, tuple),
        "website_copyright": (config.copyright, str),
        "website_email": ("", str),
        "website_favicon": ("", str),
        "website_github": ("", str),
        "website_homepage": ("", str),
        "website_license": ("", str),
        "website_logo": ("", str),
        "website_options": (config.html_theme_options, dict),
        "website_permalinks_icon": ("", str),
        "website_repository": ("", str),
        "website_title": (config.html_title or config.project, tuple),
        "website_url": (config.html_baseurl, str),
        "website_version": (config.release, str),
    }
    for configuration, (default, dtype) in configurations.items():
        app.add_config_value(configuration, default, "html", dtype)
    for default_name, new_name in theme_mapping.items():
        setattr(config, default_name, getattr(config, new_name))
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
    app.connect("html-page-context", register_website_options)
    app.connect("html-page-context", remove_title_from_scrollspy)
    app.connect("build-finished", build_finished)
    return {
        "version": version,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
