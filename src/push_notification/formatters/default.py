from __future__ import annotations
from push_notification.models import Forecast


class DefaultFormatter:
    def format(self, fc: Forecast) -> str:
        parts = [
            f"{fc.title}",
            f"{fc.headline}",
            "",
            fc.summary,
            "",
            fc.url,
        ]
        return "\n".join([p for p in parts if p is not None])
