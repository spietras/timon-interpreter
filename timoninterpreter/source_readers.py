"""

Source stream readers

"""

import os


class FileReader:
    """
    Class for reading files

    Attributes:
        file_path: path to the file
        line_num: current line of the file
        line_pos: current position in line
        absolute_pos: current absolute position in file
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self._file = None
        self.line_num = 1
        self.line_pos = 0
        self.absolute_pos = 0

    def open(self):
        """
        Opens the file
        """

        self._file = open(self.file_path, "rt")

    def close(self):
        """
        Closes the file
        """

        self._file.close()
        self._file = None

    def peek(self, n=1, start_pos=None):
        """
        Get n next (if n positive) or previous (if n negative) characters without consuming them

        Returns:
            characters (can be less than n if file ended)
        """

        position = self._file.tell()  # position from the beginning of the file

        self._file.seek(0, os.SEEK_END)
        file_size = self._file.tell()

        if start_pos is None:
            start_pos = position

        if start_pos < 0 or start_pos > file_size:
            raise ValueError("Start position outside of range. Only possible range is [0, {}]".format(file_size))

        self._file.seek(start_pos, os.SEEK_SET)

        if n < 0:
            n = -n
            offset = max(0, start_pos - n)
            self._file.seek(offset,  os.SEEK_SET)

        characters = self._file.read(n)
        self._file.seek(position, os.SEEK_SET)  # set previous position, explicitly from the beginning of the file

        return characters

    def get(self, n=1):
        """
        Get next n characters and consume them

        Returns:
            next characters (can be less than n if file ended)
        """

        if n < 0:
            raise ValueError("Get size can't be negative")

        characters = self._file.read(n)
        if characters:
            self._advance_positions(characters)
        return characters

    def ended(self):
        """
        Returns:
            True if there are no more characters to read
        """

        return self.peek() == ''

    def opened(self):
        """
        Returns:
            True if file is opened
        """

        return self._file is not None

    def _advance_positions(self, characters):
        for character in characters:
            self.absolute_pos += 1
            self.line_pos += 1
            if character == '\n':
                self.line_num += 1
                self.line_pos = 0

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
