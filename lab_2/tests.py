import math
import mpmath

from file_work import read_sequence_from_file, write_stats_to_file

PI: list = [0.2148, 0.3672, 0.2305, 0.1875]

len_mini_sequence: int = 8


def frequency_bitwise_test(sequences: dict, path_to_file: str) -> None:
    """
    Obtaining the probability of randomness of the obtained sequence using a frequency bit test.
    :param sequences: random sequences from java and c++
    :param path_to_file: path to write statistics
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


def test_for_same_bits(sequences: dict, path_to_file: str) -> None:
    """
    Obtaining the probability of randomness of the obtained sequence using a same bits test.
    :param sequences: random sequences from java and c++
    :param path_to_file: path to write statistics
    :return:
    """
    for sequence in sequences.items():
        one_count: float = 0
        sequence_value: str = sequence[1]
        sequence_key: str = sequence[0]
        stats: dict = dict()
        P: float = 0
        alternating_count: int = 0

        one_count = sequence_value.count("1") / len(sequence_value)

        if math.fabs(one_count - 0.5) >= (2 / math.sqrt(len(sequence_value))):
            stats[f"Test for same bits with {sequence_key} sequence"] = 0
            write_stats_to_file(path_to_file, stats)

        else:
            for index in range(len(sequence_value) - 1):
                if sequence_value[index] != sequence_value[index + 1]:
                    alternating_count += 1

            numerator = math.fabs(alternating_count - 2 * len(sequence_value) * one_count * (1 - one_count))
            denomirator = 2 * math.sqrt(2 * len(sequence_value)) * one_count * (1 - one_count)

            P = math.erfc(numerator / denomirator)
            stats[f"Test for same bits with {sequence_key} sequence"] = P

            write_stats_to_file(path_to_file, stats)


def ones_sequence_test(sequences: dict, path_to_file: str, len_mini_sequence: int) -> None:
    """
    Obtaining the probability of randomness of the obtained sequence using an ones sequence test.
    :param sequences: random sequences from java and c++
    :param path_to_file: path to write statistics
    :param len_mini_sequence: The length of the blocks into which the sequence will be split
    :return:
    """
    for sequence in sequences.items():
        sequence_value: str = sequence[1]
        sequence_key: str = sequence[0]
        P: float = 0
        xi_sqrt: float = 0
        stats: dict = dict()
        mini_sequence_count: list = [0, 0, 0, 0]

        for i_index in range(0, len(sequence_value), len_mini_sequence):
            ones_count: int = 0
            max_ones_count = -1

            for j_index in range(i_index, i_index + len_mini_sequence):
                if sequence_value[j_index] == "0":
                    ones_count = 0
                else:
                    ones_count += 1

                max_ones_count = max(max_ones_count, ones_count)

            match max_ones_count:
                case 0 | 1:
                    mini_sequence_count[0] += 1

                case 2:
                    mini_sequence_count[1] += 1

                case 3:
                    mini_sequence_count[2] += 1

                case _:
                    mini_sequence_count[3] += 1

        for value in zip(PI, mini_sequence_count):
            numerator: float = math.pow(value[1] - 16 * value[0], 2)
            denominator: float = 16 * value[0]
            xi_sqrt += (numerator / denominator)

        P = mpmath.gammainc(1.5, xi_sqrt / 2)
        stats[f"Ones sequence test with {sequence_key} sequence"] = float(P)

        write_stats_to_file(path_to_file, stats)


def start_work(path_to_sequence_file: str, path_to_stats_file: str) -> None:
    """
    Getting started with the program, the resulting paths are used for subsequent functions.
    :param path_to_sequence_file: path to read random sequence
    :param path_to_stats_file: path to write statistics
    :return: 
    """""
    sequences: dict = read_sequence_from_file(path_to_sequence_file)
    frequency_bitwise_test(sequences, path_to_stats_file)
    test_for_same_bits(sequences, path_to_stats_file)
    ones_sequence_test(sequences, path_to_stats_file, len_mini_sequence)

