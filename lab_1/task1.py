from string import ascii_letters
from random import choice
import logging

logging.basicConfig(level=logging.INFO)

def creating_key(key_word: list) -> list:
    """Сreate a key from a keyword according to the alphabetical order of letters"""
    key: list = [len(key_word)] * len(key_word)
    for index in range(len(key_word)):
        min_elem_index = key_word.index(min(key_word))
        key[min_elem_index] = 0 + index
        key_word[min_elem_index] = 1000

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