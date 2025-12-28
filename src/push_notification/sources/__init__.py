from push_notification.sources.weeronline import WeeronlineNetherlandsReport
from push_notification.sources.knmi import KNMINetherlandsForecast

SOURCE_REGISTRY = {
    "weeronline": WeeronlineNetherlandsReport,
    "knmi": KNMINetherlandsForecast,
}
