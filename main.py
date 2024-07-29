from src.messengers.messenger_factory import MessengerFactory

# Українці в Австрії has ID -1001564907709
# Австрия Бизнес has ID -1001456139769


# async def main():


#     async for message in client.iter_messages(
#         "@adovhai", offset_date=offset_date, reverse=True
#     ):
#         print(message.stringify())


if __name__ == "__main__":
    # Usage example
    messenger = MessengerFactory.get_or_create_messenger("telegram")()
    print(messenger)
    messenger.read_messages()
