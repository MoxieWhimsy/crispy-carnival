def strip_front_char(line: str) -> str:
    return line[1:].lstrip()  # remove the > or bullet and optional leading whitespace

def get_header_level(line: str) -> int:
    count: int = 0
    while line.startswith("#"):
        count += 1
        line = line[1:]
    return count

def remove_up_to_period(line: str) -> str:
    index = line.find(".")
    if index == -1:
        return line
    return line[index+1:].lstrip()