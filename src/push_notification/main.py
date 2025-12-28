# src/push_notification/main.py
from push_notification.sources.weeronline import WeeronlineNetherlandsReport
from push_notification.notifiers.telegram import TelegramNotifier


def main() -> None:
    src = WeeronlineNetherlandsReport()
    forecast = src.fetch()

    # Check fetched forecast
    print(forecast.headline)
    print(forecast.published_at)
    print(forecast.summary)

    # push forcast notification to Telegram
    msg = (
        f"{forecast.title}\n"
        f"{forecast.headline}\n\n"
        f"{forecast.summary}\n\n"
        f"{forecast.url}"
    )

    TelegramNotifier.from_env().send_message(msg)


if __name__ == "__main__":
    main()