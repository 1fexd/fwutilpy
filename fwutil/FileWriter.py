from textwrap import dedent
from typing import TextIO


class FileWriter:
    def __init__(self, file: TextIO):
        self.file = file

    def write_text_new_line(self, text: str, indent="", clean=False):
        self.write(text, indent, clean)
        self.write_new_line(1)

    def write_new_line(self, amount: int = 1):
        for i in range(0, amount):
            self.file.write("\n")

    def write(self, text: str, indent="", strip_first_newline=True, clean=False):
        if clean:
            lines = dedent(text).splitlines()
            if strip_first_newline and len(lines) > 1 and lines[0] == '':
                lines = lines[1:]

            text = "\n".join([indent + line for line in lines])

        self.file.write(text)

    def close(self):
        self.file.close()


def write_file(path: str) -> FileWriter:
    return FileWriter(open(path, "w"))
