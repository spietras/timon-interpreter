"""

Module for reporting errors

"""

import sys


# Exceptions


class InterpreterError(Exception):
    """
    Base class for errors

    Attributes:
        message - explanation of the error
    """

    def __init__(self, message):
        self.message = message


class LexicalError(InterpreterError):
    """Error raised when lexer can't tokenize input"""
    pass


# Reporting


LEXICAL_ERROR_HEADER = "Lexical error"
LEXICAL_WARNING_HEADER = "Lexical warning"

MAX_CHAR_SIDE_PEEK = 30


def _read_snippet(line_pos, absolute_pos, source_reader):
    left_bound = max(0, line_pos - MAX_CHAR_SIDE_PEEK)
    left_chars_num = line_pos - left_bound

    left_chars = source_reader.peek(-left_chars_num, absolute_pos)
    middle_right_chars = source_reader.peek(1 + MAX_CHAR_SIDE_PEEK, absolute_pos)

    return (left_chars + middle_right_chars).partition('\n')[0], left_chars_num


def report_lexical_error(line_num, line_pos, absolute_pos, source_reader, message, stream=sys.stdout):
    file_name = source_reader.file_path.rpartition('/')[2]
    print("{}:{}:{}: {}: {}".format(file_name, line_num, line_pos, LEXICAL_ERROR_HEADER, message), file=stream)

    snippet, left_chars_num = _read_snippet(line_pos, absolute_pos, source_reader)
    print(snippet, file=stream)

    marker = " " * left_chars_num + "^"
    print(marker, file=stream)


def report_lexical_warning(line_num, line_pos, absolute_pos, source_reader, message, action, stream=sys.stdout):
    file_name = source_reader.file_path.rpartition('/')[2]
    print("{}:{}:{}: {}: {}".format(file_name, line_num, line_pos, LEXICAL_WARNING_HEADER, message), file=stream)
    print(action, file=stream)

    snippet, left_chars_num = _read_snippet(line_pos, absolute_pos, source_reader)
    print(snippet, file=stream)

    marker = " " * left_chars_num + "^"
    print(marker, file=stream)
