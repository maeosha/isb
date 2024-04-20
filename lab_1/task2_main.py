import argparse
import os

from task2 import start_decrypt

parser = argparse.ArgumentParser()

parser.add_argument('--path_to_text_file',
                    type=str,
                    default="task2_text.json",
                    help='Enter the path to the encrypted text file.(default: task2_text.json')

parser.add_argument('--path_to_key_file',
                    type=str,
                    default="task2_key.txt",
                    help='Enter the path to the encrypted text file.(default: task2_key.txt')

parser.add_argument('--path_to_decrypted_file',
                    type=str,
                    default='decrypted_file_task2.txt',
                    help='Enter the path to the key file.(default: decrypted_file_task2.txt')

if __name__ == "__main__":
    my_variables = parser.parse_args()
    start_decrypt(*map(os.path.join, (vars(my_variables).values())))