import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

from file_work import *

iv = os.urandom(16)


def decrypt_symmetric_key(private_key, encrypt_symmetric_key: bytes) -> bytes:
    symmetric_key = private_key.decrypt(encrypt_symmetric_key,
                                            asymmetric_padding.OAEP(mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                                                algorithm=hashes.SHA256(),label=None
                                            )
                                        )

    return symmetric_key


def get_cipher(symmetric_key: bytes):
    cipher = Cipher(
        algorithms.AES(symmetric_key),
        modes.CBC(iv)
    )

    return cipher


def generation_keys(path_to_serialize_symmetric_key: str, path_to_serialize_public_key: str, path_to_serialize_private_key: str):
    key: bytes = os.urandom(16)

    keys = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
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

    serialize_symmetric_key(path_to_serialize_symmetric_key, encrypted_key)


def data_encrypt(path_to_text: str, path_to_private_key: str, path_to_symmetric_key: str, path_to_encrypted_text: str):
    text: bytes = read_from_text_file(path_to_text)
    private_key = deserialize_private_key(path_to_private_key)
    encrypt_symmetric_key: bytes = deserialize_symmetric_key(path_to_symmetric_key)

    symmetric_key = decrypt_symmetric_key(private_key, encrypt_symmetric_key)

    padder = padding.ANSIX923(128).padder()
    padded_text = padder.update(text) + padder.finalize()

    cipher = get_cipher(symmetric_key)

    encryptor = cipher.encryptor()
    c_text = encryptor.update(padded_text) + encryptor.finalize()

    write_encrypt_text_to_file(path_to_encrypted_text, c_text)


def data_decrypt(path_to_encrypted_text: str, path_to_private_key: str, path_to_symmetric_key: str, path_to_decrypted_text: str):
    encrypt_symmetric_key: bytes = deserialize_symmetric_key(path_to_symmetric_key)
    encrypted_text: bytes = read_from_text_file(path_to_encrypted_text)
    private_key = deserialize_private_key(path_to_private_key)

    symmetric_key = decrypt_symmetric_key(private_key, encrypt_symmetric_key)

    cipher = get_cipher(symmetric_key)

    decryptor = cipher.decryptor()
    dc_text = decryptor.update(encrypted_text) + decryptor.finalize()

    unpadder = padding.ANSIX923(128).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()

    write_encrypt_text_to_file(path_to_decrypted_text, unpadded_dc_text)


def start_work(path_to_symmetric_key: str,
               path_to_public_key: str,
               path_to_private_key: str,
               path_to_text: str,
               path_to_encrypted_text: str,
               path_to_decrypted_text: str):
    generation_keys(path_to_symmetric_key, path_to_public_key, path_to_private_key)
    data_encrypt(path_to_text, path_to_private_key, path_to_symmetric_key, path_to_encrypted_text)
    data_decrypt(path_to_encrypted_text, path_to_private_key, path_to_symmetric_key, path_to_decrypted_text)
