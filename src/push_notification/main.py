# src/push_notification/main.py
from push_notification.sources.weeronline import WeeronlineNetherlandsReport


def main() -> None:
    src = WeeronlineNetherlandsReport()
    forecast = src.fetch()

    print(forecast.headline)
    print(forecast.published_at)
    print(forecast.summary)


if __name__ == "__main__":
    main()
