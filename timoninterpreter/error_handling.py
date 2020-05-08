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
    def __init__(self, line_num, line_pos, absolute_pos, source_reader, message):
        super().__init__(message)
        self.line_num = line_num
        self.line_pos = line_pos
        self.absolute_pos = absolute_pos
        self.source_reader = source_reader


# Reporting


MAX_CHAR_SIDE_PEEK = 30


def _read_snippet(line_pos, absolute_pos, source_reader):
    left_bound = max(0, line_pos - MAX_CHAR_SIDE_PEEK)
    left_chars_num = line_pos - left_bound

    left_chars = source_reader.peek(-left_chars_num, absolute_pos)
    middle_right_chars = source_reader.peek(1 + MAX_CHAR_SIDE_PEEK, absolute_pos)

    return (left_chars + middle_right_chars).partition('\n')[0], left_chars_num


def report_generic_error(error_type, message, stream=sys.stdout):
    print("{} error: {}".format(error_type, message), file=stream)


def _report_positional_error(error_type, line_num, line_pos, absolute_pos, source_reader, message, stream=sys.stdout):
    file_name = source_reader.file_path.rpartition('/')[2]
    print("{}:{}:{}: {} error: {}".format(file_name, line_num, line_pos, error_type, message), file=stream)

    snippet, left_chars_num = _read_snippet(line_pos, absolute_pos, source_reader)
    print(snippet, file=stream)

    marker = " " * left_chars_num + "^"
    print(marker, file=stream)


def _report_positional_warning(warning_type, line_num, line_pos, absolute_pos, source_reader, message, action, stream=sys.stdout):
    file_name = source_reader.file_path.rpartition('/')[2]
    print("{}:{}:{}: {} warning: {}".format(file_name, line_num, line_pos, warning_type, message), file=stream)
    print(action, file=stream)

    snippet, left_chars_num = _read_snippet(line_pos, absolute_pos, source_reader)
    print(snippet, file=stream)

    marker = " " * left_chars_num + "^"
    print(marker, file=stream)


def report_lexical_error(line_num, line_pos, absolute_pos, source_reader, message, stream=sys.stdout):
    _report_positional_error("Lexical", line_num, line_pos, absolute_pos, source_reader, message, stream)


def report_lexical_warning(line_num, line_pos, absolute_pos, source_reader, message, action, stream=sys.stdout):
    _report_positional_warning("Lexical", line_num, line_pos, absolute_pos, source_reader, message, action, stream)
