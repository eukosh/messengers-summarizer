# Messengers Summarizer

Messengers Summarizer is a Python library that allows you to summarize extract topics discussed in chats from various messengers, currently only Telegram is supported.

### Prerequisites

Before using Messengers Summarizer, make sure you have the following prerequisites:

- Ollama: Install and run Ollama, a dependency required by Messengers Summarizer.
- Llama3.1 Model: Ensure that the Llama3.1 model is available for use by Messengers Summarizer.

Once you have installed and set up Ollama, and have the Llama3.1 model accessible, you are ready to proceed with using Messengers Summarizer.

TG_APP_ID=24077727
TG_API_HASH=cb2a1fd77b1fec4dad6170ae2080c9a5

### Getting Started

To get started with Messengers Summarizer, follow these steps:

1. Create a `.env` file in the project root directory.
2. Add the following values to the `.env` file:

```
TG_APP_ID=<your_telegram_app_id>
TG_API_HASH=<your_telegram_api_hash>
```

To obtain the `TG_APP_ID` and `TG_API_HASH` values, refer to the [Telegram documentation](https://core.telegram.org/api/obtaining_api_id) on how to create a Telegram application and obtain the required credentials.

3. Update the `const.py` file in the project. In this file, you will find a mapping between chat IDs and chat names. Update this mapping with the chat IDs and names of your own chats.

To get the dialog ID for a specific chat, you can use the `print_dialog_ids` method in the `Telegram` class. This method will print the ID for the specified chat name.

Once you have completed these steps, you are ready to use Messengers Summarizer to extract topics discussed in your chats.

4. Run the following command in your terminal to install the necessary dependencies:

```
poetry install
```

5. Activate the virtual environment by running the following command:

```
poetry shell
```

6. Finally, run the following command in your terminal to summarize messages in the specified chats:

```
python main.py
```

This will initiate the process of summarizing the messages in the chats that you have specified in the `const.py` file. The summarized topics will be displayed as output.

Make sure you have the necessary dependencies installed and the required credentials set up before running the command.

Congratulations! You have successfully summarized the messages in your chats using Messengers Summarizer.
Feel free to use other models than llama3.1.
