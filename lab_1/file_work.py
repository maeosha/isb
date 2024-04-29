import json
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
    except OSError as error:
        logging.warning(error, NameError)
    except Exception as error:
        logging.warning(f"The file {path_to_key_file} is not exist!", error)

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
    except OSError as error:
        logging.warning(error, NameError)
    except Exception as error:
        logging.warning(f"The file {path_to_text_file} is not exist!", error)

    return text

def write_to_file(path_to_decrypt: str, text: str) -> None:
    """
    Write the result of the program to a file.
    :param path_to_decrypt:
    :param text:
    :return:
    """
    try:
        with open(path_to_decrypt, "x", encoding="utf-8") as file:
                text_dict = dict()
                text_dict["decrypted_text"] = text
                file.write(str(text_dict))
    except OSError as error:
        logging.warning(error)
    except Exception as error:
        logging.warning(f"The file {path_to_decrypt} is not exist!", error)
