from typing import Type

from src.messengers.providers.telegram import TelegramMessenger


class MessengerFactory:
    SUPPORTED_MESSENGERS = {"telegram": TelegramMessenger}
    _messengers = {}

    @classmethod
    def get_or_create_messenger(cls: Type["MessengerFactory"], name: str):
        name = name.lower()
        if name not in cls.SUPPORTED_MESSENGERS:
            raise ValueError(f"Messenger {name} is not supported")

        messenger = cls._messengers.get(name)
        if not messenger:
            messenger = cls.SUPPORTED_MESSENGERS[name]
            cls._messengers[name] = messenger

        return messenger
