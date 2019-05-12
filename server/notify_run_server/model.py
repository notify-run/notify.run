from abc import ABC, abstractmethod
from random import choice
from typing import List

from notify_run_server.params import CHANNEL_ID_CHARS, CHANNEL_ID_LENGTH


class NoSuchChannel(Exception):
    def __init__(self, channel_id):
        super(NoSuchChannel, self).__init__()
        self.channel_id = channel_id


def generate_channel_id():
    return ''.join(choice(CHANNEL_ID_CHARS)
                   for _ in range(CHANNEL_ID_LENGTH))


class NotifyModel(ABC):
    @abstractmethod
    def register_channel(self, meta: dict) -> str:
        pass

    @abstractmethod
    def add_subscription(self, channel_id: str, subscription: dict):
        pass

    @abstractmethod
    def get_channel(self, channel_id: str):
        pass

    @abstractmethod
    def get_messages(self, channel_id: str) -> List[dict]:
        pass

    @abstractmethod
    def put_message(self, channel_id: str, message: str, data: dict, result: list):
        pass
