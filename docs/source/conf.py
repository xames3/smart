"""\
Studying, Mentorship, And Resourceful Teaching Configuration
===========================================================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Saturday, February 22 2025
Last updated on: Wednesday, March 05 2025

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
"""

from __future__ import annotations

import os
import subprocess
import typing as t
from datetime import datetime as dt

from theme import version

project: t.Final[str] = "Home"
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
]
nitpicky: bool = True

try:
    last_updated_cmd = (
        "git",
        "log",
        "--pretty=format:%cd",
        "--date=format:%B %d, %Y",
        "-n1",
    )
    last_updated = f"on {subprocess.check_output(last_updated_cmd).decode()}"
except Exception:
    last_updated = "today"

website_author: t.Final[str] = author
website_copyright: t.Final[str] = f"{dt.now().year}, {website_author}."
website_email: t.Final[str] = author_email
website_github: str = source
website_homepage: str = baseurl
website_license: str = f"{source}/blob/main/LICENSE"
website_repository: str = source
website_title: t.Final[str] = project
website_version: t.Final[str] = version
website_hide_index_toctree: bool = True
website_documentation: str = source
website_options: dict[str, t.Any] = {
    "last_updated": last_updated,
    "add_copy_to_headerlinks": True,
    "open_links_in_new_tab": True,
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
docsearch_placeholder: t.Final[str] = "SMART Search"
docsearch_missing_results_url: str = source + "/issues/new?title=${query}"

copybutton_exclude: str = ".linenos, .gp, .go"
copybutton_line_continuation_character: str = "\\"
copybutton_selector: str = "div:not(.no-copybutton) > div.highlight > pre"
copybutton_image_svg: str = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
width="24" height="24" stroke-width="2">
  <path d="M9 5h-2a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-12a2 2 0
  0 0 -2 -2h-2"></path>
  <path d="M9 3m0 2a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v0a2 2 0 0 1 -2 2h-2a2 2 0 0
  1 -2 -2z"></path>
  <path d="M9 12l.01 0"></path>
  <path d="M13 12l2 0"></path>
  <path d="M9 16l.01 0"></path>
  <path d="M13 16l2 0"></path>
</svg>
"""
