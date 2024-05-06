import argparse
import os

from secure_crypto_toolkit import start_work

parser = argparse.ArgumentParser()


parser.add_argument('--path_to_symmetric_key',
                    type=str,
                    default=os.path.join("symmetric_key.txt"),
                    help='Enter the path to the symmetric key file.(default: symmetric_key.txt')


parser.add_argument('--path_to_public_key',
                    type=str,
                    default=os.path.join("public.pem"),
                    help='Enter the path to the public key file.(default: public.pem')

parser.add_argument('--path_to_private_key',
                    type=str,
                    default=os.path.join("private.pem"),
                    help='Enter the path to the private key file.(default: private.pem')

parser.add_argument('--path_to_text',
                    type=str,
                    default=os.path.join("text.txt"),
                    help='Enter the path to the text file.(default: text.txt)')

parser.add_argument('--path_to_encrypt_text',
                    type=str,
                    default=os.path.join("encrypted_text.txt"),
                    help='Enter the path to the encrypted text file.(default: encrypted_text.txt')

parser.add_argument('--path_to_decrypt_text',
                    type=str,
                    default=os.path.join("decrypted_text.txt"),
                    help='Enter the path to the decrypted text file.(default: encrypted_text.txt')

parser.add_argument('--size_key',
                    type=int,
                    default=128,
                    help='select the bit size for the symmetric key: 128 bits, 192 bits, 256 bits .(default: 128 bits)')

parser.add_argument('--work_mode',
                    type=str,
                    default='123',
                    help='Select the operating mode: 1 - hybrid System Key Generation, 2 - data encryption by a hybrid system, 3 - data decryption by a hybrid system. '
                         'You can select several modes by specifying them in order without spaces'
                         'default: 123(hybrid system key generation, data encryption by a hybrid system, data decryption by a hybrid system)')



if __name__ == "__main__":
    my_variables = parser.parse_args()
    start_work(*vars(my_variables).values())