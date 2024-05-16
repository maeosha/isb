import os
import json
import logging

logging.basicConfig(level=logging.INFO)


def read_sequence_from_file(path_to_file: str) -> dict:
    """
    Reads a JSON file from the given path and returns its contents as a dictionary.

    :param path_to_file: The path to the file to read the sequence from.
    :return: A dictionary containing the sequences, or an empty dictionary if an error occurs.
    """
    sequences = {}
    try:
        with open(path_to_file, "r", encoding='utf-8') as file:
            sequences = json.load(file)
            logging.info(f"Successfully read sequences from '{path_to_file}'")
    except FileNotFoundError:
        logging.error(f"The file '{path_to_file}' does not exist.")
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error in file '{path_to_file}': {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while reading the file '{path_to_file}': {str(e)}")

    return sequences


def write_stats_to_file(path_to_file: str, stats: dict) -> None:
    """
    Writes the given statistics to a file in JSON format. Appends the stats as a new line in the file.

    :param path_to_file: The path to the file to write the statistics to.
    :param stats: A dictionary containing the statistics to write.
    :return: None
    """
    try:
        with open(path_to_file, "a", encoding="utf-8") as file:
            file.write(json.dumps(stats) + "\n")
            logging.info(f"Successfully wrote stats to '{path_to_file}'")
    except OSError as e:
        logging.error(f"An OS error occurred while writing to the file '{path_to_file}': {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while writing to the file '{path_to_file}': {str(e)}")
