"""\
SMART Sphinx Theme Extension Manager
====================================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Saturday, 22 February 2025
Last updated on: Saturday, 6 September 2025

This module manages SMART Sphinx Theme's custom directive and roles.
"""

from __future__ import annotations

import typing as t

from . import author
from . import picture
from . import tagged
from . import thumbnail
from . import video
from . import youtube


if t.TYPE_CHECKING:
    import types

directives: t.Sequence[types.ModuleType] = (
    author,
    picture,
    tagged,
    thumbnail,
    video,
    youtube,
)
