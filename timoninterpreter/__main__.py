"""

Main script

"""

import argparse

from timoninterpreter import error_handling
from timoninterpreter import tokens
from timoninterpreter.lexical_analysis import Lexer
from timoninterpreter.source_readers import FileReader
from timoninterpreter.syntax_nodes import LeafNode
from timoninterpreter.syntax_nodes import Program
from timoninterpreter.execution import Environment


def display_tokens(token_list):
    format_string = "{:<50} | {:<30} | {:<15} | {:<15} | {:<20}"
    print(format_string.format("token", "type", "line number", "line position", "absolute position"))
    for token in token_list:
        print(
            format_string.format(str(token)[:50],
                                 token.get_type(),
                                 token.get_file_pos().get_line_num(),
                                 token.get_file_pos().get_line_pos(),
                                 token.get_file_pos().get_absolute_pos()))


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
                yield from tree(child, prefix=prefix + extension)

    print(type(root_node).__name__)
    for line in tree(root_node):
        print(line)


def run_lexer(path):
    try:
        read_tokens = []

        with FileReader(path) as fr:
            lex = Lexer(fr)
            while not (read_tokens and read_tokens[-1].get_type() == tokens.TokenType.END):
                read_tokens.append(lex.get())

        display_tokens(read_tokens)

    except IOError as e:
        error_handling.report_generic_error("IO", str(e).capitalize())
    except error_handling.LexicalError as e:
        error_handling.report_lexical_error(e.file_pos, e.message)
    except error_handling.SyntacticError as e:
        error_handling.report_syntactic_error(e.token, e.message)
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
    except error_handling.LexicalError as e:
        error_handling.report_lexical_error(e.file_pos, e.message)
    except error_handling.SyntacticError as e:
        error_handling.report_syntactic_error(e.token, e.message)
    except Exception as e:
        error_handling.report_generic_error("Unknown", str(e).capitalize())


def run_execution(path):
    try:
        with FileReader(path) as fr:
            lex = Lexer(fr)
            program = Program(lex)

        program.execute(Environment())

    except IOError as e:
        error_handling.report_generic_error("IO", str(e).capitalize())
    except error_handling.LexicalError as e:
        error_handling.report_lexical_error(e.file_pos, e.message)
    except error_handling.SyntacticError as e:
        error_handling.report_syntactic_error(e.token, e.message)
    except Exception as e:
        error_handling.report_generic_error("Unknown", str(e).capitalize())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="python based interpreter for simple date oriented language")
    parser.add_argument('path', help='path to script file')
    parser.add_argument('-stage', choices=['lexer', 'parser', 'execution'], default='execution')

    args = parser.parse_args()

    if args.stage == 'lexer':
        run_lexer(args.path)
    elif args.stage == 'parser':
        run_parser(args.path)
    elif args.stage == 'execution':
        run_execution(args.path)
