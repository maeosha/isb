import hashlib
import multiprocessing as mp
import time
import logging

from matplotlib import pyplot as plt
from tqdm import trange

from file_work import write_card_num_to_file, read_config_file

logging.basicConfig(level=logging.INFO)

LEN_INS_ELEM: int = 6  # Length of the part of the card number to be inserted between BIN and last 4 digits
CHECK_INTERVAL: int = 1000  # Interval to check if the stop event is set
MAX_ITERATORS: int = 10000000  # Maximum number of iterations for generating card numbers


def hash_matches(card_bin: str, last_4_digits: str, card_hash: str, i: int):
    """
    Checks if the hash of the generated card number matches the given hash.

    :param card_bin: Card BIN.
    :param last_4_digits: Last 4 digits of the card number.
    :param card_hash: Given hash to compare.
    :param i: Current number being checked.
    :return: Tuple (True/False, generated card number or None).
    """
    str_i: str = "0" * (LEN_INS_ELEM - len(str(i))) + str(i)
    card_num = card_bin + str_i + last_4_digits
    hash = hashlib.sha3_512(card_num.encode()).hexdigest()

    if hash == card_hash:
        return True, card_num

    return False, None


def find_card_num_for_bin(card_bin: str, last_4_digits: str, card_hash: str, path_to_file: str, stop_event):
    """
    Attempts to find a card number for the given BIN and writes it to a file if found.

    :param card_bin: Card BIN.
    :param last_4_digits: Last 4 digits of the card number.
    :param card_hash: Given hash to compare.
    :param path_to_file: Path to the file to write the found card number.
    :param stop_event: Event to signal termination.
    """
    try:
        if len(card_bin) != 6:
            raise ValueError("Your BIN is incorrect, change the BIN and try again.")

        with trange(MAX_ITERATORS, desc=f"Selecting a card number with BIN: {card_bin}", leave=False) as t:
            for i in t:
                if i % CHECK_INTERVAL == 0 and stop_event.is_set():
                    break

                match, card_num = hash_matches(card_bin, last_4_digits, card_hash, i)
                if match:
                    write_card_num_to_file(card_num, path_to_file)
                    stop_event.set()
                    return True

    except ValueError as val_error:
        logging.error(val_error)

    except Exception as error:
        logging.exception(f"An error occurred while finding the card number for BIN: {card_bin}.", exc_info=error)


def find_card_num_with_mp(card_bins: list, last_4_digit: str, card_hash: str, number_of_process: int, path_to_file: str = ""):
    """
    Finds the card number using multiprocessing for different BINs.

    :param card_hash: Given hash to compare.
    :param last_4_digit: Last 4 digits of the card number.
    :param card_bins: List of BINs.
    :param number_of_process: Number of processes to use.
    :param path_to_file: Path to the file to write the found card number.
    """
    try:
        stop_event = mp.Manager().Event()
        with mp.Pool(number_of_process) as pool:
            results = [pool.apply_async(find_card_num_for_bin, args=(card_bin, last_4_digit, card_hash, path_to_file, stop_event)) for card_bin in card_bins]
            for result in results:
                if result.get():
                    logging.info("We managed to find the card number!")
                    pool.terminate()
                    break

    except Exception as error:
        logging.exception("An error occurred during multiprocessing card number search.", exc_info=error)


def check_correctness_card_num(card_num: str) -> None:
    """
    Checks the correctness of a card number using the Luhn algorithm.

    :param card_num: Card number as a string.
    :return: None
    """
    try:
        res, correct_num = lunas_algorithm(card_num)
        logging.info(f"Your card number: {card_num}")
        logging.info(f"The control number calculated for this number: {correct_num}")
        if res:
            logging.info("The control numbers match, the card number is correct!")
        else:
            logging.info("The control numbers do not match, the card number is incorrect!")

    except Exception as error:
        logging.exception("An error occurred while checking the correctness of the card number.", exc_info=error)


def lunas_algorithm(card_num: str):
    """
    Implements the Luhn algorithm to check the correctness of a card number.

    :param card_num: Card number as a string.
    :return: Tuple (bool, int), where bool indicates if the card number is correct,
             and int is the calculated control number.
    """
    try:
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

    except Exception as error:
        logging.exception("An error occurred while executing the Luhn algorithm.", exc_info=error)
        return False, -1


def time_collision_search(card_bins: list, last_4_digit: str, card_hash: str):
    """
    Measures the execution time of finding a card number using different numbers of processes.

    :param card_bins: List of BINs.
    :param last_4_digit: Last 4 digits of the card number.
    :param card_hash: Given hash to compare.
    """
    try:
        time_list: list = list()
        number_of_process_list: list = list()
        for number_of_processes in range(1, int(mp.cpu_count() * 1.5 + 1)):
            start_time = time.time()
            find_card_num_with_mp(card_bins, last_4_digit, card_hash, number_of_processes)
            end_time = time.time()

            time_list.append(end_time - start_time)
            number_of_process_list.append(number_of_processes)
        generate_graph(number_of_process_list, time_list)

    except Exception as error:
        logging.exception("An error occurred during the collision search timing.", exc_info=error)


def generate_graph(x: list, y: list) -> None:
    """
    Generate a graph to visualize execution time vs. number of processes.

    :param x: List of number of processes.
    :param y: List of execution times.
    """
    try:
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

    except Exception as error:
        logging.exception("An error occurred while generating the graph.", exc_info=error)


def mode_choice(mode: int, path_to_file: str, card_bins: list, last_4_digit: str, card_hash: str, card_num: str):
    """
    Selects and executes the appropriate mode of operation based on user input.

    :param mode: Mode of operation (1, 2, or 3).
    :param card_bins: List of BINs.
    :param last_4_digit: Last 4 digits of the card number.
    :param card_hash: Given hash to compare.
    :param card_num: Card number as a string (used in mode 2).
    :param path_to_file: Path to the file to write the found card number (used in mode 1).
    """
    try:
        match mode:
            case 1:
                number_of_processes: int = mp.cpu_count()
                find_card_num_with_mp(card_bins, last_4_digit, card_hash, number_of_processes, path_to_file)

            case 2:
                check_correctness_card_num(card_num)

            case 3:
                time_collision_search(card_bins, last_4_digit, card_hash)

            case _:
                raise ValueError("Incorrect mode of operation, select another one and try again!")

    except ValueError as val_error:
        logging.error(val_error)

    except Exception as error:
        logging.exception("An unexpected error occurred during mode execution.", exc_info=error)


def start_work(mode: int, path_to_config_file: str, path_to_file: str):
    """
    Starts the card number processing work based on the selected mode.

    :param mode: Mode of operation (1, 2, or 3).
    :param path_to_config_file: Path to the configuration file.
    :param path_to_file: Path to the file to write the found card number (used in mode 1).
    """
    config: dict = read_config_file(path_to_config_file)
    mode_choice(mode, path_to_file,
                config['card_bins'],
                config['last_4_digits'],
                config['card_hash'],
                config['card_number'])

