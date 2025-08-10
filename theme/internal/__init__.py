"""\
SMART Sphinx Theme Extension Manager
====================================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Saturday, 22 February 2025
Last updated on: Saturday, 9 August 2025

This module manages SMART Sphinx Theme's custom directive and roles.
"""

from __future__ import annotations

import types
import typing as t

from . import author
from . import tagged
from . import video
from . import youtube

directives: t.Sequence[types.ModuleType] = (
    author,
    tagged,
    video,
    youtube,
)
