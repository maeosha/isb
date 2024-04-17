from file_work import read_from_text_file_task2, read_from_key_file_task2, write_to_file
def get_stats(encrypted_text: str, key: list) -> str:
    """Calculating the percentage of letters meeting and decoding the text"""

    stats: dict = dict()

    for letter in sorted(set(encrypted_text)):
        stats[letter] = encrypted_text.count(letter)

    for i in range(len(stats)):
        count = 0
        for j in range(i + 1, len(stats)):
            if list(stats.items())[i][1] == list(stats.items())[j][1]:
                if ord(list(stats.items())[i][0]) > ord(list(stats.items())[j][0]):
                    stats[list(stats.items())[j][0]] += 0.01 + count
                else:
                    stats[list(stats.items())[i][0]] += 0.01 + count
                count += 0.01


    stats = dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))

    keys = list(stats.keys())
    i = 0

    for symbol, letter in zip(keys, key):
        encrypted_text = encrypted_text.replace(symbol, letter)

    return encrypted_text

def start_decrypt(path_to_key_file: str, path_to_text_file: str, path_to_decrypted_file: str) -> None:
    """the start of the program, the input gets the path to work with files"""
    encrypted_text: str = read_from_text_file_task2(path_to_text_file)
    key: list = read_from_key_file_task2(path_to_key_file)

    decrypted_text = get_stats(encrypted_text, key)

    write_to_file(decrypted_text, path_to_decrypted_file)
