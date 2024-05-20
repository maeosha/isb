import hashlib
import multiprocessing as mp
import time

from matplotlib import pyplot as plt
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


def check_correctness_card_num(card_num: str) -> None:
    """
    Checks the correctness of a card number using the Luhn algorithm.

    :param card_num: Card number as a string.
    :return: None
    """
    res, correct_num = lunas_algorithm(card_num)
    logging.info(f"Your card number: {card_num}")
    logging.info(f"The control number calculated for this number: {correct_num}")
    if res:
        logging.info("The control numbers match, the card number is correct!")
    else:
        logging.info("The control numbers do not match, the card number is incorrect!")


def lunas_algorithm(card_num: str):
    """
    Implements the Luhn algorithm to check the correctness of a card number.

    :param card_num: Card number as a string.
    :return: Tuple (bool, int), where bool indicates if the card number is correct,
             and int is the calculated control number.
    """
    control_num = int(card_num[-1])
    card_num = card_num[:-1]
    reverse_card_num: str = card_num[::-1]
    checksum: int = 0

    for index, digit in enumerate(reverse_card_num):
        if index % 2 == 0:
            digit = str(int(digit) * 2)
        checksum += sum(map(int, digit))
    checksum = (10 - (checksum % 10)) % 10

    if checksum == control_num:
        return True, checksum
    return False, checksum


def time_collision_search():
    time_list: list = list()
    number_of_process_list: list = list()
    for number_of_processes in range(1, int(mp.cpu_count() * 1.5)):
        start_time = time.time()
        find_card_num_with_mp(number_of_processes)
        end_time = time.time()

        time_list.append(end_time - start_time)
        number_of_process_list.append(number_of_processes)
    generate_graph(number_of_process_list, time_list)


def generate_graph(x: list, y: list) -> None:
    """
    Generate a graph to visualize execution time vs. number of processes.

    :param x: List of number of processes.
    :param y: List of execution times.
    """
    fig, ax = plt.subplots()

    ax.plot(x, y, color="blue", marker='o', linestyle='-')

    y_min = min(y)
    x_min = y.index(y_min) + 1
    ax.scatter(x_min, y_min, color="red", label="minimum execution time", zorder=5)

    ax.set_xlabel("Number of processes")
    ax.set_ylabel("Execution time (s)")
    ax.set_title("Execution Time vs. Number of Processes")

    ax.set_xticks(x)
    ax.grid(True)

    ax.legend()

    plt.tight_layout()
    plt.show()