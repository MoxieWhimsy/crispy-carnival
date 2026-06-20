import os
import shutil


def clear_and_copy(source: str, destination: str):
    if not os.path.isdir(source):
        raise TypeError("Source must be a directory")
    shutil.rmtree(destination, ignore_errors=True)
    os.mkdir(destination)
    contents = os.listdir(source)
    if contents is None or len(contents) == 0:
        return
    directories = filter(lambda x: os.path.isdir(os.path.join(source, x)), contents)
    files = filter(lambda x: os.path.isfile(os.path.join(source, x)), contents)
    for directory in directories:
        directory_path = os.path.join(destination, directory)
        clear_and_copy(os.path.join(source, directory), directory_path)
    for file in files:
        shutil.copy(os.path.join(source, file), destination)
