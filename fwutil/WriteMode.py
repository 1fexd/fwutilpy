import os
from enum import Enum
from typing import TextIO


class WriteMode(Enum):
    WRITE = "w"
    APPEND = "a"


def open_text_write_file(path: str, write_mode: WriteMode = WriteMode.WRITE, mkdirs: bool = True) -> TextIO:
    if mkdirs:
        abs_path = os.path.abspath(path)
        dir_name = os.path.dirname(abs_path)
        if not os.path.exists(abs_path) and not os.path.exists(dir_name):
            os.makedirs(dir_name)

    return open(path, write_mode.value)
