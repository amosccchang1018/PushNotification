# src/push_notification/sources/base.py
from abc import ABC, abstractmethod
from push_notification.models import Forecast


class BaseSource(ABC):
    def __init__(self, *, name: str, url: str) -> None:
        self.name = name
        self.url = url

    @abstractmethod
    def fetch(self) -> Forecast:
        raise NotImplementedError
