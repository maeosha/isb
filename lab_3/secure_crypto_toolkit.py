import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

from file_work import *

iv = os.urandom(16)

def generation_keys(path_to_serialize_symmetric_key: str, path_to_serialize_public_key: str, path_to_serialize_private_key: str):
    key: bytes = b"1" * 16

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

    symmetric_key = private_key.decrypt(encrypt_symmetric_key,
                                            asymmetric_padding.OAEP(mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                                                algorithm=hashes.SHA256(),label=None
                                            )
                                        )

    padder = padding.ANSIX923(128).padder()
    padded_text = padder.update(text) + padder.finalize()


    cipher = Cipher(
        algorithms.AES(symmetric_key),
        modes.CBC(iv)
    )
    encryptor = cipher.encryptor()
    c_text = encryptor.update(padded_text) + encryptor.finalize()

    write_encrypt_text_to_file(path_to_encrypted_text, c_text)


def data_decrypt(path_to_encrypted_text: str, path_to_private_key: str, path_to_symmetric_key: str, path_to_decrypted_text: str):
    encrypt_symmetric_key: bytes = deserialize_symmetric_key(path_to_symmetric_key)
    encrypted_text: bytes = read_from_text_file(path_to_encrypted_text)
    private_key = deserialize_private_key(path_to_private_key)

    symmetric_key = private_key.decrypt(encrypt_symmetric_key,
                                            asymmetric_padding.OAEP(mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                                                algorithm=hashes.SHA256(),label=None
                                            )
                                        )

    cipher = Cipher(
        algorithms.AES(symmetric_key),
        modes.CBC(iv)
    )

    decryptor = cipher.decryptor()

    dc_text = decryptor.update(encrypted_text) + decryptor.finalize()

    unpadder = padding.ANSIX923(128).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()

    print(unpadded_dc_text.decode("utf-8"))

    write_encrypt_text_to_file(path_to_decrypted_text, unpadded_dc_text)

generation_keys("symmetric_key.txt", "public.pem", "private.pem")
data_encrypt("text.txt", "private.pem", "symmetric_key.txt", "encrypted_text.txt")
data_decrypt("encrypted_text.txt", "private.pem", "symmetric_key.txt", "decrypted_text.txt")
