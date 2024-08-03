from src.messengers.messenger_factory import MessengerFactory

if __name__ == "__main__":
    # Usage example
    messenger = MessengerFactory.get_or_create_messenger("telegram")()
    print(messenger)
    messages = messenger.read_messages()
    print(messages)
