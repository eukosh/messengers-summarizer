"""A collection of utility functions."""

from telethon.types import Message


def extract_props_from_obj_to_dict(obj: object, properties: list[str]) -> dict:
    """
    Extracts specified properties from an object and returns them as a dictionary.

    Args:
        obj: The object from which to extract properties.
        properties: A list of property names to extract.

    Returns:
        A dictionary containing the extracted properties as key-value pairs.
    """
    result = {}
    for prop in properties:
        result[prop] = getattr(obj, prop)
    return result


def print_message(message: Message | dict):
    """
    Prints the key-value pairs of a dictionary or stringified message.

    Args:
        message: The dictionary or message to be pretty printed.
    """
    if isinstance(message, Message):
        print(message.stringify())
    else:
        for key, value in message.items():
            print(f"{key}: {value}")
    print("--------------------")
