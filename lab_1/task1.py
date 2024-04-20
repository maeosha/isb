import logging

from string import ascii_letters
from random import choice

from file_work import read_from_key_file, read_from_text_file, write_to_file

logging.basicConfig(level=logging.INFO)

def key_conversion(key: str) -> list:
    """
    Create a key from a keyword according to the alphabetical order of letters.
    :param key:
    :return key:
    """
    key = list(map(ord, key))
    key = [len(key)] * len(key)
    tmp_big_elem: int = max(key) + 1
    for index in range(len(key)):
        min_elem_index = key.index(min(key))
        key[min_elem_index] = index
        key[min_elem_index] = tmp_big_elem

    return key

def adding_letters(text: str, key: list) -> str:
    """
    Complete the text to the full distribution by key, for further encoding.
    :param text:
    :param key:
    :return text:
    """
    while len(text) % len(key) != 0:
        random_letter = choice(ascii_letters)
        text += random_letter

    return text

def encrypting_text(text: str, key: list) -> str:
    """
    Encrypt the text using the route permutation method.
    :param text:
    :param key:
    :return:
    """
    encryption_matrix: list = list()
    encrypted_text: str = ""

    for index in range(0, len(text), len(key)):
        encryption_matrix.append(text[index:len(key) + index])

    for index in key:
        for row in encryption_matrix:
            encrypted_text += row[index]

    return encrypted_text

def start_to_encrypt(path_to_key_file: str, path_to_text_file: str, path_to_decrypt: str) -> None:
    """
    The start of the program, the input gets the path to work with files.
    :param path_to_key_file:
    :param path_to_text_file:
    :param path_to_decrypt:
    :return:
    """
    key: str = read_from_key_file(path_to_key_file)
    key: list = key_conversion(key)

    text: str = read_from_text_file(path_to_text_file)

    text = adding_letters(text, key)
    decrypted_text = encrypting_text(text, key)
    write_to_file(path_to_decrypt, decrypted_text)
