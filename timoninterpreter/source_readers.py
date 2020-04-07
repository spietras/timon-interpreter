"""

Source stream readers

"""


class FileReader:
    """
    Class for reading files

    Attributes:
        file_path: path to the file
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self._file = None

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
            next character
        """

        position = self._file.tell()  # position from the beginning of the file
        character = self._file.read(1)
        self._file.seek(position, 0)  # set previous position, explicitly from the beginning of the file
        return character

    def get(self):
        """
        Get next character and consume it

        Returns:
            next character
        """

        return self._file.read(1)
