from __future__ import annotations

import contextlib
from textwrap import dedent
from types import TracebackType
from typing import TextIO, Optional, Type, TypeVar, Callable

from fwutil.WriteMode import WriteMode, open_text_write_file


class FileWriter(contextlib.AbstractContextManager):
    __NEW_LINE = "\n"

    def __init__(self, file: TextIO):
        self._file = file
        self._writes = 0

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]):
        self.close()
        return False

    def __has_buffered_lines(self) -> bool:
        return self._writes > 0

    def close(self):
        self._file.close()

    def write_line(self, text: str, indent="", new_lines: int = 0, clean=False):
        self.write_multiline(text, indent, clean, auto_newline=False)
        self.new_line(new_lines)

    def new_line(self, amount: int = 1):
        for i in range(0, amount):
            self._write(self.__NEW_LINE)

    def write_multiline(self, text: str, indent: str = "", strip_first_newline: bool = True, clean: bool = True,
                        auto_newline: bool = True):
        if auto_newline and self.__has_buffered_lines():
            self.new_line()

        if clean:
            lines = dedent(text).splitlines()
            if strip_first_newline and len(lines) > 1 and len(lines[0]) == 0:
                lines = lines[1:]

            text = self.__NEW_LINE.join([indent + line for line in lines])

        self._write(text)

    def write_list(self, text_list: [str], separator: str = ", ", indent: str = "", new_lines: int = 0, clean=False):
        self.write_line(separator.join(text_list), indent, new_lines, clean)

    T = TypeVar("T")

    def transform_and_write_list(self, items: [T], separator: str = ", ",
                                 transform: Callable[[T], str] = lambda val: str(val),
                                 indent: str = "",
                                 new_lines: int = 0,
                                 clean=False):
        return self.write_list([transform(item) for item in items], separator, indent, new_lines, clean)

    def _write(self, text: str):
        self._file.write(text)
        self._writes += 1


def open_file(path: str, write_mode: WriteMode = WriteMode.WRITE, mkdirs: bool = True) -> FileWriter:
    return FileWriter(open_text_write_file(path, write_mode, mkdirs))
