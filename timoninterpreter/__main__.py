"""

Main script

"""

import argparse

from timoninterpreter.source_readers import FileReader
from timoninterpreter.lexical_analysis import Lexer
from timoninterpreter.syntax_analysis import Program
from timoninterpreter.syntax_analysis import LeafNode
from timoninterpreter import tokens
from timoninterpreter import error_handling


def display_tokens(token_list):
    format_string = "{:<50} | {:<30} | {:<15} | {:<15} | {:<20}"
    print(format_string.format("token", "type", "line number", "line position", "absolute position"))
    for token in token_list:
        print(format_string.format(str(token)[:50], token.type, token.line_num, token.line_pos, token.absolute_pos))


def display_syntax_tree(root_node):
    def tree(node, prefix=""):
        # prefix components:
        space = '    '
        branch = '│   '
        # pointers:
        tee = '├── '
        last = '└── '

        pointers = [tee] * (len(node.get_children()) - 1) + [last]
        for pointer, child in zip(pointers, node.get_children()):
            suffix = " : " + str(child.token) if isinstance(child, LeafNode) else ""
            yield prefix + pointer + type(child).__name__ + suffix
            if child.get_children():
                extension = branch if pointer == tee else space
                yield from tree(child, prefix=prefix+extension)

    print(type(root_node).__name__)
    for line in tree(root_node):
        print(line)


def run_lexer(path):
    try:
        read_tokens = []

        with FileReader(path) as fr:
            lex = Lexer(fr)
            while not (read_tokens and read_tokens[-1].type == tokens.TokenType.END):
                read_tokens.append(lex.get())

        display_tokens(read_tokens)

    except IOError as e:
        error_handling.report_generic_error("IO", str(e).capitalize())
    except Exception as e:
        error_handling.report_generic_error("Unknown", str(e).capitalize())


def run_parser(path):
    try:
        with FileReader(path) as fr:
            lex = Lexer(fr)
            program = Program(lex)

        display_syntax_tree(program)

    except IOError as e:
        error_handling.report_generic_error("IO", str(e).capitalize())
    except Exception as e:
        error_handling.report_generic_error("Unknown", str(e).capitalize())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="python based interpreter for simple date oriented language")
    parser.add_argument('path', help='path to script file')

    args = parser.parse_args()

    run_parser(args.path)
