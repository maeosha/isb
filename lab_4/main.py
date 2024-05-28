import argparse
import os

from card_num_tool import start_work


def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Find card numbers or check their correctness using multiprocessing.")

    parser.add_argument(
        "--mode",
        type=int,
        choices=[1, 2, 3],
        default=1,
        help="Choose the mode of operation: 1 - search for card numbers (default), 2 - check card numbers for correctness, 3 - generate a graph based on code execution time."
    )

    parser.add_argument(
        "--path_to_config_file",
        type=str,
        default=os.path.join("config.json"),
        help="Path to the configuration file (default: config.json)"
    )

    parser.add_argument(
        "--path_to_file",
        default=os.path.join("card_num.txt"),
        type=str,
        help=f"Path to the file to write the found card number (default: card_num.txt)"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    start_work(*vars(args).values())