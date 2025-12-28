# src/push_notification/models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Forecast:
    source: str  # e.g. "weeronline"
    url: str
    title: str  # e.g. "Weerbericht Nederland"
    headline: str  # e.g. "Veel zon en een koude wind"
    published_at: Optional[datetime]
    summary: str  # first paragraph you want
