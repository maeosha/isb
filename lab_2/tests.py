import math
import mpmath

from filework import read_sequence_from_file, write_stats_to_file

def frequency_bitwise_test(sequences: dict, path_to_file: str) -> None:
    """
    Obtaining the probability of randomness of the obtained sequence using a frequency bit test.
    :param sequences: 
    :param path_to_file: 
    :return: 
    """
    for sequence in sequences.items():
        S: float = 0
        zero_or_one: dict = {"1": 1, "0": -1}
        stats: dict = dict()
        sequence_value: str = sequence[1]
        sequence_key: str = sequence[0]
        P: float = 0

        for elem in sequence_value:
            S += zero_or_one[elem]

        S = S / math.sqrt(len(sequence_value))
        P = math.erfc(math.fabs(S / math.sqrt(2)))
        stats[f"Frequency bitwise test with {sequence_key} sequence"] = P
        
        write_stats_to_file(path_to_file, stats)


def start_work(path_to_sequence_file: str, path_to_stats_file: str) -> None:
    """
    Getting started with the program, the resulting paths are used for subsequent functions.
    :param path_to_sequence_file: 
    :param path_to_stats_file: 
    :return: 
    """""
    sequences: dict = read_sequence_from_file(path_to_sequence_file)
    frequency_bitwise_test(sequences, path_to_stats_file)

