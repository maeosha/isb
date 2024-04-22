import argparse
import os

from tests import start_work

parser = argparse.ArgumentParser()

parser.add_argument('--path_to_key_file',
                    type=str,
                    default="stats/random_sequence.json",
                    help='Enter the path to the random sequence file.(default: stats/random_sequence.json')

parser.add_argument('--path_to_text_file',
                    type=str,
                    default="stats/stats.txt",
                    help='Enter the path to the stats file.(default: stats/stats.txt')


if __name__ == "__main__":
    my_variables = parser.parse_args()
    start_work(*map(os.path.join, (vars(my_variables).values())))

