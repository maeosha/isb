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