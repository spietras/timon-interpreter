"""

Source stream readers

"""

import copy
import os


class FilePosition:
    def __init__(self, file_path):
        self._file_path = file_path
        self._line_num = 1
        self._line_pos = 0
        self._absolute_pos = 0

    def advance(self, characters):
        for character in characters:
            self._absolute_pos += 1
            self._line_pos += 1
            if character == '\n':
                self._line_num += 1
                self._line_pos = 0

    def get_line_num(self):
        return self._line_num

    def get_line_pos(self):
        return self._line_pos

    def get_absolute_pos(self):
        return self._absolute_pos

    def get_file_path(self):
        return self._file_path

    def __eq__(self, other):
        if not isinstance(other, FilePosition):
            return NotImplemented

        return (self._line_num == other._line_num and
                self._line_pos == other._line_pos and
                self._absolute_pos == other._absolute_pos and
                self._file_path == other._file_path)


class FileReader:
    """
    Class for reading files
    """

    def __init__(self, file_path):
        self._file_path = file_path
        self._file = None
        self._file_pos = FilePosition(self._file_path)
        self._backward_checkpoint = None
        self._forward_checkpoint = None

    def open(self):
        """
        Opens the file
        """

        self._file = open(self._file_path, "rt")

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
            self._file.seek(offset, os.SEEK_SET)

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
            self._file_pos.advance(characters)
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

    def checkpoint(self):
        """
        Creates position checkpoint that reader can be rewinded to
        """
        self._backward_checkpoint = copy.deepcopy(self._file_pos)

    def rewind_backward(self):
        """
        Rewinds to previous backward checkpoint (if exists) and sets forward checkpoint (as current position)
        """
        if self._backward_checkpoint is not None:
            self._forward_checkpoint = copy.deepcopy(self._file_pos)
            self._file_pos = copy.deepcopy(self._backward_checkpoint)

    def rewind_forward(self):
        """
        Rewinds to previous forward checkpoint (if exists) and resets forward checkpoint to None
        """
        if self._forward_checkpoint is not None:
            self._file_pos = copy.deepcopy(self._forward_checkpoint)
            self._forward_checkpoint = None

    def get_file_path(self):
        return copy.deepcopy(self._file_path)

    def get_file_pos(self):
        return copy.deepcopy(self._file_pos)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
