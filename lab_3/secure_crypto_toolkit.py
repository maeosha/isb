import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

from file_work import *

size_128_bit = 128
size_192_bit = 192
size_256_bit = 256
byte_size = 8
public_exponent=65537
key_size=2048

logging.basicConfig(level=logging.INFO)


def check_key_length(size_key: int) -> None:
    """
    checking the received key for belonging to 128, 192, 256 bit size
    :param size_key:
    :return:
    """
    try:
        if [size_128_bit, size_192_bit, size_256_bit].count(size_key) == 0:
            raise ValueError
    except ValueError:
        logging.warning("Select the correct key size!")
    except Exception as error:
        logging.warning(error)


def choose_mode(
        path_to_symmetric_key: str,
        path_to_public_key: str,
        path_to_private_key: str,
        path_to_text: str,
        path_to_encrypted_text: str,
        path_to_decrypted_text: str,
        iv: bytes,
        size_key: int,
        work_modes: str) -> None:
    """
    selecting the operating mode
    :param path_to_symmetric_key:
    :param path_to_public_key:
    :param path_to_private_key:
    :param path_to_text:
    :param path_to_encrypted_text:
    :param path_to_decrypted_text:
    :param iv:
    :param size_key:
    :param work_modes:
    :return:
    """
    for mode in work_modes:
        try:
            match mode:
                case "1":
                    generation_keys(path_to_symmetric_key, path_to_public_key, path_to_private_key, size_key)
                    logging.info("The keys have been generated successfully!")

                case "2":
                    data_encrypt(path_to_text, path_to_private_key, path_to_symmetric_key, path_to_encrypted_text, iv)
                    logging.info("The text has been successfully encrypted!")

                case "3":
                    data_decrypt(path_to_encrypted_text, path_to_private_key, path_to_symmetric_key, path_to_decrypted_text, iv)
                    logging.info("The text has been successfully decrypted")

                case _:
                    raise ValueError


        except Exception as error:
            logging.warning(error)


def decrypt_symmetric_key(private_key, encrypt_symmetric_key: bytes) -> bytes:
    """
    symmetric key encryption with an asymmetric algorithm
    :param private_key:
    :param encrypt_symmetric_key:
    :return symmetric_key:
    """
    symmetric_key = private_key.decrypt(encrypt_symmetric_key,
                                            asymmetric_padding.OAEP(mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                                                algorithm=hashes.SHA256(),label=None
                                            )
                                        )

    return symmetric_key


def get_cipher(symmetric_key: bytes, iv: bytes):
    """
    getting the encryption method
    :param symmetric_key:
    :param iv:
    :return cipher:
    """
    cipher = Cipher(
        algorithms.AES(symmetric_key),
        modes.CBC(iv)
    )

    return cipher


def generation_keys(path_to_serialize_symmetric_key: str, path_to_serialize_public_key: str, path_to_serialize_private_key: str, size_key: int):
    """
    generation and serialization of symmetric and asymmetric keys
    :param path_to_serialize_symmetric_key:
    :param path_to_serialize_public_key:
    :param path_to_serialize_private_key:
    :param size_key:
    :return:
    """
    key: bytes = os.urandom(size_key)

    keys = rsa.generate_private_key(
        public_exponent,
        key_size
    )

    private_key = keys
    public_key = keys.public_key()

    serialize_asymmetric_key(
        path_to_serialize_public_key,
        path_to_serialize_private_key,
        public_key,
        private_key
    )

    encrypted_key = public_key.encrypt(
        key,
        asymmetric_padding.OAEP(mgf=asymmetric_padding.MGF1(
            algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None)
    )

    write_to_file(path_to_serialize_symmetric_key, encrypted_key)


def data_encrypt(path_to_text: str, path_to_private_key: str, path_to_symmetric_key: str, path_to_encrypted_text: str, iv: bytes):
    """
    encryption of text using a symmetric algorithm
    :param path_to_text:
    :param path_to_private_key:
    :param path_to_symmetric_key:
    :param path_to_encrypted_text:
    :param iv:
    :return:
    """
    text: bytes = read_from_file(path_to_text)
    private_key = deserialize_private_key(path_to_private_key)
    encrypt_symmetric_key: bytes = read_from_file(path_to_symmetric_key)

    symmetric_key = decrypt_symmetric_key(private_key, encrypt_symmetric_key)

    padder = padding.ANSIX923(size_128_bit).padder()
    padded_text = padder.update(text) + padder.finalize()

    cipher = get_cipher(symmetric_key, iv)

    encryptor = cipher.encryptor()
    c_text = encryptor.update(padded_text) + encryptor.finalize()

    write_to_file(path_to_encrypted_text, c_text)



def data_decrypt(path_to_encrypted_text: str, path_to_private_key: str, path_to_symmetric_key: str, path_to_decrypted_text: str, iv: bytes):
    """
    decryption of text using a symmetric algorithm
    :param path_to_encrypted_text:
    :param path_to_private_key:
    :param path_to_symmetric_key:
    :param path_to_decrypted_text:
    :param iv:
    :return:
    """
    encrypt_symmetric_key: bytes = read_from_file(path_to_symmetric_key)
    encrypted_text: bytes = read_from_file(path_to_encrypted_text)
    private_key = deserialize_private_key(path_to_private_key)

    symmetric_key = decrypt_symmetric_key(private_key, encrypt_symmetric_key)

    cipher = get_cipher(symmetric_key, iv)

    decryptor = cipher.decryptor()
    dc_text = decryptor.update(encrypted_text) + decryptor.finalize()

    unpadder = padding.ANSIX923(size_128_bit).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()

    write_to_file(path_to_decrypted_text, unpadded_dc_text)


def start_work(path_to_symmetric_key: str,
               path_to_public_key: str,
               path_to_private_key: str,
               path_to_text: str,
               path_to_encrypted_text: str,
               path_to_decrypted_text: str,
               size_key: int,
               work_mode: str):
    iv = os.urandom(size_128_bit // byte_size)
    check_key_length(size_key)
    size_key_bytes = size_key // byte_size
    choose_mode(
        path_to_symmetric_key,
        path_to_public_key,
        path_to_private_key,
        path_to_text,
        path_to_encrypted_text,
        path_to_decrypted_text,
        iv,
        size_key_bytes,
        work_mode,
    )
