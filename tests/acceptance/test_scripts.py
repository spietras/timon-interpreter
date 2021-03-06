import unittest
import unittest.mock as mock
import os

from timoninterpreter.execution import Environment
from timoninterpreter.source_readers import FileReader
from timoninterpreter.lexical_analysis import Lexer
from timoninterpreter.syntax_nodes import *
from timoninterpreter import tokens


def get_path(path):
    return os.path.join(os.path.dirname(__file__), path)


def get_program(path):
    with FileReader(path) as fr:
        return Program(Lexer(fr))


class ScriptsTokensTestCase(unittest.TestCase):
    @staticmethod
    def get_all_tokens(path):
        read_tokens = []

        with FileReader(path) as fr:
            lex = Lexer(fr)
            while not (read_tokens and read_tokens[-1].get_type() == tokens.TokenType.END):
                read_tokens.append(lex.get())

        return read_tokens

    def assert_tokens(self, expected, actual):
        for i, (token, (expected_type, expected_value)) in enumerate(zip(actual, expected)):
            self.assertEqual(expected_type, token.get_type(), msg="Type mismatch for token number {}".format(i))
            self.assertEqual(expected_value, token.get_value(), msg="Value mismatch for token number {}".format(i))

    def test_script1(self):
        read_tokens = self.get_all_tokens(get_path('scripts/script1.tim'))

        expected_tokens = [(tokens.TokenType.FUN,                    None),
                           (tokens.TokenType.IDENTIFIER,             "printDaysBetweenDates"),
                           (tokens.TokenType.LEFT_PARENTHESIS,       None),
                           (tokens.TokenType.IDENTIFIER,             "d1"),
                           (tokens.TokenType.COMMA,                  None),
                           (tokens.TokenType.IDENTIFIER,             "d2"),
                           (tokens.TokenType.RIGHT_PARENTHESIS,      None),
                           (tokens.TokenType.LEFT_BRACKET,           None),
                           (tokens.TokenType.FROM,                   None),
                           (tokens.TokenType.IDENTIFIER,             "d1"),
                           (tokens.TokenType.TO,                     None),
                           (tokens.TokenType.IDENTIFIER,             "d2"),
                           (tokens.TokenType.BY,                     None),
                           (tokens.TokenType.DAYS,                   None),
                           (tokens.TokenType.AS,                     None),
                           (tokens.TokenType.IDENTIFIER,             "d3"),
                           (tokens.TokenType.LEFT_BRACKET,           None),
                           (tokens.TokenType.PRINT,                  None),
                           (tokens.TokenType.IDENTIFIER,             "d3"),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.RIGHT_BRACKET,          None),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.RETURN,                 None),
                           (tokens.TokenType.NUMBER_LITERAL,         0),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.RIGHT_BRACKET,          None),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.VAR,                    None),
                           (tokens.TokenType.IDENTIFIER,             "dt"),
                           (tokens.TokenType.ASSIGN,                 None),
                           (tokens.TokenType.DATETIME_LITERAL,       tokens.DateTimeValue(10, 4, 2018, 10, 57, 0)),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.VAR,                    None),
                           (tokens.TokenType.IDENTIFIER,             "d"),
                           (tokens.TokenType.ASSIGN,                 None),
                           (tokens.TokenType.DATE_LITERAL,           tokens.DateValue(12, 4, 2018)),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.IDENTIFIER,             "printDaysBetweenDates"),
                           (tokens.TokenType.LEFT_PARENTHESIS,       None),
                           (tokens.TokenType.IDENTIFIER,             "dt"),
                           (tokens.TokenType.COMMA,                  None),
                           (tokens.TokenType.IDENTIFIER,             "d"),
                           (tokens.TokenType.RIGHT_PARENTHESIS,      None),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.END,                    None)]

        self.assert_tokens(expected_tokens, read_tokens)

    def test_script2(self):
        read_tokens = self.get_all_tokens(get_path('scripts/script2.tim'))

        expected_tokens = [(tokens.TokenType.VAR,                    None),
                           (tokens.TokenType.IDENTIFIER,             "start_time"),
                           (tokens.TokenType.ASSIGN,                 None),
                           (tokens.TokenType.DATE_LITERAL,           tokens.DateValue(10, 6, 2020)),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.VAR,                    None),
                           (tokens.TokenType.IDENTIFIER,             "delay"),
                           (tokens.TokenType.ASSIGN,                 None),
                           (tokens.TokenType.TIMEDELTA_LITERAL,      tokens.TimedeltaValue(days=5, seconds=0)),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.VAR,                    None),
                           (tokens.TokenType.IDENTIFIER,             "prev_t1"),
                           (tokens.TokenType.ASSIGN,                 None),
                           (tokens.TokenType.DATE_LITERAL,           tokens.DateValue(25, 5, 2020)),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.VAR,                    None),
                           (tokens.TokenType.IDENTIFIER,             "prev_t2"),
                           (tokens.TokenType.ASSIGN,                 None),
                           (tokens.TokenType.DATE_LITERAL,           tokens.DateValue(20, 5, 2020)),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.IF,                     None),
                           (tokens.TokenType.IDENTIFIER,             "start_time"),
                           (tokens.TokenType.PLUS,                   None),
                           (tokens.TokenType.LEFT_PARENTHESIS,       None),
                           (tokens.TokenType.IDENTIFIER,             "prev_t1"),
                           (tokens.TokenType.MINUS,                  None),
                           (tokens.TokenType.IDENTIFIER,             "prev_t2"),
                           (tokens.TokenType.RIGHT_PARENTHESIS,      None),
                           (tokens.TokenType.PLUS,                   None),
                           (tokens.TokenType.IDENTIFIER,             "delay"),
                           (tokens.TokenType.LESS_OR_EQUAL,          None),
                           (tokens.TokenType.DATE_LITERAL,           tokens.DateValue(20, 6, 2020)),
                           (tokens.TokenType.LEFT_BRACKET,           None),
                           (tokens.TokenType.PRINT,                  None),
                           (tokens.TokenType.STRING_LITERAL,         "we have time"),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.RIGHT_BRACKET,          None),
                           (tokens.TokenType.ELSE,                   None),
                           (tokens.TokenType.LEFT_BRACKET,           None),
                           (tokens.TokenType.PRINT,                  None),
                           (tokens.TokenType.STRING_LITERAL,         "we dont have time"),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.RIGHT_BRACKET,          None),
                           (tokens.TokenType.SEMICOLON,              None)]

        self.assert_tokens(expected_tokens, read_tokens)
        
    def test_script3(self):
        read_tokens = self.get_all_tokens(get_path('scripts/script3.tim'))

        expected_tokens = [(tokens.TokenType.FUN,				     None),
                           (tokens.TokenType.IDENTIFIER,			 "getMonthDiff"),
                           (tokens.TokenType.LEFT_PARENTHESIS,		 None),
                           (tokens.TokenType.IDENTIFIER,			 "d1"),
                           (tokens.TokenType.COMMA,					 None),
                           (tokens.TokenType.IDENTIFIER,			 "d2"),
                           (tokens.TokenType.RIGHT_PARENTHESIS,		 None),
                           (tokens.TokenType.LEFT_BRACKET,			 None),
                           (tokens.TokenType.RETURN,				 None),
                           (tokens.TokenType.LEFT_PARENTHESIS,		 None),
                           (tokens.TokenType.IDENTIFIER,			 "d1"),
                           (tokens.TokenType.MINUS,					 None),
                           (tokens.TokenType.IDENTIFIER,			 "d2"),
                           (tokens.TokenType.RIGHT_PARENTHESIS,		 None),
                           (tokens.TokenType.ACCESS,				 None),
                           (tokens.TokenType.MONTHS,				 None),
                           (tokens.TokenType.PLUS,					 None),
                           (tokens.TokenType.NUMBER_LITERAL,		 12),
                           (tokens.TokenType.MULTIPLICATION,		 None),
                           (tokens.TokenType.LEFT_PARENTHESIS,		 None),
                           (tokens.TokenType.IDENTIFIER,			 "d1"),
                           (tokens.TokenType.MINUS,					 None),
                           (tokens.TokenType.IDENTIFIER,			 "d2"),
                           (tokens.TokenType.RIGHT_PARENTHESIS,		 None),
                           (tokens.TokenType.ACCESS,				 None),
                           (tokens.TokenType.YEARS,					 None),
                           (tokens.TokenType.SEMICOLON,				 None),
                           (tokens.TokenType.RIGHT_BRACKET,			 None),
                           (tokens.TokenType.SEMICOLON,				 None),
                           (tokens.TokenType.FUN,					 None),
                           (tokens.TokenType.IDENTIFIER,			 "getFirstDateOfNextMonth"),
                           (tokens.TokenType.LEFT_PARENTHESIS,		 None),
                           (tokens.TokenType.IDENTIFIER,			 "date"),
                           (tokens.TokenType.RIGHT_PARENTHESIS,		 None),
                           (tokens.TokenType.LEFT_BRACKET,			 None),
                           (tokens.TokenType.FROM,					 None),
                           (tokens.TokenType.IDENTIFIER,			 "date"),
                           (tokens.TokenType.TO,					 None),
                           (tokens.TokenType.IDENTIFIER,			 "date"),
                           (tokens.TokenType.PLUS,					 None),
                           (tokens.TokenType.TIMEDELTA_LITERAL,		 tokens.TimedeltaValue(months=1)),
                           (tokens.TokenType.BY,					 None),
                           (tokens.TokenType.DAYS,					 None),
                           (tokens.TokenType.AS,					 None),
                           (tokens.TokenType.IDENTIFIER,			 "d"),
                           (tokens.TokenType.LEFT_BRACKET,			 None),
                           (tokens.TokenType.IF,					 None),
                           (tokens.TokenType.IDENTIFIER,			 "d"),
                           (tokens.TokenType.ACCESS,				 None),
                           (tokens.TokenType.DAYS,					 None),
                           (tokens.TokenType.EQUALS,				 None),
                           (tokens.TokenType.NUMBER_LITERAL,		 1),
                           (tokens.TokenType.LEFT_BRACKET,			 None),
                           (tokens.TokenType.RETURN,				 None),
                           (tokens.TokenType.IDENTIFIER,			 "d"),
                           (tokens.TokenType.SEMICOLON,				 None),
                           (tokens.TokenType.RIGHT_BRACKET,			 None),
                           (tokens.TokenType.SEMICOLON,				 None),
                           (tokens.TokenType.RIGHT_BRACKET,			 None),
                           (tokens.TokenType.SEMICOLON,				 None),
                           (tokens.TokenType.RETURN,				 None),
                           (tokens.TokenType.IDENTIFIER,			 "date"),
                           (tokens.TokenType.SEMICOLON,				 None),
                           (tokens.TokenType.RIGHT_BRACKET,			 None),
                           (tokens.TokenType.SEMICOLON,				 None),
                           (tokens.TokenType.PRINT,					 None),
                           (tokens.TokenType.IDENTIFIER,			 "getMonthDiff"),
                           (tokens.TokenType.LEFT_PARENTHESIS,		 None),
                           (tokens.TokenType.IDENTIFIER,			 "getFirstDateOfNextMonth"),
                           (tokens.TokenType.LEFT_PARENTHESIS,		 None),
                           (tokens.TokenType.DATE_LITERAL,		     tokens.DateValue(15, 11, 2021)),
                           (tokens.TokenType.RIGHT_PARENTHESIS,		 None),
                           (tokens.TokenType.COMMA,					 None),
                           (tokens.TokenType.IDENTIFIER,			 "getFirstDateOfNextMonth"),
                           (tokens.TokenType.LEFT_PARENTHESIS,		 None),
                           (tokens.TokenType.DATE_LITERAL,			 tokens.DateValue(28, 5, 2020)),
                           (tokens.TokenType.RIGHT_PARENTHESIS,		 None),
                           (tokens.TokenType.RIGHT_PARENTHESIS,		 None),
                           (tokens.TokenType.SEMICOLON,				 None),
                           (tokens.TokenType.END,					 None)]

        self.assert_tokens(expected_tokens, read_tokens)

    def test_script4(self):
        read_tokens = self.get_all_tokens(get_path('scripts/script4.tim'))

        expected_tokens = [(tokens.TokenType.VAR,                    None),
                           (tokens.TokenType.IDENTIFIER,             "t1"),
                           (tokens.TokenType.ASSIGN,                 None),
                           (tokens.TokenType.TIME_LITERAL,           tokens.TimeValue(15, 57, 23)),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.VAR,                    None),
                           (tokens.TokenType.IDENTIFIER,             "t2"),
                           (tokens.TokenType.ASSIGN,                 None),
                           (tokens.TokenType.TIME_LITERAL,           tokens.TimeValue(20, 45, 0)),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.VAR,                    None),
                           (tokens.TokenType.IDENTIFIER,             "td"),
                           (tokens.TokenType.ASSIGN,                 None),
                           (tokens.TokenType.IDENTIFIER,             "t2"),
                           (tokens.TokenType.MINUS,                  None),
                           (tokens.TokenType.IDENTIFIER,             "t1"),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.VAR,                    None),
                           (tokens.TokenType.IDENTIFIER,             "h"),
                           (tokens.TokenType.ASSIGN,                 None),
                           (tokens.TokenType.IDENTIFIER,             "td"),
                           (tokens.TokenType.ACCESS,                 None),
                           (tokens.TokenType.HOURS,                  None),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.VAR,                    None),
                           (tokens.TokenType.IDENTIFIER,             "napis"),
                           (tokens.TokenType.ASSIGN,                 None),
                           (tokens.TokenType.STRING_LITERAL,         "hours between "),
                           (tokens.TokenType.PLUS,                   None),
                           (tokens.TokenType.IDENTIFIER,             "t1"),
                           (tokens.TokenType.PLUS,                   None),
                           (tokens.TokenType.STRING_LITERAL,         " and "),
                           (tokens.TokenType.PLUS,                   None),
                           (tokens.TokenType.IDENTIFIER,             "t2"),
                           (tokens.TokenType.PLUS,                   None),
                           (tokens.TokenType.STRING_LITERAL,         " : "),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.PRINT,                  None),
                           (tokens.TokenType.IDENTIFIER,             "napis"),
                           (tokens.TokenType.PLUS,                   None),
                           (tokens.TokenType.IDENTIFIER,             "h"),
                           (tokens.TokenType.SEMICOLON,              None)]

        self.assert_tokens(expected_tokens, read_tokens)


class ScriptsParsingTestCase(unittest.TestCase):
    def assert_tree(self, node, expected_tree):
        tree = [type(node)] + list(ScriptsParsingTestCase._get_tree(node))
        self.assertEqual(expected_tree, tree)

    @staticmethod
    def _get_tree(node):
        for child in node.get_children():
            yield type(child)
            if child.get_children():
                yield from ScriptsParsingTestCase._get_tree(child)

    def test_script1(self):
        program = get_program(get_path('scripts/script1.tim'))

        expected_tree = [
            Program,
                FunctionDefinitionStatement,
                    Identifier,
                    ParametersDeclaration,
                        Identifier,
                        Identifier,
                    Body,
                        FromStatement,
                            Identifier,
                            Identifier,
                            Days,
                            Identifier,
                            Body,
                                PrintStatement,
                                    Identifier,
                        ReturnStatement,
                            NumberLiteral,
                VariableDefinitionStatement,
                    Identifier,
                    VariableAssignmentStatement,
                        Identifier,
                        DateTimeLiteral,
                VariableDefinitionStatement,
                    Identifier,
                    VariableAssignmentStatement,
                        Identifier,
                        DateLiteral,
                FunctionCall,
                    Identifier,
                    Identifier,
                    Identifier
        ]

        self.assert_tree(program, expected_tree)

    def test_script2(self):
        program = get_program(get_path('scripts/script2.tim'))

        expected_tree = [
            Program,
                VariableDefinitionStatement,
                    Identifier,
                    VariableAssignmentStatement,
                        Identifier,
                        DateLiteral,
                VariableDefinitionStatement,
                    Identifier,
                    VariableAssignmentStatement,
                        Identifier,
                        TimedeltaLiteral,
                VariableDefinitionStatement,
                    Identifier,
                    VariableAssignmentStatement,
                        Identifier,
                        DateLiteral,
                VariableDefinitionStatement,
                    Identifier,
                    VariableAssignmentStatement,
                        Identifier,
                        DateLiteral,
                IfStatement,
                    LogicRelationalExpression,
                        MathExpression,
                            Identifier,
                            PlusOperator,
                            MathExpression,
                                Identifier,
                                MinusOperator,
                                Identifier,
                            PlusOperator,
                            Identifier,
                        LessOrEqualOperator,
                        DateLiteral,
                    Body,
                        PrintStatement,
                            StringLiteral,
                    Body,
                        PrintStatement,
                            StringLiteral
        ]

        self.assert_tree(program, expected_tree)

    def test_script3(self):
        program = get_program(get_path('scripts/script3.tim'))

        expected_tree = [
            Program,
                FunctionDefinitionStatement,
                    Identifier,
                    ParametersDeclaration,
                        Identifier,
                        Identifier,
                    Body,
                        ReturnStatement,
                            MathExpression,
                                MathTerm,
                                    MathExpression,
                                        Identifier,
                                        MinusOperator,
                                        Identifier,
                                    TimeInfoAccess,
                                        Months,
                                PlusOperator,
                                MultiplicativeMathExpression,
                                    NumberLiteral,
                                    MultiplyOperator,
                                    MathTerm,
                                        MathExpression,
                                            Identifier,
                                            MinusOperator,
                                            Identifier,
                                        TimeInfoAccess,
                                            Years,
                FunctionDefinitionStatement,
                    Identifier,
                    ParametersDeclaration,
                        Identifier,
                    Body,
                        FromStatement,
                            Identifier,
                            MathExpression,
                                Identifier,
                                PlusOperator,
                                TimedeltaLiteral,
                            Days,
                            Identifier,
                            Body,
                                IfStatement,
                                    LogicEqualityExpression,
                                        MathTerm,
                                            Identifier,
                                            TimeInfoAccess,
                                                Days,
                                        EqualOperator,
                                        NumberLiteral,
                                    Body,
                                        ReturnStatement,
                                            Identifier,
                        ReturnStatement,
                            Identifier,
                PrintStatement,
                    FunctionCall,
                        Identifier,
                        FunctionCall,
                            Identifier,
                            DateLiteral,
                        FunctionCall,
                            Identifier,
                            DateLiteral
        ]

        self.assert_tree(program, expected_tree)

    def test_script4(self):
        program = get_program(get_path('scripts/script4.tim'))

        expected_tree = [
            Program,
                VariableDefinitionStatement,
                    Identifier,
                    VariableAssignmentStatement,
                        Identifier,
                        TimeLiteral,
                VariableDefinitionStatement,
                    Identifier,
                    VariableAssignmentStatement,
                        Identifier,
                        TimeLiteral,
                VariableDefinitionStatement,
                    Identifier,
                    VariableAssignmentStatement,
                        Identifier,
                        MathExpression,
                            Identifier,
                            MinusOperator,
                            Identifier,
                VariableDefinitionStatement,
                    Identifier,
                    VariableAssignmentStatement,
                        Identifier,
                        MathTerm,
                            Identifier,
                            TimeInfoAccess,
                                Hours,
                VariableDefinitionStatement,
                    Identifier,
                    VariableAssignmentStatement,
                        Identifier,
                        MathExpression,
                            StringLiteral,
                            PlusOperator,
                            Identifier,
                            PlusOperator,
                            StringLiteral,
                            PlusOperator,
                            Identifier,
                            PlusOperator,
                            StringLiteral,
                PrintStatement,
                    MathExpression,
                        Identifier,
                        PlusOperator,
                        Identifier
        ]

        self.assert_tree(program, expected_tree)


class ScriptsExecutionTestCase(unittest.TestCase):
    def assert_printed(self, mocked_print, path, expected_print_calls):
        get_program(get_path(path)).execute(Environment())
        self.assertEqual(mocked_print.mock_calls, [mock.call(s) for s in expected_print_calls])

    @mock.patch('builtins.print')
    def test_script1(self, mocked_print):
        self.assert_printed(mocked_print, "scripts/script1.tim", ["10.04.2018~10:57:00", "11.04.2018~10:57:00"])

    @mock.patch('builtins.print')
    def test_script2(self, mocked_print):
        self.assert_printed(mocked_print, "scripts/script2.tim", ["we have time"])

    @mock.patch('builtins.print')
    def test_script3(self, mocked_print):
        self.assert_printed(mocked_print, "scripts/script3.tim", ["18"])

    @mock.patch('builtins.print')
    def test_script4(self, mocked_print):
        self.assert_printed(mocked_print, "scripts/script4.tim", ["hours between 15:57:23 and 20:45:00 : 4"])
