import os
import json
import logging

def read_sequence_from_file(path_to_file: str) -> dict:
    """
    Reading a file using the accepted path.
    :param path_to_file:
    :return sequence:
    """
    try:
        with open(path_to_file, "r", encoding='utf-8') as file:
            sequences: dict = json.load(file)
    except OSError as error:
        logging.warning(error, NameError)
    except Exception as error:
        logging.warning(f"The file {path_to_key_file} is not exist!", error)

    return sequences

def write_stats_to_file(path_to_file: str, stats: dict) -> None: 
    """
    Writing to a file using the accepted path.
    :param path_to_file:
    :param stats:
    :return:
    """
    try:
        if os.path.exists(path_to_file):
            with open(path_to_file, "a", encoding="utf-8") as file:
                file.writelines(str(stats)[1:-1] + "\n")
        else:
            raise FileExistsError(f"The file {path_to_decrypt} is not exist!")
    except OSError as error:
        logging.warning(error, NameError)
    except Exception as error:
        logging.warning(f"The file {path_to_key_file} is not exist!", error)
        