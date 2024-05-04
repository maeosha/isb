import logging

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def serialize_symmetric_key(path_to_serialize_symmetric_key: str, key: bytes):
    try:
        with open(path_to_serialize_symmetric_key, 'wb') as key_file:
            key_file.write(key)
    except OSError as error:
        logging.warning(error)

    except Exception as error:
        logging.warning(error)

def serialize_asymmetric_key(path_to_serialize_public_key: str, path_to_serialize_private_key: str, public_key, private_key):
    try:
        with open(path_to_serialize_public_key, 'wb') as key_file:
            key_file.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo)
            )

        with open(path_to_serialize_private_key, "wb") as key_file:
            key_file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption())
            )

    except OSError as error:
        logging.warning(error)

    except Exception as error:
        logging.warning(error)


def read_from_text_file(path_to_file: str) -> str:
    try:
        with open(path_to_file, "r", encoding="utf-8") as text_file:
            text = text_file.read()

    except OSError as error:
        logging.warning(error)

    except Exception as error:
        logging.warning(error)

    return text


def deserialize_private_key(path_to_private):
    try:
        with open(path_to_private, 'rb') as pem_in:
            private_key: bytes = pem_in.read()
            d_private_key = load_pem_private_key(private_key, password=None)

    except OSError as error:
        logging.warning(error)

    except Exception as error:
        logging.warning(error)

    return d_private_key


def deserialize_symmetric_key(path_to_symmetric_key) -> bytes:
    try:
        with open(path_to_symmetric_key, "rb", encoding="utf-8") as key_file:
            key = key_file.read()

    except OSError as error:
        logging.warning(error)

    except Exception as error:
        logging.warning(error)

    return key


def write_encrypt_text_to_file(path_to_file: str, encrypted_text):
    try:
        with open(path_to_file, 'w') as text_file:
            text_file.write(encrypted_text)

    except OSError as error:
        logging.warning(error)

    except Exception as error:
        logging.warning(error)

