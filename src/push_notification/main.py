# src/push_notification/main.py
from push_notification.sources.weeronline import WeeronlineNetherlandsReport
from push_notification.notifiers.telegram import TelegramNotifier
from push_notification.sources.knmi import KNMINetherlandsForecast
from push_notification.formatters.default import DefaultFormatter
from push_notification.config import load_sources_config
from push_notification.sources import SOURCE_REGISTRY

CONFIG_PATH = "configs/sources.yaml"


def main() -> None:
    sources_cfg = load_sources_config(CONFIG_PATH)

    formatter = DefaultFormatter()
    notifier = TelegramNotifier.from_env()

    messages: list[str] = []

    for cfg in sources_cfg:
        if not cfg.get("enabled", False):
            continue

        name = cfg["name"]
        url = cfg["url"]

        if name not in SOURCE_REGISTRY:
            raise RuntimeError(f"Unknown source: {name}")

        source_cls = SOURCE_REGISTRY[name]
        source = source_cls(url=url)

        forecast = source.fetch()
        messages.append(formatter.format(forecast))

    if not messages:
        return

    separator = "\n\n" + ("-" * 20) + "\n\n"
    notifier.send_message(separator.join(messages))


if __name__ == "__main__":
    main()
