"""

Module for reporting errors

"""

import sys

from timoninterpreter.source_readers import FileReader


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

    def __init__(self, file_pos, message):
        super().__init__(message)
        self.file_pos = file_pos


class SyntacticError(InterpreterError):
    """Error raised when syntax is wrong"""

    def __init__(self, token, message):
        super().__init__(message)
        self.token = token


# Reporting


MAX_CHAR_SIDE_PEEK = 30


def _read_snippet(file_pos):
    left_bound = max(0, file_pos.get_line_pos() - MAX_CHAR_SIDE_PEEK)
    left_chars_num = file_pos.get_line_pos() - left_bound

    with FileReader(file_pos.get_file_path()) as source_reader:
        left_chars = source_reader.peek(-left_chars_num, file_pos.get_absolute_pos())
        middle_right_chars = source_reader.peek(1 + MAX_CHAR_SIDE_PEEK, file_pos.get_absolute_pos())

    return (left_chars + middle_right_chars).partition('\n')[0], left_chars_num


def report_generic_error(error_type, message, stream=sys.stdout):
    print("{} error: {}".format(error_type, message), file=stream)


def _report_positional_error(error_type, file_pos, message, stream=sys.stdout):
    file_name = file_pos.get_file_path().rpartition('/')[2]
    print("{}:{}:{}: {} error: {}".format(file_name, file_pos.get_line_num(), file_pos.get_line_pos(), error_type,
                                          message),
          file=stream)

    snippet, left_chars_num = _read_snippet(file_pos)
    print(snippet, file=stream)

    marker = " " * left_chars_num + "^"
    print(marker, file=stream)


def _report_positional_warning(warning_type, file_pos, message, action, stream=sys.stdout):
    file_name = file_pos.get_file_path().rpartition('/')[2]
    print("{}:{}:{}: {} warning: {}".format(file_name, file_pos.get_line_num(), file_pos.get_line_pos(), warning_type,
                                            message),
          file=stream)
    print(action, file=stream)

    snippet, left_chars_num = _read_snippet(file_pos)
    print(snippet, file=stream)

    marker = " " * left_chars_num + "^"
    print(marker, file=stream)


def report_lexical_error(file_pos, message, stream=sys.stdout):
    _report_positional_error("Lexical", file_pos, message, stream)


def report_lexical_warning(file_pos, message, action, stream=sys.stdout):
    _report_positional_warning("Lexical", file_pos, message, action, stream)


def report_syntactic_error(token, message, stream=sys.stdout):
    _report_positional_error("Syntactic", token.get_file_pos(), message, stream)


def report_syntactic_warning(token, message, action, stream=sys.stdout):
    _report_positional_warning("Syntactic", token.get_file_pos(), message, action, stream)
