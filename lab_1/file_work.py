import json
import logging
import os

logging.basicConfig(level=logging.INFO)

def read_from_file_task1(path_to_file: str) -> dict:
    """Reading the key from the file"""
    try:
        with open(os.path.join(path_to_file), "r", encoding='utf-8') as file:
            info: dict = json.load(file)
    except FileExistsError or FileNotFoundError:
        logging.warning(f"The file {path_to_file} is not exist!", NameError)

    return info


def read_from_text_file_task2(path_to_file: str) -> str:
    """Read encrypted text from a file"""
    encrypted_text: str = ""
    try:
        with open(os.path.join(path_to_file), "r") as file:
            encrypted_text = json.load(file)["encrypted_text"]
    except FileExistsError or FileNotFoundError:
        logging.warning(f"The file {path_to_file} is not exist!", NameError)

    return encrypted_text.replace("\n", "")

def read_from_key_file_task2(path_to_file: str) -> list:
    """reading a key from a file, any key position is possible"""
    try:
        with open(os.path.join(path_to_file), "r", encoding='utf-8') as file:
            key = [i[0] for i in json.load(file)["key"].split(", ").replase(" ", "")]

    except FileExistsError or FileNotFoundError:
        logging.warning(f"The file {path_to_file} is not exist!", NameError)
    return key


def write_to_file(path_to_decrypt: str, text: str) -> None:
    """Writing encrypted text to a file"""
    try:
        if os.path.exists(os.path.join(path_to_decrypt)):
            with open(os.path.join(path_to_decrypt), "w", encoding="utf-8") as file:
                text_dict = dict()
                text_dict["decrypted_text"] = text
                file.write(str(text_dict))

        else:
            raise FileExistsError(f"The file {path_to_decrypt} is not exist!")
    except FileExistsError or FileNotFoundError as error:
        logging.warning(error)
