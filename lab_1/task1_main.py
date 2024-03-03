import argparse
from encrypting_text import start_to_encrypt

parser = argparse.ArgumentParser()

parser.add_argument('--keyword',
                    type=str,
                    default="abcdMaxim",
                    help='Enter the keyword.(default: abcdMaxim')

parser.add_argument('text',
                    type=str,
                    help='Enter the text to encrypt.')

if __name__ == "__main__":
    my_variables = parser.parse_args()
    start_to_encrypt(*(vars(my_variables).values()))

