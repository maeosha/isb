import os

def read_from_file() -> str:
    """Read encrypted text from a file"""
    encrypted_text: str = ""
    with open(os.path.join("encrypted_file.txt"), "r") as file:
        for i in file:
            encrypted_text += i.replace('\n', '')

    return encrypted_text