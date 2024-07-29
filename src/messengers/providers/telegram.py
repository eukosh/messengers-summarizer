import datetime
import os
from typing import List, Union

from telethon import TelegramClient

from src.messengers.base_messenger import BaseMessenger

TG_APP_ID = os.environ["TG_APP_ID"]
TG_API_HASH = os.environ["TG_API_HASH"]


class TelegramMessenger(BaseMessenger):
    def __init__(self):
        self.client = TelegramClient("anon", TG_APP_ID, TG_API_HASH)

    def run_with_client(func: callable):
        def wrapper(self, *args, **kwargs):
            with self.client as client:
                print("Running with client")
                return client.loop.run_until_complete(func(self, *args, **kwargs))

        return wrapper

    @run_with_client
    async def print_channel_ids(self, channel_name: Union[str, List[str]]):
        async for dialog in self.client.iter_dialogs():
            match channel_name:
                case str():
                    if dialog.name == channel_name:
                        print(dialog.name, "has ID", dialog.id)
                case list():
                    if dialog.name in channel_name:
                        print(dialog.name, "has ID", dialog.id)
                case _:
                    raise ValueError(
                        "Channel name should be a string or a list of strings"
                    )

    def read_messages(self):
        now = datetime.datetime.now()
        offset_date = now - datetime.timedelta(hours=21)
        print(f"Now: {now}, offset_date: {offset_date}")

        self.print_channel_ids(["Українці в Австрії", "Австрия Бизнес"])
