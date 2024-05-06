import logging

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def write_to_file(path_to_file: str, content: bytes):
    try:
        with open(path_to_file, 'wb') as file:
            file.write(content)
    except OSError as error:
        logging.warning(error)

    except Exception as error:
        logging.warning(error)


def read_from_file(path_to_file: str) -> bytes:
    try:
        with open(path_to_file, "rb") as file:
            content = file.read()

    except OSError as error:
        logging.warning(error)

    except Exception as error:
        logging.warning(error)

    return content


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

