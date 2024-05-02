import os

from cryptography.hazmat.primitives.asymmetric import rsa

from file_work import serialize_symmetric_key, serialize_asymmetric_key

def generation_keys(path_to_serialize_symmetric_key: str, path_to_serialize_public_key: str, path_to_serialize_privete_key: str):
    key: bytes = os.urandom(16)
    serialize_symmetric_key(path_to_serialize_symmetric_key, key)

    keys = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    private_key = keys
    public_key = keys.public_key()
    serialize_asymmetric_key(path_to_serialize_public_key,
                             path_to_serialize_privete_key,
                             public_key,
                             private_key)