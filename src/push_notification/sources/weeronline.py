# src/push_notification/sources/weeronline.py
from __future__ import annotations

import re
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

from push_notification.models import Forecast


_DATETIME_RE = re.compile(
    r"\b(\d{1,2}\s+\w+\s+\d{4}),\s+(\d{2}:\d{2})\b", re.IGNORECASE
)


class WeeronlineNetherlandsReport:
    NAME = "weeronline"
    URL = "https://www.weeronline.nl/weerbericht-nederland"

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self._session = session or requests.Session()
        self._session.headers.update(
            {
                "User-Agent": "push-notification-bot/1.0",
            }
        )

    def fetch(self) -> Forecast:
        html = self._get_html(self.URL)
        soup = BeautifulSoup(html, "lxml")

        title = "Weerbericht Nederland"

        h2 = soup.find("h2")
        if not h2:
            raise RuntimeError("Weeronline: cannot find first <h2> headline.")
        headline = h2.get_text(" ", strip=True)

        published_at = self._find_published_at_after(h2)
        summary = self._find_first_paragraph_after(h2)

        if not summary:
            raise RuntimeError("Weeronline: cannot find first forecast paragraph.")

        return Forecast(
            source=self.NAME,
            url=self.URL,
            title=title,
            headline=headline,
            published_at=published_at,
            summary=summary,
        )

    def _get_html(self, url: str) -> str:
        resp = self._session.get(url, timeout=25)
        resp.raise_for_status()
        return resp.text

    def _find_published_at_after(self, anchor: Tag) -> Optional[datetime]:
        # Walk forward through siblings and try to parse something like:
        # "24 december 2025, 11:45" (as seen on the page) :contentReference[oaicite:2]{index=2}
        for node in anchor.next_elements:
            if isinstance(node, Tag) and node.name in ("h2", "h3"):
                # stop if a new heading appears before we find a datetime
                if node is not anchor:
                    break
            if isinstance(node, (NavigableString, Tag)):
                text = (
                    node.get_text(" ", strip=True)
                    if isinstance(node, Tag)
                    else str(node).strip()
                )
                if not text:
                    continue
                m = _DATETIME_RE.search(text)
                if m:
                    # Dutch month names parsing: keep simple; treat as raw string if needed
                    # For now, return None if parsing fails safely.
                    try:
                        # Attempt parsing with a tolerant approach:
                        return datetime.strptime(
                            f"{m.group(1)} {m.group(2)}", "%d %B %Y %H:%M"
                        )
                    except Exception:
                        return None
        return None

    def _find_first_paragraph_after(self, anchor: Tag) -> str:
        # Collect the first meaningful paragraph until the next h2 appears.
        chunks: list[str] = []

        for node in anchor.next_elements:
            if isinstance(node, Tag) and node.name == "h2" and node is not anchor:
                break  # next section starts
            if isinstance(node, Tag) and node.name in ("p",):
                text = node.get_text(" ", strip=True)
                if text:
                    chunks.append(text)
                    break

        # Fallback: sometimes content is plain text nodes (site-dependent)
        if not chunks:
            for node in anchor.next_elements:
                if isinstance(node, Tag) and node.name == "h2" and node is not anchor:
                    break
                if isinstance(node, NavigableString):
                    t = str(node).strip()
                    if len(t) >= 40:  # heuristic for "real paragraph"
                        chunks.append(t)
                        break

        return chunks[0] if chunks else ""
