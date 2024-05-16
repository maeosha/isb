import logging

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def write_to_file(path_to_file: str, content: bytes) -> None:
    """
    Writes content to a specified file.

    :param path_to_file: The path to the file where content will be written.
    :param content: The content to write (key, encrypted text, decrypted text).
    :return: None
    """
    try:
        with open(path_to_file, 'wb') as file:
            file.write(content)
    except OSError as error:
        logging.warning(f"The file {path_to_file} does not exist!", error)
    except Exception as error:
        logging.warning(error)


def read_from_file(path_to_file: str) -> bytes:
    """
    Reads content from a specified file.

    :param path_to_file: The path to the file to read content from.
    :return: The content read from the file (key, encrypted text, decrypted text).
    """
    try:
        with open(path_to_file, "rb") as file:
            content = file.read()
    except OSError as error:
        logging.warning(f"The file {path_to_file} does not exist!", error)
        content = b''  # Return an empty bytes object in case of error
    except Exception as error:
        logging.warning(error)
        content = b''  # Return an empty bytes object in case of error

    return content


def serialize_asymmetric_key(
    path_to_serialize_public_key: str,
    path_to_serialize_private_key: str,
    public_key,
    private_key
) -> None:
    """
    Serializes and writes the public and private keys to specified paths.

    :param path_to_serialize_public_key: The path to write the public key of the asymmetric key.
    :param path_to_serialize_private_key: The path to write the private key of the asymmetric key.
    :param public_key: The public key to serialize.
    :param private_key: The private key to serialize.
    :return: None
    """
    try:
        with open(path_to_serialize_public_key, 'wb') as key_file:
            key_file.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    except OSError as error:
        logging.warning(f"The file {path_to_serialize_public_key} does not exist!", error)
    except Exception as error:
        logging.warning(error)

    try:
        with open(path_to_serialize_private_key, "wb") as key_file:
            key_file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
    except OSError as error:
        logging.warning(f"The file {path_to_serialize_private_key} does not exist!", error)
    except Exception as error:
        logging.warning(error)


def deserialize_private_key(path_to_private: str):
    """
    Deserializes a private key from a specified path.

    :param path_to_private: The path to the file containing the private key.
    :return: The private key of the asymmetric algorithm.
    """
    try:
        with open(path_to_private, 'rb') as pem_in:
            private_key: bytes = pem_in.read()
            d_private_key = load_pem_private_key(private_key, password=None)
    except OSError as error:
        logging.warning(f"The file {path_to_private} does not exist!", error)
        d_private_key = None  # Return None in case of error
    except Exception as error:
        logging.warning(error)
        d_private_key = None  # Return None in case of error

    return d_private_key
