import argparse
import multiprocessing as mp
import os

from card_num_tool import mode_choice

def parse_arguments():
    """
    Parse command line arguments.
    """
    default_card_bins = ["437772", "437783", "437773", "470127"]
    default_last_4_digits = "5274"
    default_card_hash = "e537d605a9f957a2c6ccb8cb2bb59537675e048c7ef78f86389a333d54feb154270a0f9df684f2b0d0e30c4eee9403bfd53b8e32af89f6fba9fd16aafdfa7420"
    default_path_to_file = os.path.join("card_num.txt")
    default_processes = mp.cpu_count()
    default_card_number = "4377721789462148"

    parser = argparse.ArgumentParser(description="Find card numbers or check their correctness using multiprocessing.")

    parser.add_argument(
        "--mode",
        type=int,
        choices=[1, 2, 3],
        default=1,
        help="Choose the mode of operation: 1 - search for card numbers (default), 2 - check card numbers for correctness, 3 - generate a graph based on code execution time."
    )

    parser.add_argument(
        "--card_bins",
        nargs="+",
        default=default_card_bins,
        type=str,
        help=f"List of card BINs (default: {' '.join(default_card_bins)})"
    )

    parser.add_argument(
        "--last_4_digits",
        default=default_last_4_digits,
        type=str,
        help=f"Last 4 digits of the card number (default: {default_last_4_digits})"
    )

    parser.add_argument(
        "--card_hash",
        default=default_card_hash,
        type=str,
        help=f"Hash of the correct card number (default: {default_card_hash})"
    )

    parser.add_argument(
        "--card_number",
        type=str,
        default=default_card_number,
        help=f"Card number to check (default: {default_card_number})"
    )

    parser.add_argument(
        "--path_to_file",
        default=default_path_to_file,
        type=str,
        help=f"Path to the file to write the found card number (default: {default_path_to_file})"
    )

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    mode_choice(*vars(args).values())