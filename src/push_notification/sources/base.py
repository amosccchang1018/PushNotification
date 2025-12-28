# src/push_notification/sources/base.py
from abc import ABC, abstractmethod
from push_notification.models import Forecast


class BaseSource(ABC):
    @abstractmethod
    def fetch(self) -> Forecast:
        """Fetch and parse a Forecast from a source."""
        raise NotImplementedError
