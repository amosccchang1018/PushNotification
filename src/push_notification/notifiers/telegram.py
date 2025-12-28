from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import requests


class TelegramConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class TelegramConfig:
    bot_token: str
    chat_id: str  # keep as str (chat ids can be large, and groups are negative)


class TelegramNotifier:
    """
    Sends messages to Telegram via Bot API.
    Required env vars:
      - TG_BOT_TOKEN
      - TG_CHAT_ID
    """

    def __init__(
        self, config: TelegramConfig, session: Optional[requests.Session] = None
    ) -> None:
        self._config = config
        self._session = session or requests.Session()
        self._session.headers.update({"User-Agent": "push-notification-bot/1.0"})

    @staticmethod
    def from_env() -> "TelegramNotifier":
        """
        Load configuration from environment variables.
        """
        bot_token = os.getenv("TG_BOT_TOKEN", "").strip()
        chat_id = os.getenv("TG_CHAT_ID", "").strip()

        if not bot_token:
            raise TelegramConfigError("Missing environment variable: TG_BOT_TOKEN")
        if not chat_id:
            raise TelegramConfigError("Missing environment variable: TG_CHAT_ID")

        return TelegramNotifier(TelegramConfig(bot_token=bot_token, chat_id=chat_id))

    def send_message(
        self,
        text: str,
        *,
        parse_mode: str = "HTML",
        disable_web_page_preview: bool = True,
        reply_to_message_id: Optional[int] = None,
    ) -> None:
        """
        Send a plain text message.

        parse_mode:
          - None (plain)
          - "HTML"
          - "MarkdownV2" (be careful with escaping)
        """
        if not text or not text.strip():
            raise ValueError("Telegram message text is empty.")

        url = f"https://api.telegram.org/bot{self._config.bot_token}/sendMessage"
        payload = {
            "chat_id": self._config.chat_id,
            "text": text,
            "disable_web_page_preview": disable_web_page_preview,
            "parse_mode": parse_mode,
        }
        if parse_mode:
            payload["parse_mode"] = parse_mode
        if reply_to_message_id is not None:
            payload["reply_to_message_id"] = reply_to_message_id

        resp = self._session.post(url, json=payload, timeout=25)

        # Telegram returns JSON even on errors; include it in the exception for debugging.
        if resp.status_code >= 400:
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text
            raise RuntimeError(f"Telegram API error {resp.status_code}: {detail}")

        resp.raise_for_status()
