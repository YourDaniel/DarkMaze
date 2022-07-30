def lower_first_letter(description: str) -> str:
    return description[:1].lower() + description[1:]


def debug(msg):
    with open('debug_file.txt', 'a') as f:
        f.write(msg + '\n')
