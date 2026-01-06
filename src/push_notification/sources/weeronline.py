from __future__ import annotations

from datetime import datetime
from typing import Optional

from playwright.sync_api import sync_playwright, TimeoutError as PwTimeoutError

from push_notification.models import Forecast
from push_notification.sources.base import BaseSource


class WeeronlineNetherlandsReport(BaseSource):
    def __init__(self, *, url: str) -> None:
        super().__init__(name="weeronline", url=url)

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
                page.goto(self.url, wait_until="domcontentloaded", timeout=30_000)
                page.wait_for_timeout(1200)
            except PwTimeoutError:
                browser.close()
                raise RuntimeError("Weeronline: page load timeout.")

            container = page.locator("main, article").first
            if container.count() == 0:
                container = page.locator("body")

            headline = self._first_text(container, ["h1", "h2"]) or ""
            published_at = self._try_extract_datetime(container)

            lead = self._extract_lead_paragraph(container)
            morgen_block = self._extract_morgen_section(container)

            browser.close()

        if not headline:
            raise RuntimeError("Weeronline: cannot find headline (h1/h2).")
        if not lead:
            raise RuntimeError("Weeronline: cannot find lead paragraph.")

        summary = lead
        if morgen_block:
            summary = f"{lead}\n\n{morgen_block}"

        # hard cap for Telegram readability
        summary = self._cap(summary, 1200)

        return Forecast(
            source=self.name,
            url=self.url,
            title=title,
            headline=headline,
            published_at=published_at,
            summary=summary,
        )

    # ---------------- helpers ----------------

    def _first_text(self, container, selectors: list[str]) -> str:
        for sel in selectors:
            el = container.locator(sel).first
            if el.count():
                txt = el.inner_text().strip()
                if txt:
                    return txt
        return ""

    def _extract_lead_paragraph(self, container) -> str:
        """
        Grab the very first meaningful paragraph of the report (the top overview).
        """
        ps = container.locator("p")
        for i in range(min(ps.count(), 8)):
            txt = ps.nth(i).inner_text().strip()
            if not txt:
                continue
            low = txt.lower()
            # defensive skips
            if "cookie" in low or low.startswith("bekijk") or low.startswith("lees"):
                continue
            return txt
        return ""

    def _extract_morgen_section(self, container) -> str:
        """
        Find the first section heading that contains 'Morgen' and return:
          "<heading>\n<first paragraph after heading>"
        Stop before the next heading to avoid long details.
        """
        # Weeronline tends to use h2/h3 for section titles.
        headings = container.locator("h2, h3")
        n = headings.count()
        if n == 0:
            return ""

        for i in range(n):
            h = headings.nth(i)
            h_txt = (h.inner_text() or "").strip()
            if not h_txt:
                continue

            if "morgen" not in h_txt.lower():
                continue

            # From the heading element, walk forward to capture paragraph(s)
            block_parts: list[str] = [h_txt]

            # Use DOM traversal: collect following sibling paragraphs until next heading
            # Playwright doesn't have direct "nextSibling" API, so we use XPath from the heading node.
            # Grab first 2 paragraphs max to avoid length.
            paras = h.locator(
                "xpath=following::p[preceding::h2[1]=self::h2 or preceding::h3[1]=self::h3]"
            )
            # The XPath above can be finicky across layouts. We'll do a simpler, robust approach:
            # Take the first paragraph after the heading in document order.
            p1 = h.locator("xpath=following::p[1]").first
            if p1.count():
                p_txt = p1.inner_text().strip()
                if p_txt:
                    block_parts.append(p_txt)

            # Optional: take second paragraph ONLY if it is still part of the Morgen section
            # and not already a new subheading section (best-effort guard by proximity).
            p2 = h.locator("xpath=following::p[2]").first
            next_heading = h.locator("xpath=following::h2[1] | following::h3[1]").first

            if p2.count() and next_heading.count():
                try:
                    # If the second paragraph appears before the next heading in the DOM, include it.
                    # Compare bounding boxes as a heuristic.
                    p2_box = p2.bounding_box()
                    nh_box = next_heading.bounding_box()
                    if p2_box and nh_box and p2_box["y"] < nh_box["y"]:
                        p2_txt = p2.inner_text().strip()
                        if p2_txt:
                            block_parts.append(p2_txt)
                except Exception:
                    pass

            return "\n".join(block_parts).strip()

        return ""

    def _cap(self, text: str, max_chars: int) -> str:
        text = text.strip()
        if len(text) <= max_chars:
            return text
        return text[:max_chars].rstrip() + "…"

    def _try_extract_datetime(self, container) -> Optional[datetime]:
        # You can implement Dutch datetime parsing later if you want.
        return None
