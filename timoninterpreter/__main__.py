"""

Main script

"""

import argparse

from timoninterpreter.source_readers import FileReader
from timoninterpreter.lexical_analysis import Lexer
from timoninterpreter import tokens
from timoninterpreter import error_handling


def run(path):
    try:
        read_tokens = []

        with FileReader(path) as fr:
            lex = Lexer(fr)
            while not (read_tokens and read_tokens[-1].type == tokens.TokenType.END):
                read_tokens.append(lex.get())

        format_string = "{:<50} | {:<30} | {:<15} | {:<15} | {:<20}"
        print(format_string.format("token", "type", "line number", "line position", "absolute position"))
        for token in read_tokens:
            print(format_string.format(str(token)[:50], token.type, token.line_num, token.line_pos, token.absolute_pos))

    except IOError as e:
        error_handling.report_generic_error("IO", str(e).capitalize())
    except Exception as e:
        error_handling.report_generic_error("Unknown", str(e).capitalize())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="python based interpreter for simple date oriented language")
    parser.add_argument('path', help='path to script file')

    args = parser.parse_args()

    run(args.path)