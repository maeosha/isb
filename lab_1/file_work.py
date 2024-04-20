import json
import os
import logging

logging.basicConfig(level=logging.INFO)

def read_from_key_file(path_to_key_file: str) -> str:
    """
    Accepts the path to the file and returns the key.
    :param path_to_key_file:
    :return:
    """
    try:
        with open(path_to_key_file, "r", encoding='utf-8') as file:
            key: str = json.load(file)["key"]
    except OSError:
        logging.warning(f"The file {path_to_key_file} is not exist!", NameError)

    return key

def read_from_text_file(path_to_text_file: str):
    """
    Accepts the path to the file and returns the text.
    :param path_to_text_file:
    :return:
    """
    try:
        with open(path_to_text_file, "r", encoding="utf-8") as file:
            file.__next__()
            text = file.read()
    except OSError:
        logging.warning(f"The file {path_to_text_file} is not exist!", NameError)

    return text

def write_to_file(path_to_decrypt: str, text: str) -> None:
    """
    Write the result of the program to a file.
    :param path_to_decrypt:
    :param text:
    :return:
    """
    try:
        if os.path.exists(os.path.join(path_to_decrypt)):
            with open(path_to_decrypt, "w", encoding="utf-8") as file:
                text_dict = dict()
                text_dict["decrypted_text"] = text
                file.write(str(text_dict))

        else:
            raise FileExistsError(f"The file {path_to_decrypt} is not exist!")
    except OSError as error:
        logging.warning(error)
