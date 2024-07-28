import datetime
import os

from telethon import TelegramClient

from src.messengers.messenger_factory import MessengerFactory

TG_APP_ID = os.environ["TG_APP_ID"]
TG_API_HASH = os.environ["TG_API_HASH"]


client = TelegramClient("anon", TG_APP_ID, TG_API_HASH)


# Українці в Австрії has ID -1001564907709
# Австрия Бизнес has ID -1001456139769


now = datetime.datetime.now()
offset_date = now - datetime.timedelta(hours=21)
print(f"Now: {now}, offset_date: {offset_date}")


async def main():
    # async for dialog in client.iter_dialogs():
    #     if dialog.name in ("Українці в Австрії", "Австрия Бизнес"):
    #         print(dialog.name, "has ID", dialog.id)

    async for message in client.iter_messages(
        "@adovhai", offset_date=offset_date, reverse=True
    ):
        print(message.stringify())


# with client:
#     client.loop.run_until_complete(main())


if __name__ == "__main__":
    # Usage example
    messenger = MessengerFactory.get_or_create_messenger("telegram")
    print(messenger)
