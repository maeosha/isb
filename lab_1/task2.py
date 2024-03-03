import os

def read_from_file() -> str:
    """Read encrypted text from a file"""
    encrypted_text: str = ""
    with open(os.path.join("encrypted_file.txt"), "r") as file:
        for i in file:
            encrypted_text += i.replace('\n', '')

    return encrypted_text

def get_stats(encrypted_text: str) -> tuple:
    """Calculating the percentage of letters meeting and decoding the text"""
    stats: dict = dict()
    ave_stats: str = " оаинетслвпкурдябмьызюйгщэчжъфщхц"

    for letter in encrypted_text:
        if letter in stats:
            stats[letter] += 1
        else:
            stats[letter] = 1

    for stat in stats:
        stats[stat] = stats[stat] / len(encrypted_text)

    stats = dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))
    keys = list(stats.keys())
    item = list(stats.items())
    i = 0

    for stat in ave_stats:
        encrypted_text = encrypted_text.replace(keys[i], stat)
        i += 1

    return ave_stats, item

