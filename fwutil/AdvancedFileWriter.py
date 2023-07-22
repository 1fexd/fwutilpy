from __future__ import annotations

import os
from typing import TextIO

from fwutil.FileWriter import FileWriter
from fwutil.WriteMode import WriteMode, open_text_write_file


class AdvancedFileWriter(FileWriter):
    def __init__(self, file: TextIO, clear_buffer_on_flush: bool = False):
        super().__init__(file)

        self.line_buffer = []
        self.clear_buffer_on_flush = clear_buffer_on_flush

    def flush(self):
        self._file.flush()
        os.fsync(self._file)

        if self.clear_buffer_on_flush:
            self.line_buffer.clear()

    def get_write_count(self) -> int:
        return self._writes

    def file(self) -> TextIO:
        return self._file

    def _write(self, text: str):
        super()._write(text)
        self.line_buffer.append(text)


def open_file_advanced(path: str, write_mode: WriteMode = WriteMode.WRITE,
                       mkdirs: bool = True,
                       clear_buffer_on_flush: bool = False) -> AdvancedFileWriter:
    return AdvancedFileWriter(open_text_write_file(path, write_mode, mkdirs), clear_buffer_on_flush)
