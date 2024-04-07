import os
import json
import logging

from string import ascii_letters
from random import choice

logging.basicConfig(level=logging.INFO)

def read_from_file(path_to_file: str) -> dict:
    """Reading the key and text from the file"""
    try:
        with open(os.path.join(path_to_file), "r", encoding='utf-8') as file:
            info: dict = json.load(file)
    except FileExistsError:
        logging.warning(f"The file {path_to_file} is not exist!", NameError)

    return info

def key_conversion(key_word: list) -> list:
    """Сreate a key from a keyword according to the alphabetical order of letters"""
    key: list = [len(key_word)] * len(key_word)
    tmp_big_elem: int = max(key_word) + 1
    for index in range(len(key_word)):
        min_elem_index = key_word.index(min(key_word))
        key[min_elem_index] = index
        key_word[min_elem_index] = tmp_big_elem

    return key

def adding_letters(text: str, key: list) -> str:
    """Complete the text to the full distribution by key, for further encoding"""
    while len(text) % len(key) != 0:
        random_letter = choice(ascii_letters)
        text += random_letter

    return text

def encrypting_text(text: str, key: list) -> str:
    """Encrypt the text using the route permutation method"""
    encryption_matrix: list = list()
    encrypted_text: str = ""

    for index in range(0, len(text), len(key)):
        encryption_matrix.append(text[index:len(key) + index])

    for index in key:
        for row in encryption_matrix:
            encrypted_text += row[index]

    return encrypted_text

def write_to_file(path_to_decrypt: str, text: str) -> None:
    """Writing encrypted text to a file"""
    try:
        if os.path.exists(os.path.join(path_to_decrypt)):
            with open(os.path.join(path_to_decrypt), "w", encoding="utf-8") as file:
                file.write(text)
        else:
            raise FileExistsError(f"The file {path_to_decrypt} is not exist!")
    except FileExistsError as error:
        logging.warning(error)



def start_to_encrypt(path_to_file: str, path_to_decrypt: str) -> None:
    key_word: list = list(map(ord, read_from_file(path_to_file)["key"]))
    text: str = read_from_file(path_to_file)["text"]
    key: list = key_conversion(key_word)
    text = adding_letters(text, key)
    decrypted_text = encrypting_text(text, key)
    write_to_file(path_to_decrypt, decrypted_text)
