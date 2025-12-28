from __future__ import annotations

from datetime import datetime
from typing import Optional

from playwright.sync_api import sync_playwright, TimeoutError as PwTimeoutError

from push_notification.models import Forecast


class WeeronlineNetherlandsReport:
    NAME = "weeronline"
    URL = "https://www.weeronline.nl/weerbericht-nederland"

    def fetch(self) -> Forecast:
        title = "Weerbericht Nederland"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                locale="nl-NL",
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )
            page = context.new_page()

            try:
                page.goto(self.URL, wait_until="domcontentloaded", timeout=30_000)
                page.wait_for_timeout(1200)
            except PwTimeoutError:
                browser.close()
                raise RuntimeError("Weeronline: page load timeout.")

            container = page.locator("main, article").first
            if container.count() == 0:
                container = page.locator("body")

            h2 = container.locator("h2").first
            headline = h2.inner_text().strip() if h2.count() else ""

            p1 = container.locator("p").first
            summary = p1.inner_text().strip() if p1.count() else ""

            published_at = self._try_extract_datetime(container)

            browser.close()

        if not headline:
            raise RuntimeError("Weeronline: cannot find headline (h2).")
        if not summary:
            raise RuntimeError("Weeronline: cannot find summary paragraph (p).")

        return Forecast(
            source=self.NAME,
            url=self.URL,
            title=title,
            headline=headline,
            published_at=published_at,
            summary=summary,
        )

    def _try_extract_datetime(self, container) -> Optional[datetime]:
        try:
            text = container.inner_text(timeout=2000)
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
            for ln in lines[:30]:
                if "," in ln and ":" in ln and any(ch.isdigit() for ch in ln):
                    return None
        except Exception:
            return None
        return None
