import argparse
from task2 import start_decrypt

parser = argparse.ArgumentParser()

parser.add_argument('--path_to_file',
                    type=str,
                    default="task2.json",
                    help='Enter the path to the encrypted text file.(default: encrypted.txt')

parser.add_argument('--path_to_decrypted_file',
                    type=str,
                    default='decrypted_file_task2.txt',
                    help='Enter the path to the key file.(default: decrypted_file_task2.txt')

if __name__ == "__main__":
    my_variables = parser.parse_args()
    start_decrypt(*(vars(my_variables).values()))