from __future__ import annotations
from push_notification.models import Forecast
import html


class DefaultFormatter:
    def format(self, fc: Forecast) -> str:
        title = html.escape(fc.title)
        headline = html.escape(fc.headline)
        summary = html.escape(fc.summary)
        url = html.escape(fc.url)

        return (
            f"<b>{title}</b>\n"
            f"<i>{headline}</i>\n\n"
            f"{summary}\n\n"
            f'<a href="{url}">Source: {fc.source}</a>'
        )
