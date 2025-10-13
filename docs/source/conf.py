"""\
Studying, Mentorship, And Resourceful Teaching Configuration
===========================================================

Author: Akshay Mestry <xa@mes3.dev>
Created on: 22 February, 2025
Last updated on: 13 October, 2025

This file contains the configuration settings for building SMART,
Study, Mentorship, And Resourceful Teaching website using Sphinx, a
popular Python documentation tool. Sphinx is a powerful documentation
generator that makes it easy to create high quality technical
documentation for technical projects. I, however will be using it as
teaching and learning platform.

.. versionadded:: 22.2.2025

    [1] Added support for Algolia DocSearch instead of using standard
        Sphinx search. This support is added through the
        `sphinx_docsearch` extension.

.. versionadded:: 1.3.2025

    [1] Added support for copy button. For some reason, the default copy
        button doesn't seem to work. Hence, relying on external sphinx
        extension. This support is added through the `sphinx_copybutton`
        extension.

.. versionchanged:: 5.3.2025

    [1] Customized the CSS of the copy button extension and fixed a bug
        caused by default copy button element.

.. versionchanged:: 19.4.2025

    [1] Added support for PyTorch docs via InterSphinx mappings.

.. deprecated:: 8.8.2025

    [1] Copybutton SVG icon has been replaced with `FontAwesome` icon.
    [2] The `show_sphinx` and `last_updated` options are disabled now.

.. versionchanged:: 8.8.2025

    [1] The website `copyright` is updated to enforce minimalism.

.. versionadded:: 22.8.2025

    [1] Added support for `sphinx-notfound-page` extension to handle the
        404 pages. This extension is used to provide a better user
        experience when a page is not found.

.. versionchanged:: 27.8.2025

    [1] Configured `linkcheck` builder to ignore localhost links.
    [2] Added support for showing the last updated date just above the
        footer. This is done using the `website_options` configuration
        option `last_updated_body`.
    [3] Show the "Built with Sphinx" footer note by enabling the
        `show_sphinx` option in `website_options`.
    [4] Added support for `sponsor` button in the right sidebar.
"""

from __future__ import annotations

import os
import typing as t
from datetime import datetime as dt

from markupsafe import Markup

from theme import version


project: t.Final[str] = "MES"
author: t.Final[str] = "Akshay Mestry"
author_email: t.Final[str] = "xa@mes3.dev"
baseurl: t.Final[str] = "https://smart.mes3.dev/"
source: t.Final[str] = "https://github.com/xames3/smart"

extensions: list[str] = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_docsearch",
    "notfound.extension",
]
nitpicky: bool = True

website_author: t.Final[str] = author
website_copyright: t.Final[str] = f"{website_author} © {dt.now().year}"
website_email: t.Final[str] = author_email
website_github: str = source
website_homepage: str = baseurl
website_license: str = f"{source}/blob/main/LICENSE"
website_repository: str = source
website_title: t.Final[str] = project
website_version: t.Final[str] = version
website_hide_index_toctree: bool = True
website_documentation: str = source
website_favicon: str = "_static/favicon.ico"

website_options: dict[str, t.Any] = {
    "add_copy_to_headerlinks": True,
    "open_links_in_new_tab": True,
    "show_sphinx": False,
    "extra_header_links": {
        "Sponsor on GitHub": {
            "link": "https://github.com/sponsors/xames3",
            "icon": Markup(
                "<i class='fa-regular fa-heart' aria-hidden='true'></i>"
            ),
        },
    },
}

html_theme: t.Final[str] = "smart"
html_static_path: list[str] = ["_static"]
exclude_patterns: list[str] = ["_build"]
templates_path: list[str] = ["_templates"]
locale_dirs: list[str] = ["../locale/"]
gettext_compact: bool = False
html_context: dict[str, t.Any] = {
    "docsearch": True,
}
rst_epilog = ""
with open("_static/extra/epilog.rst") as f:
    rst_epilog += f.read()
intersphinx_mapping: dict[str, tuple[str, t.Any]] = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "torch": ("https://pytorch.org/docs/stable/", None),
}

ogp_site_name: t.Final[str] = "Studying, Mentorship, And Resourceful Teaching"
ogp_site_url: t.Final[str] = website_homepage
ogp_social_cards: dict[str, str | bool] = {
    "site_url": website_homepage,
    "enable": False,
}
ogp_type: t.Final[str] = "website"
ogp_enable_meta_description: bool = True

docsearch_app_id: str = os.getenv("DOCSEARCH_APP_ID", "")
docsearch_api_key: str = os.getenv("DOCSEARCH_API_KEY", "")
docsearch_index_name: str = os.getenv("DOCSEARCH_INDEX_NAME", "")
docsearch_container: t.Final[str] = "#smart-search"
docsearch_placeholder: t.Final[str] = "Search"
docsearch_missing_results_url: str = source + "/issues/new?title=${query}"

copybutton_exclude: str = ".linenos, .gp, .go"
copybutton_line_continuation_character: str = "\\"
copybutton_selector: str = "div:not(.no-copybutton) > div.highlight > pre"

linkcheck_ignore: list[str] = [r"https://localhost:\d+/"]
linkcheck_timeout: int = 10
linkcheck_retries: int = 2
