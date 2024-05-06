import argparse
import os

from secure_crypto_toolkit import start_work

parser = argparse.ArgumentParser()


parser.add_argument('--path_to_symmetric_key',
                    type=str,
                    default=os.path.join("symmetric_key.txt"),
                    help='Enter the path to the random sequence file.(default: stats/random_sequence.json')


parser.add_argument('--path_to_public_key',
                    type=str,
                    default=os.path.join("public.pem"),
                    help='Enter the path to the stats file.(default: stats/stats.txt')

parser.add_argument('--path_to_private_key',
                    type=str,
                    default=os.path.join("private.pem"),
                    help='Enter the path to the stats file.(default: stats/stats.txt')

parser.add_argument('--path_to_text',
                    type=str,
                    default=os.path.join("text.txt"),
                    help='Enter the path to the stats file.(default: stats/stats.txt')

parser.add_argument('--path_to_encrypt_text',
                    type=str,
                    default=os.path.join("encrypted_text.txt"),
                    help='Enter the path to the stats file.(default: stats/stats.txt')

parser.add_argument('--path_to_decrypt_text',
                    type=str,
                    default=os.path.join("decrypted_text.txt"),
                    help='Enter the path to the stats file.(default: stats/stats.txt')

parser.add_argument('--size_key',
                    type=int,
                    default=128,
                    help='Enter the path to the stats file.(default: stats/stats.txt')

parser.add_argument('--work_mode',
                    type=str,
                    default='123',
                    help='Enter the path to the stats file.(default: stats/stats.txt')


if __name__ == "__main__":
    my_variables = parser.parse_args()
    start_work(*vars(my_variables).values())