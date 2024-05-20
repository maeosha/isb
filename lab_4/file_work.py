import logging


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

