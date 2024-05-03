import math
import mpmath

from file_work import read_sequence_from_file, write_stats_to_file

PI_0: float = 0.2148
PI_1: float = 0.3672
PI_2: float = 0.2305
PI_3: float = 0.1875

len_mini_sequence: int = 8


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


def test_for_same_bits(sequences: dict, path_to_file: str) -> None:
    """
    Obtaining the probability of randomness of the obtained sequence using a same bits test.
    :param sequences:
    :param path_to_file:
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
    :param sequences:
    :param path_to_file:
    :param len_mini_sequence:
    :return:
    """
    for sequence in sequences.items():
        sequence_value: str = sequence[1]
        sequence_key: str = sequence[0]
        P: float = 0
        xi_sqrt: float = 0
        stats: dict = dict()
        probabilities_pi: dict = {PI_0: 0, PI_1: 0, PI_2: 0, PI_3: 0}

        for i_index in range(0, len(sequence_value), 8):
            ones_count: int = 0
            max_ones_count = -1

            for j_index in range(i_index, i_index + 8):
                if sequence_value[j_index] == "0":
                    ones_count = 0
                else:
                    ones_count += 1

                max_ones_count = max(max_ones_count, ones_count)

            match max_ones_count:
                case 0 | 1:
                    probabilities_pi[PI_0] += 1

                case 2:
                    probabilities_pi[PI_1] += 1

                case 3:
                    probabilities_pi[PI_2] += 1

                case _:
                    probabilities_pi[PI_3] += 1

        for PI in probabilities_pi.keys():
            numerator: float = math.pow(probabilities_pi[PI] - 16 * PI, 2)
            denominator: float = 16 * PI
            xi_sqrt += (numerator / denominator)

        P = mpmath.gammainc(1.5, xi_sqrt / 2)
        stats[f"Ones sequence test with {sequence_key} sequence"] = float(P)

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
    test_for_same_bits(sequences, path_to_stats_file)
    ones_sequence_test(sequences, path_to_stats_file, len_mini_sequence)

