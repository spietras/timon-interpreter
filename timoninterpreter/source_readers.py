"""

Source stream readers

"""


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

    def peek(self):
        """
        Get next character without consuming it

        Returns:
            next character or empty string if file ended
        """

        position = self._file.tell()  # position from the beginning of the file
        character = self._file.read(1)
        self._file.seek(position, 0)  # set previous position, explicitly from the beginning of the file
        return character

    def get(self):
        """
        Get next character and consume it

        Returns:
            next character or empty string if file ended
        """

        character = self._file.read(1)
        if character:
            self._advance_positions(character)
        return character

    def ended(self):
        """
        Returns:
            True if there are no more characters to read
        """

        return self.peek() == ''

    def _advance_positions(self, character):
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
