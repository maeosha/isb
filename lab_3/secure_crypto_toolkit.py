import os
import logging

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

from file_work import *

size_128_bit = 128
size_192_bit = 192
size_256_bit = 256
byte_size = 8
public_exponent = 65537
key_size = 2048

logging.basicConfig(level=logging.INFO)


def check_key_length(size_key: int) -> None:
    """
    Checks if the provided key size is valid.

    :param size_key: The size of the key in bits.
    :raises ValueError: If the key size is not 128, 192, or 256 bits.
    """
    if size_key not in [size_128_bit, size_192_bit, size_256_bit]:
        logging.warning("Select the correct key size!")
        raise ValueError("Invalid key size!")


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
    Executes the specified work modes.

    :param path_to_symmetric_key: Path to the symmetric key file.
    :param path_to_public_key: Path to the public key file.
    :param path_to_private_key: Path to the private key file.
    :param path_to_text: Path to the text file.
    :param path_to_encrypted_text: Path to the encrypted text file.
    :param path_to_decrypted_text: Path to the decrypted text file.
    :param iv: Initialization vector for encryption.
    :param size_key: Size of the symmetric key in bytes.
    :param work_modes: String containing modes to execute (e.g., '123').
    """
    for mode in work_modes:
        try:
            if mode == "1":
                generation_keys(path_to_symmetric_key, path_to_public_key, path_to_private_key, size_key)
                logging.info("The keys have been generated successfully!")
            elif mode == "2":
                data_encrypt(path_to_text, path_to_private_key, path_to_symmetric_key, path_to_encrypted_text, iv)
                logging.info("The text has been successfully encrypted!")
            elif mode == "3":
                data_decrypt(path_to_encrypted_text, path_to_private_key, path_to_symmetric_key, path_to_decrypted_text,
                             iv)
                logging.info("The text has been successfully decrypted!")
            else:
                raise ValueError(f"Invalid mode: {mode}")
        except Exception as error:
            logging.warning(f"An error occurred in mode {mode}: {error}")


def decrypt_symmetric_key(private_key, encrypt_symmetric_key: bytes) -> bytes:
    """
    Decrypts the symmetric key using the provided private key.

    :param private_key: The private RSA key.
    :param encrypt_symmetric_key: The encrypted symmetric key.
    :return: The decrypted symmetric key.
    """
    return private_key.decrypt(
        encrypt_symmetric_key,
        asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def get_cipher(symmetric_key: bytes, iv: bytes):
    """
    Creates a Cipher object for AES encryption/decryption.

    :param symmetric_key: The symmetric key.
    :param iv: The initialization vector.
    :return: The Cipher object.
    """
    return Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))


def generation_keys(path_to_serialize_symmetric_key: str, path_to_serialize_public_key: str,
                    path_to_serialize_private_key: str, size_key: int):
    """
    Generates and serializes symmetric and asymmetric keys.

    :param path_to_serialize_symmetric_key: Path to save the serialized symmetric key.
    :param path_to_serialize_public_key: Path to save the serialized public key.
    :param path_to_serialize_private_key: Path to save the serialized private key.
    :param size_key: Size of the symmetric key in bytes.
    :return: None
    """
    key = os.urandom(size_key)

    keys = rsa.generate_private_key(public_exponent, key_size)
    private_key = keys
    public_key = keys.public_key()

    serialize_asymmetric_key(path_to_serialize_public_key, path_to_serialize_private_key, public_key, private_key)

    encrypted_key = public_key.encrypt(
        key,
        asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    write_to_file(path_to_serialize_symmetric_key, encrypted_key)


def data_encrypt(path_to_text: str, path_to_private_key: str, path_to_symmetric_key: str, path_to_encrypted_text: str,
                 iv: bytes):
    """
    Encrypts text using a symmetric algorithm.

    :param path_to_text: Path to the plaintext file.
    :param path_to_private_key: Path to the private key file.
    :param path_to_symmetric_key: Path to the encrypted symmetric key file.
    :param path_to_encrypted_text: Path to save the encrypted text.
    :param iv: Initialization vector for encryption.
    """
    text = read_from_file(path_to_text)
    private_key = deserialize_private_key(path_to_private_key)
    encrypt_symmetric_key = read_from_file(path_to_symmetric_key)

    symmetric_key = decrypt_symmetric_key(private_key, encrypt_symmetric_key)

    padder = padding.ANSIX923(size_128_bit).padder()
    padded_text = padder.update(text) + padder.finalize()

    cipher = get_cipher(symmetric_key, iv)
    encryptor = cipher.encryptor()
    c_text = encryptor.update(padded_text) + encryptor.finalize()

    write_to_file(path_to_encrypted_text, c_text)


def data_decrypt(path_to_encrypted_text: str, path_to_private_key: str, path_to_symmetric_key: str,
                 path_to_decrypted_text: str, iv: bytes):
    """
    Decrypts text using a symmetric algorithm.

    :param path_to_encrypted_text: Path to the encrypted text file.
    :param path_to_private_key: Path to the private key file.
    :param path_to_symmetric_key: Path to the encrypted symmetric key file.
    :param path_to_decrypted_text: Path to save the decrypted text.
    :param iv: Initialization vector used during encryption.
    """
    encrypt_symmetric_key = read_from_file(path_to_symmetric_key)
    encrypted_text = read_from_file(path_to_encrypted_text)
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
    """
    Initiates the encryption or decryption process based on the specified mode.

    :param path_to_symmetric_key: Path to the symmetric key file.
    :param path_to_public_key: Path to the public key file.
    :param path_to_private_key: Path to the private key file.
    :param path_to_text: Path to the text file.
    :param path_to_encrypted_text: Path to the encrypted text file.
    :param path_to_decrypted_text: Path to the decrypted text file.
    :param size_key: Size of the symmetric key in bits.
    :param work_mode: Modes of operation (e.g., '1' for key generation, '2' for encryption, '3' for decryption).
    """
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
