import logging
import json


def write_card_num_to_file(card_num: str, path_to_file: str):
    """
    Writes the card number to a file.

    :param card_num: The card number to write to the file.
    :param path_to_file: The path to the file where the card number will be written.
    """
    if path_to_file == "":
        return

    try:
        with open(path_to_file, 'w') as file:
            file.write(card_num)

    except OSError as e:
        logging.error(f"OS error occurred while writing card number '{card_num}' to '{path_to_file}': {e}")
    except Exception as e:
        logging.error(f"Error writing card number '{card_num}' to '{path_to_file}': {e}")


def read_config_file(config_path: str) -> dict:
    """
    Load configuration from a JSON file.
    :param config_path: The path to the JSON configuration file.
    :return config:
    """
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        return config
    except OSError as e:
        logging.error(f"The configuration file {config_path} was not found.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the configuration file {config_path}: {e}") from e

