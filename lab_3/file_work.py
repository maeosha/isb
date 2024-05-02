import logging

from cryptography.hazmat.primitives import serialization


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
