import logging


def serialize_symmetric_key(path_to_serialize_symmetric_key: str, key: bytes):
    try:
        with open(path_to_serialize_symmetric_key, 'wb') as key_file:
            key_file.write(key)
    except OSError as error:
        logging.warning(error)

    except Exception as error:
        logging.warning(error)
