from src.const import messages
from src.messengers.messenger_factory import MessengerFactory

if __name__ == "__main__":
    # Usage example
    messenger = MessengerFactory.get_or_create_messenger("telegram")()
    print(messenger)
    # messages = messenger.read_messages()
    # smaller_messages = {}
    # for channel, channel_messages in messages.items():
    #     smaller_messages[channel] = channel_messages[:2]
    # print(smaller_messages)
    