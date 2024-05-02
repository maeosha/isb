import os

from file_work import serialize_symmetric_key

def generation_keys(path_to_serialize_symmetric_key: str, path_to_serialize_public_key: str, path_to_serialize_privete_key: str):
    key: bytes = os.urandom(16)
    serialize_symmetric_key(path_to_serialize_symmetric_key, key)
