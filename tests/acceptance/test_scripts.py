import unittest

from timoninterpreter.source_readers import FileReader
from timoninterpreter.lexical_analysis import Lexer
from timoninterpreter import tokens


class ScriptsTokensTestCase(unittest.TestCase):
    @staticmethod
    def get_all_tokens(path):
        read_tokens = []

        with FileReader(path) as fr:
            lex = Lexer(fr)
            while not (read_tokens and read_tokens[-1].type == tokens.TokenType.END):
                read_tokens.append(lex.get())

        return read_tokens

    def assert_tokens(self, expected, actual):
        for i, (token, (expected_type, expected_value)) in enumerate(zip(actual, expected)):
            self.assertEqual(expected_type, token.type, msg="Type mismatch for token number {}".format(i))
            self.assertEqual(expected_value, token.value, msg="Value mismatch for token number {}".format(i))

    def test_script1(self):
        read_tokens = self.get_all_tokens("scripts/script1.tim")

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
        read_tokens = self.get_all_tokens("scripts/script2.tim")

        expected_tokens = [(tokens.TokenType.VAR,                    None),
                           (tokens.TokenType.IDENTIFIER,             "start_time"),
                           (tokens.TokenType.ASSIGN,                 None),
                           (tokens.TokenType.DATE_LITERAL,           tokens.DateValue(10, 6, 2020)),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.VAR,                    None),
                           (tokens.TokenType.IDENTIFIER,             "delay"),
                           (tokens.TokenType.ASSIGN,                 None),
                           (tokens.TokenType.TIMEDELTA_LITERAL,      tokens.TimedeltaValue(weeks=10, days=10)),
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
        read_tokens = self.get_all_tokens("scripts/script3.tim")

        expected_tokens = [(tokens.TokenType.VAR,                    None),
                           (tokens.TokenType.IDENTIFIER,             "t1"),
                           (tokens.TokenType.ASSIGN,                 None),
                           (tokens.TokenType.HOUR_LITERAL,           tokens.HourValue(15, 57, 23)),
                           (tokens.TokenType.SEMICOLON,              None),
                           (tokens.TokenType.VAR,                    None),
                           (tokens.TokenType.IDENTIFIER,             "t2"),
                           (tokens.TokenType.ASSIGN,                 None),
                           (tokens.TokenType.HOUR_LITERAL,           tokens.HourValue(20, 45, 0)),
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
                           (tokens.TokenType.STRING_LITERAL,         " "),
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