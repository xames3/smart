"""\
Studying, Mentorship, And Resourceful Teaching Configuration
===========================================================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Saturday, February 22 2025
Last updated on: Monday, February 24 2025

This file contains the configuration settings for building SMART,
Study, Mentorship, And Resourceful Teaching website using Sphinx, a
popular Python documentation tool. Sphinx is a powerful documentation
generator that makes it easy to create high quality technical
documentation for technical projects. I, however will be using it as
teaching and learning platform.
"""

from __future__ import annotations

import subprocess
import typing as t
from datetime import datetime as dt

from theme import version

project: t.Final[str] = "Home"
author: t.Final[str] = "Akshay Mestry"
author_email: t.Final[str] = "xa@mes3.dev"
baseurl: t.Final[str] = "https://xames3.github.io/"
homepage: str = f"{baseurl}/smart/"
source: t.Final[str] = "https://github.com/xames3/smart"

extensions: list[str] = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx.ext.viewcode",
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
    last_updated = subprocess.check_output(last_updated_cmd).decode()
except Exception:
    last_updated = "Today"

website_author: t.Final[str] = author
website_copyright: t.Final[str] = f"{dt.now().year}, {website_author}."
website_email: t.Final[str] = author_email
website_github: str = source
website_license: str = f"{source}/blob/main/LICENSE"
website_repository: str = source
website_title: t.Final[str] = project
website_version: t.Final[str] = version
website_hide_index_toctree: bool = True
website_homepage: str = homepage
website_documentation: str = website_homepage
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
html_context: dict[str, str] = {}
rst_epilog = ""
with open("_static/extra/epilog.rst") as f:
    rst_epilog += f.read()
intersphinx_mapping: dict[str, tuple[str, t.Any]] = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
