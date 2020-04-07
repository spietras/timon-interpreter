import unittest
import unittest.mock as mock
import io

from timoninterpreter.source_readers import FileReader


def make_mock_open(test_case, data):
    patcher = mock.patch('builtins.open')
    test_case.addCleanup(patcher.stop)
    mock_open = patcher.start()
    mock_open.return_value = io.StringIO(data)
    return mock_open


class FileReaderOpenTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_open = make_mock_open(self, '')

        self.file_reader = FileReader("whatever")

    def test_file_not_existing(self):
        self.mock_open.side_effect = FileNotFoundError()
        self.assertRaises(FileNotFoundError, self.file_reader.open)


class FileReaderGetTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_open = make_mock_open(self, 'ab')

        self.file_reader = FileReader("whatever")
        self.file_reader.open()

    def test_get_consume(self):
        self.assertEqual('a', self.file_reader.get())
        self.assertEqual('b', self.file_reader.get())

    def test_get_end(self):
        self.file_reader.get()
        self.file_reader.get()
        self.assertEqual('', self.file_reader.get())

    def tearDown(self):
        self.file_reader.close()


class FileReaderPeekTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_open = make_mock_open(self, 'a')

        self.file_reader = FileReader("whatever")
        self.file_reader.open()

    def test_peek_not_consume(self):
        self.assertEqual('a', self.file_reader.peek())
        self.assertEqual('a', self.file_reader.get())

    def test_peek_end(self):
        self.file_reader.get()
        self.assertEqual('', self.file_reader.peek())

    def tearDown(self):
        self.file_reader.close()
