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


class FileReaderEndedTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_open = make_mock_open(self, 'a')

        self.file_reader = FileReader("whatever")
        self.file_reader.open()

    def test_ended_not_on_end(self):
        self.assertFalse(self.file_reader.ended())

    def test_ended_on_end(self):
        self.file_reader.get()
        self.assertTrue(self.file_reader.ended())

    def tearDown(self):
        self.file_reader.close()


class FileReaderOpenedTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_open = make_mock_open(self, 'a')

        self.file_reader = FileReader("whatever")

    def test_opened_before_open(self):
        self.assertFalse(self.file_reader.opened())

    def test_opened_after_open(self):
        self.file_reader.open()
        self.assertTrue(self.file_reader.opened())
        self.file_reader.close()

    def test_opened_after_close(self):
        self.file_reader.open()
        self.file_reader.close()
        self.assertFalse(self.file_reader.opened())


class FileReaderPositionsTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_open = make_mock_open(self, 'a\na\na\nfourth line')

        self.file_reader = FileReader("whatever")
        self.file_reader.open()

    def test_positions_in_line(self):
        for _ in range(11):
            self.file_reader.get()
        self.assertEqual(4, self.file_reader.line_num)
        self.assertEqual(5, self.file_reader.line_pos)
        self.assertEqual(11, self.file_reader.absolute_pos)

    def test_positions_not_advance_at_end(self):
        for _ in range(17):
            self.file_reader.get()
        self.assertEqual(4, self.file_reader.line_num)
        self.assertEqual(11, self.file_reader.line_pos)
        self.assertEqual(17, self.file_reader.absolute_pos)

        self.file_reader.get()

        self.assertEqual(4, self.file_reader.line_num)
        self.assertEqual(11, self.file_reader.line_pos)
        self.assertEqual(17, self.file_reader.absolute_pos)

    def tearDown(self):
        self.file_reader.close()


class FileReaderWithTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_open = make_mock_open(self, 'abc')

    def test_opened_in_with(self):
        with FileReader("whatever") as fr:
            self.assertTrue(fr.opened())

    def test_closed_after_with(self):
        with FileReader("whatever") as fr:
            fr.get()

        self.assertFalse(fr.opened())
