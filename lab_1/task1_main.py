import argparse
from task1 import start_to_encrypt

parser = argparse.ArgumentParser()

parser.add_argument('--path_to_text_file',
                    type=str,
                    default="task1.json",
                    help='Enter the path to the encrypted text file.(default: task1.json')

parser.add_argument('--path_to_decrypt',
                    type=str,
                    default="encrypt_task1.txt",
                    help='Enter the path to the decrypted text file.(default: encrypt_task1.txt')

if __name__ == "__main__":
    my_variables = parser.parse_args()
    start_to_encrypt(*(vars(my_variables).values()))

