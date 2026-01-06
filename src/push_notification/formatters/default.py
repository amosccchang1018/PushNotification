from __future__ import annotations

import html
from push_notification.models import Forecast


class DefaultFormatter:
    def format(self, fc: Forecast) -> str:
        title = html.escape(fc.title)
        headline = html.escape(fc.headline)
        url = html.escape(fc.url)
        source = html.escape(fc.source)

        # Split summary into sections (by blank line)
        raw = (fc.summary or "").strip()
        parts = [p.strip() for p in raw.split("\n\n") if p.strip()]

        overview = html.escape(parts[0]) if parts else ""
        extra = "\n\n".join(parts[1:]) if len(parts) > 1 else ""
        extra = html.escape(extra) if extra else ""

        lines: list[str] = []
        lines.append(f"<b>{title}</b>")
        lines.append(f"<i>{headline}</i>")
        lines.append("")  # blank line

        if overview:
            lines.append("<b>Overview</b>")
            lines.append(overview)

        if extra:
            lines.append("")
            lines.append("────────────")
            lines.append("<b>Tomorrow</b>")
            lines.append(extra)

        lines.append("")
        lines.append(f'<a href="{url}">Source: {source}</a>')

        return "\n".join(lines).strip()
