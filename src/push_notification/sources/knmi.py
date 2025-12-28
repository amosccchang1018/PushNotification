from __future__ import annotations

from datetime import datetime
from typing import Optional

from playwright.sync_api import sync_playwright, TimeoutError as PwTimeoutError

from push_notification.models import Forecast
from push_notification.sources.base import BaseSource


class KNMINetherlandsForecast(BaseSource):
    def __init__(self, *, url: str) -> None:
        super().__init__(name="knmi", url=url)

    def fetch(self) -> Forecast:
        title = "KNMI Verwachtingen"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(locale="nl-NL")
            page = context.new_page()

            try:
                page.goto(self.url, wait_until="domcontentloaded", timeout=30_000)
                page.wait_for_timeout(1200)
            except PwTimeoutError:
                browser.close()
                raise RuntimeError("KNMI: page load timeout.")

            anchor = page.get_by_text("Lees het hele weerbericht", exact=False).first
            if anchor.count() == 0:
                browser.close()
                raise RuntimeError(
                    "KNMI: cannot find 'Lees het hele weerbericht' anchor."
                )

            container = anchor.locator(
                "xpath=ancestor-or-self::section[1] | ancestor-or-self::article[1] | ancestor-or-self::div[1]"
            ).first
            if container.count() == 0:
                container = page.locator("main").first
            if container.count() == 0:
                container = page.locator("body")

            headline = ""
            for sel in ("h2", "h3"):
                h = container.locator(sel).first
                if h.count():
                    headline = h.inner_text().strip()
                    break
            if not headline:
                headline = "Vandaag & morgen"

            summary = self._extract_summary_before_anchor(container, anchor)

            browser.close()

        if not summary:
            raise RuntimeError(
                "KNMI: cannot extract summary before 'Lees het hele weerbericht'."
            )

        return Forecast(
            source=self.name,
            url=self.url,
            title=title,
            headline=headline,
            published_at=None,
            summary=summary,
        )

    def _extract_summary_before_anchor(self, container, anchor) -> str:
        """
        Strategy:
        - Get full container inner_text
        - Get anchor inner_text index position
        - Take text before anchor label
        - Clean and keep only relevant top portion
        """
        text = container.inner_text(timeout=3000)
        marker = anchor.inner_text(timeout=2000).strip() or "Lees het hele weerbericht"

        idx = text.find(marker)
        if idx == -1:
            return ""

        before = text[:idx].strip()

        before = before[:1200].strip()

        lines = [ln.strip() for ln in before.splitlines()]
        lines = [ln for ln in lines if ln]
        return "\n".join(lines)
