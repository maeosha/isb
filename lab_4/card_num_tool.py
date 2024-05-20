import hashlib
import multiprocessing as mp

from tqdm import trange
from file_work import *

len_ins_elem = 6
check_interval: int = 1000 #
max_iterators = 10000000



def hash_matches(card_bin: str, last_4_digits: str, card_hash: str, i:int):
    """
    Checks if the hash of the generated card number matches the given hash.

    :param card_bin: Card BIN.
    :param last_4_digits:
    :param card_hash:
    :param i: Current number being checked.
    :return: Tuple (True/False, generated card number or None).
    """
    str_i: str = "0" * (len_ins_elem - len(str(i))) + str(i)
    card_num = card_bin + str_i + last_4_digits
    hash = hashlib.sha3_512(card_num.encode()).hexdigest()

    if hash == card_hash:
        return True, card_num

    return False, None


def find_card_num_for_bin(card_bin: str, last_4_digits: str, card_hash: str, path_to_file: str, stop_event):
    """
    Attempts to find a card number for the given BIN and writes it to a file if found.

    :param card_bin: Card BIN.
    :param last_4_digits:
    :param card_hash:
    :param path_to_file: Path to the file to write the found card number.
    :param stop_event: Event to signal termination.
    """
    with trange(max_iterators, desc=f"Selecting a card number with BIN: {card_bin}", leave=False) as t:
        for i in t:
            if i % check_interval == 0 and stop_event.is_set():
                break

            match, card_num = hash_matches(card_bin, last_4_digits, card_hash, i)
            if match:
                write_card_num_to_file(card_num, path_to_file)
                stop_event.set()
                return True
        return False


def find_card_num_with_mp(card_bins: list, last_4_digit: str, card_hash: str, number_of_process: int, path_to_file: str = ""):
    """
    Finds the card number using multiprocessing for different BINs.
    :param card_hash:
    :param last_4_digit:
    :param card_bins:
    :param number_of_process:
    :param path_to_file: Path to the file to write the found card number.
    """
    stop_event = mp.Manager().Event()
    with mp.Pool(number_of_process) as pool:
        results = [pool.apply_async(find_card_num_for_bin, args=(card_bin, last_4_digit, card_hash, path_to_file, stop_event)) for card_bin in card_bins]
        for result in results:
            if result.get():
                logging.info("We managed to find the card number!")
                pool.terminate()
                break

