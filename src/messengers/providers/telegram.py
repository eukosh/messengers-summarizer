import datetime
import os
from typing import List, Optional, Union

from telethon import TelegramClient
from telethon.tl.types import Message

from src.const import CHAT_ID_MAPPING
from src.messengers.base_messenger import BaseMessenger
from src.utils import extract_props_from_obj_to_dict

TG_APP_ID = os.environ["TG_APP_ID"]
TG_API_HASH = os.environ["TG_API_HASH"]


class TelegramMessenger(BaseMessenger):
    def __init__(self):
        self.client = TelegramClient("anon", TG_APP_ID, TG_API_HASH)

    @staticmethod
    def run_with_client(func: callable):
        def wrapper(self, *args, **kwargs):
            with self.client as client:
                print("Running with client")
                return client.loop.run_until_complete(func(self, *args, **kwargs))

        return wrapper

    @run_with_client
    async def print_dialog_ids(self, channel_name: Union[str, List[str]]):
        print("Printing dialog IDs ", channel_name)

        def print_dialog_id(channel_name: str, dialog):
            channel_name = channel_name.lower()
            dialog_name = dialog.name.lower()
            if channel_name in dialog_name:
                print(dialog.name, "has ID", dialog.id)

        async for dialog in self.client.iter_dialogs():
            match channel_name:
                case str():
                    print_dialog_id(channel_name, dialog)
                case list():
                    for name in channel_name:
                        print_dialog_id(channel_name=name, dialog=dialog)

                case _:
                    raise ValueError("Channel name should be a string or a list of strings")

    @run_with_client
    async def get_messages(
        self,
        channel_id: int,
        start_date: Optional[datetime.datetime] = None,
        extract_props: Optional[List[str]] = None,
        skip_empty_messages: bool = True,
    ) -> List[Message]:
        messages = []
        async for message in self.client.iter_messages(channel_id, offset_date=start_date, reverse=True):
            if skip_empty_messages and not message.message:
                continue
            if extract_props:
                messages.append(extract_props_from_obj_to_dict(message, extract_props))
            else:
                messages.append(message)

        return messages

    def read_messages(self, start_date: Optional[datetime.datetime] = None, skip_empty_messages: bool = True):
        if not start_date:
            start_date = datetime.datetime.now() - datetime.timedelta(hours=10)
        print(f"Reading with offset_date: {start_date}")

        # self.print_dialog_ids(["Арина", "Українці в Австрії", "Австрия Бизнес", "Австрія IT"])

        messages = {}
        for channel_name, channel_id in CHAT_ID_MAPPING.items():
            chat_messages = self.get_messages(
                channel_id,
                start_date,
                extract_props=["id", "chat_id", "sender_id", "date", "message"],
                skip_empty_messages=skip_empty_messages,
            )
            messages[channel_name] = chat_messages

        return messages
