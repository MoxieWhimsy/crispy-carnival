def strip_front_char(line: str) -> str:
    return line[1:].lstrip()  # remove the > or bullet and optional leading whitespace
