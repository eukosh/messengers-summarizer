import time

from src.llm import summarize_topics
from src.messengers.messenger_factory import MessengerFactory
from src.messengers.providers.telegram import TelegramMessenger

if __name__ == "__main__":
    messenger: TelegramMessenger = MessengerFactory.get_or_create_messenger("telegram")()
    print(messenger)
    messages = messenger.read_messages()

    start_time = time.time()
    for channel, channel_messages in messages.items():
        print("Summarizing topics for channel:", channel)
        model_res = summarize_topics(channel_messages)
        print(f"Channel: {channel}, Result: {model_res}\n\n")

    end_time = time.time()
    elapsed_time = (end_time - start_time) / 60
    print("Time taken to summarize all messages:", elapsed_time, "minutes")
