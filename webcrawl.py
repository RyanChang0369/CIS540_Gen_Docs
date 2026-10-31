"""
webcrawl.py

Authors: rchang
Created: 2026-10-31
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class HtmlSelector:
    kind: Literal["css", "xpath"]
    value: str
    action: Literal["next", "request"]