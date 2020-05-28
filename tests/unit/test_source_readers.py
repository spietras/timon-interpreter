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
        self.file_reader.get(2)
        self.assertEqual('', self.file_reader.get())

    def test_get_multiple(self):
        self.assertEqual('ab', self.file_reader.get(2))

    def test_get_more_than_available(self):
        self.assertEqual('ab', self.file_reader.get(10))
        self.assertEqual('', self.file_reader.get())

    def test_get_negative(self):
        self.assertRaises(ValueError, self.file_reader.get, -10)

    def tearDown(self):
        self.file_reader.close()


class FileReaderPeekTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_open = make_mock_open(self, 'ab')

        self.file_reader = FileReader("whatever")
        self.file_reader.open()

    def test_peek_not_consume(self):
        self.assertEqual('a', self.file_reader.peek())
        self.assertEqual('a', self.file_reader.get())

    def test_peek_end(self):
        self.file_reader.get(2)
        self.assertEqual('', self.file_reader.peek())

    def test_peek_multiple(self):
        self.assertEqual('ab', self.file_reader.peek(2))

    def test_peek_more_than_available(self):
        self.assertEqual('ab', self.file_reader.peek(10))

    def test_peek_negative(self):
        self.file_reader.get(1)
        self.assertEqual('a', self.file_reader.peek(-1))

    def test_peek_negative_multiple(self):
        self.file_reader.get(2)
        self.assertEqual('ab', self.file_reader.peek(-2))

    def test_peek_negative_more_than_available(self):
        self.file_reader.get(2)
        self.assertEqual('ab', self.file_reader.peek(-10))

    def test_peek_with_start_position(self):
        self.assertEqual('b', self.file_reader.peek(1, 1))

    def test_peek_with_start_position_negative(self):
        self.assertRaises(ValueError, self.file_reader.peek, 1, -10)

    def test_peek_with_start_position_after_end(self):
        self.assertRaises(ValueError, self.file_reader.peek, -1, 10)

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
        self.file_reader.get(11)
        self.assertEqual(4, self.file_reader.get_file_pos().get_line_num())
        self.assertEqual(5, self.file_reader.get_file_pos().get_line_pos())
        self.assertEqual(11, self.file_reader.get_file_pos().get_absolute_pos())

    def test_positions_not_advance_at_end(self):
        self.file_reader.get(17)
        self.assertEqual(4, self.file_reader.get_file_pos().get_line_num())
        self.assertEqual(11, self.file_reader.get_file_pos().get_line_pos())
        self.assertEqual(17, self.file_reader.get_file_pos().get_absolute_pos())

        self.file_reader.get()

        self.assertEqual(4, self.file_reader.get_file_pos().get_line_num())
        self.assertEqual(11, self.file_reader.get_file_pos().get_line_pos())
        self.assertEqual(17, self.file_reader.get_file_pos().get_absolute_pos())

    def tearDown(self):
        self.file_reader.close()


class FileReaderRewindTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_open = make_mock_open(self, 'aaaaaaaaaaaa')

        self.file_reader = FileReader("whatever")
        self.file_reader.open()

    def test_rewind_backward(self):
        self.file_reader.get()
        self.file_reader.checkpoint()
        self.file_reader.get(3)
        self.file_reader.rewind_backward()

        self.assertEqual(1, self.file_reader.get_file_pos().get_line_num())
        self.assertEqual(1, self.file_reader.get_file_pos().get_line_pos())
        self.assertEqual(1, self.file_reader.get_file_pos().get_absolute_pos())

    def test_rewind_forward(self):
        self.file_reader.get()
        self.file_reader.checkpoint()
        self.file_reader.get(3)
        self.file_reader.rewind_backward()
        self.file_reader.rewind_forward()

        self.assertEqual(1, self.file_reader.get_file_pos().get_line_num())
        self.assertEqual(4, self.file_reader.get_file_pos().get_line_pos())
        self.assertEqual(4, self.file_reader.get_file_pos().get_absolute_pos())

    def test_rewind_backward_without_checkpoint(self):
        self.file_reader.get()
        self.file_reader.rewind_backward()

        self.assertEqual(1, self.file_reader.get_file_pos().get_line_num())
        self.assertEqual(1, self.file_reader.get_file_pos().get_line_pos())
        self.assertEqual(1, self.file_reader.get_file_pos().get_absolute_pos())

    def test_rewind_forward_without_checkpoint(self):
        self.file_reader.get()
        self.file_reader.rewind_forward()

        self.assertEqual(1, self.file_reader.get_file_pos().get_line_num())
        self.assertEqual(1, self.file_reader.get_file_pos().get_line_pos())
        self.assertEqual(1, self.file_reader.get_file_pos().get_absolute_pos())

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
