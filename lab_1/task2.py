import json
import os
import logging

def read_from_text_file(path_to_file: str) -> str:
    """Read encrypted text from a file"""
    encrypted_text: str = ""
    try:
        with open(os.path.join(path_to_file), "r") as file:
            encrypted_text = json.load(file)["encrypted_text"]
    except FileExistsError:
        logging.warning(f"The file {path_to_file} is not exist!", NameError)

    return encrypted_text.replace("\n", "")

def read_from_key_file(path_to_file: str) -> list:
    """"""
    try:
        with open(os.path.join(path_to_file), "r", encoding='utf-8') as file:
            key = [i[7] for i in json.load(file)["key"].split(", ")]

    except FileExistsError:
        logging.warning(f"The file {path_to_file} is not exist!", NameError)
    return key


def get_stats(encrypted_text: str, key: list) -> str:
    """Calculating the percentage of letters meeting and decoding the text"""

    stats: dict = dict()

    for letter in sorted(set(encrypted_text)):
        stats[letter] = encrypted_text.count(letter)

    for i in range(len(stats)):
        count = 0
        for j in range(i + 1, len(stats)):
            if list(stats.items())[i][1] == list(stats.items())[j][1]:
                if ord(list(stats.items())[i][0]) > ord(list(stats.items())[j][0]):
                    stats[list(stats.items())[j][0]] += 0.01 + count
                else:
                    stats[list(stats.items())[i][0]] += 0.01 + count
                count += 0.01


    stats = dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))

    keys = list(stats.keys())
    i = 0

    for stat in key:
        encrypted_text = encrypted_text.replace(keys[i], stat)
        i += 1

    return encrypted_text



def write_to_file(decrypted_text: str, path_to_decrypted_file: str) -> None:
    """Write the decrypted text and the encryption key to the file"""
    try:
        if os.path.exists(os.path.join(path_to_decrypted_file)):
            with open(os.path.join(path_to_decrypted_file), "w", encoding='utf-8') as file:
                file.write("Decrypted text: \n")
                file.write(decrypted_text)
        else:
            raise FileExistsError(f"The file {path_to_decrypted_file} is not exist!")
    except FileExistsError as error:
        logging.warning(error, NameError)



def start_decrypt(path_to_file: str, path_to_decrypted_file: str) -> None:
    encrypted_text: str = read_from_text_file(path_to_file)
    key: list = read_from_key_file(path_to_file)

    decrypted_text = get_stats(encrypted_text, key)

    write_to_file(decrypted_text, path_to_decrypted_file)
