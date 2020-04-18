import unittest
import unittest.mock as mock
import io

from timoninterpreter.source_readers import FileReader
from timoninterpreter import lexical_analysis
from timoninterpreter.lexical_analysis import Lexer
from timoninterpreter import tokens
from timoninterpreter import error_handling


class BaseLexerTestCase(unittest.TestCase):
    def assert_tokens(self, expectations):
        with FileReader("whatever") as fr:
            for expected_type, expected_value in expectations:
                token = Lexer(fr).get()
                self.assertEqual(expected_type, token.type)
                self.assertEqual(expected_value, token.value)

    def assert_token(self, expected_type, expected_value):
        self.assert_tokens([(expected_type, expected_value)])


# noinspection PyUnusedLocal
class LexerStaticTokensTestCase(BaseLexerTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("fun"))
    def test_get_keyword_fun(self, mock_open):
        self.assert_token(tokens.TokenType.FUN, None)

    @mock.patch('builtins.open', return_value=io.StringIO("var"))
    def test_get_keyword_var(self, mock_open):
        self.assert_token(tokens.TokenType.VAR, None)

    @mock.patch('builtins.open', return_value=io.StringIO("if"))
    def test_get_keyword_if(self, mock_open):
        self.assert_token(tokens.TokenType.IF, None)

    @mock.patch('builtins.open', return_value=io.StringIO("else"))
    def test_get_keyword_else(self, mock_open):
        self.assert_token(tokens.TokenType.ELSE, None)

    @mock.patch('builtins.open', return_value=io.StringIO("from"))
    def test_get_keyword_from(self, mock_open):
        self.assert_token(tokens.TokenType.FROM, None)

    @mock.patch('builtins.open', return_value=io.StringIO("print"))
    def test_get_keyword_print(self, mock_open):
        self.assert_token(tokens.TokenType.PRINT, None)

    @mock.patch('builtins.open', return_value=io.StringIO("return"))
    def test_get_keyword_return(self, mock_open):
        self.assert_token(tokens.TokenType.RETURN, None)

    @mock.patch('builtins.open', return_value=io.StringIO("to"))
    def test_get_keyword_to(self, mock_open):
        self.assert_token(tokens.TokenType.TO, None)

    @mock.patch('builtins.open', return_value=io.StringIO("by"))
    def test_get_keyword_by(self, mock_open):
        self.assert_token(tokens.TokenType.BY, None)

    @mock.patch('builtins.open', return_value=io.StringIO("as"))
    def test_get_keyword_as(self, mock_open):
        self.assert_token(tokens.TokenType.AS, None)

    @mock.patch('builtins.open', return_value=io.StringIO("years"))
    def test_get_keyword_years(self, mock_open):
        self.assert_token(tokens.TokenType.YEARS, None)

    @mock.patch('builtins.open', return_value=io.StringIO("months"))
    def test_get_keyword_months(self, mock_open):
        self.assert_token(tokens.TokenType.MONTHS, None)

    @mock.patch('builtins.open', return_value=io.StringIO("weeks"))
    def test_get_keyword_weeks(self, mock_open):
        self.assert_token(tokens.TokenType.WEEKS, None)

    @mock.patch('builtins.open', return_value=io.StringIO("days"))
    def test_get_keyword_days(self, mock_open):
        self.assert_token(tokens.TokenType.DAYS, None)

    @mock.patch('builtins.open', return_value=io.StringIO("hours"))
    def test_get_keyword_hours(self, mock_open):
        self.assert_token(tokens.TokenType.HOURS, None)

    @mock.patch('builtins.open', return_value=io.StringIO("minutes"))
    def test_get_keyword_minutes(self, mock_open):
        self.assert_token(tokens.TokenType.MINUTES, None)

    @mock.patch('builtins.open', return_value=io.StringIO("seconds"))
    def test_get_keyword_seconds(self, mock_open):
        self.assert_token(tokens.TokenType.SECONDS, None)

    @mock.patch('builtins.open', return_value=io.StringIO(";"))
    def test_get_special_semicolon(self, mock_open):
        self.assert_token(tokens.TokenType.SEMICOLON, None)

    @mock.patch('builtins.open', return_value=io.StringIO("("))
    def test_get_special_left_parenthesis(self, mock_open):
        self.assert_token(tokens.TokenType.LEFT_PARENTHESIS, None)

    @mock.patch('builtins.open', return_value=io.StringIO(")"))
    def test_get_special_right_parenthesis(self, mock_open):
        self.assert_token(tokens.TokenType.RIGHT_PARENTHESIS, None)

    @mock.patch('builtins.open', return_value=io.StringIO(","))
    def test_get_special_comma(self, mock_open):
        self.assert_token(tokens.TokenType.COMMA, None)

    @mock.patch('builtins.open', return_value=io.StringIO("{"))
    def test_get_special_left_bracket(self, mock_open):
        self.assert_token(tokens.TokenType.LEFT_BRACKET, None)

    @mock.patch('builtins.open', return_value=io.StringIO("}"))
    def test_get_special_right_bracket(self, mock_open):
        self.assert_token(tokens.TokenType.RIGHT_BRACKET, None)

    @mock.patch('builtins.open', return_value=io.StringIO("="))
    def test_get_special_assign(self, mock_open):
        self.assert_token(tokens.TokenType.ASSIGN, None)

    @mock.patch('builtins.open', return_value=io.StringIO("|"))
    def test_get_special_logical_or(self, mock_open):
        self.assert_token(tokens.TokenType.LOGICAL_OR, None)

    @mock.patch('builtins.open', return_value=io.StringIO("&"))
    def test_get_special_logical_and(self, mock_open):
        self.assert_token(tokens.TokenType.LOGICAL_AND, None)

    @mock.patch('builtins.open', return_value=io.StringIO("=="))
    def test_get_special_equals(self, mock_open):
        self.assert_token(tokens.TokenType.EQUALS, None)

    @mock.patch('builtins.open', return_value=io.StringIO("!="))
    def test_get_special_not_equals(self, mock_open):
        self.assert_token(tokens.TokenType.NOT_EQUALS, None)

    @mock.patch('builtins.open', return_value=io.StringIO(">"))
    def test_get_special_greater(self, mock_open):
        self.assert_token(tokens.TokenType.GREATER, None)

    @mock.patch('builtins.open', return_value=io.StringIO(">="))
    def test_get_special_greater_or_equal(self, mock_open):
        self.assert_token(tokens.TokenType.GREATER_OR_EQUAL, None)

    @mock.patch('builtins.open', return_value=io.StringIO("<"))
    def test_get_special_less(self, mock_open):
        self.assert_token(tokens.TokenType.LESS, None)

    @mock.patch('builtins.open', return_value=io.StringIO("<="))
    def test_get_special_less_or_equal(self, mock_open):
        self.assert_token(tokens.TokenType.LESS_OR_EQUAL, None)

    @mock.patch('builtins.open', return_value=io.StringIO("!"))
    def test_get_special_not(self, mock_open):
        self.assert_token(tokens.TokenType.NOT, None)

    @mock.patch('builtins.open', return_value=io.StringIO("+"))
    def test_get_special_plus(self, mock_open):
        self.assert_token(tokens.TokenType.PLUS, None)

    @mock.patch('builtins.open', return_value=io.StringIO("-"))
    def test_get_special_minus(self, mock_open):
        self.assert_token(tokens.TokenType.MINUS, None)

    @mock.patch('builtins.open', return_value=io.StringIO("*"))
    def test_get_special_multiplication(self, mock_open):
        self.assert_token(tokens.TokenType.MULTIPLICATION, None)

    @mock.patch('builtins.open', return_value=io.StringIO("/"))
    def test_get_special_division(self, mock_open):
        self.assert_token(tokens.TokenType.DIVISION, None)

    @mock.patch('builtins.open', return_value=io.StringIO("."))
    def test_get_special_access(self, mock_open):
        self.assert_token(tokens.TokenType.ACCESS, None)

    @mock.patch('builtins.open', return_value=io.StringIO(""))
    def test_get_special_end(self, mock_open):
        self.assert_token(tokens.TokenType.END, None)


# noinspection PyUnusedLocal
class LexerIdentifierTestCase(BaseLexerTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("abc"))
    def test_get_identifier(self, mock_open):
        self.assert_token(tokens.TokenType.IDENTIFIER, "abc")

    @mock.patch('builtins.open', return_value=io.StringIO("abc1abc"))
    def test_get_identifier_with_digit(self, mock_open):
        self.assert_token(tokens.TokenType.IDENTIFIER, "abc1abc")

    @mock.patch('builtins.open', return_value=io.StringIO("abcreturnabc"))
    def test_get_identifier_with_keyword(self, mock_open):
        self.assert_token(tokens.TokenType.IDENTIFIER, "abcreturnabc")

    @mock.patch('builtins.open', return_value=io.StringIO("ifif"))
    def test_get_identifier_multiple_keywords(self, mock_open):
        self.assert_token(tokens.TokenType.IDENTIFIER, "ifif")

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO('x' * (lexical_analysis.IdentifierSubLexer.MAX_IDENTIFIER_LENGTH + 1)))
    def test_get_identifier_too_long(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)


# noinspection PyUnusedLocal
class LexerNumberLiteralTestCase(BaseLexerTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("123"))
    def test_get_number_literal(self, mock_open):
        self.assert_token(tokens.TokenType.NUMBER_LITERAL, 123)

    @mock.patch('builtins.open', return_value=io.StringIO("0"))
    def test_get_number_literal_zero_at_beginning(self, mock_open):
        self.assert_token(tokens.TokenType.NUMBER_LITERAL, 0)

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO('x' * (lexical_analysis.NumberLiteralSubLexer.MAX_NUMBER_LITERAL_LENGTH + 1)))
    def test_get_number_literal_too_long(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)


# noinspection PyUnusedLocal
class LexerDateLiteralTestCase(BaseLexerTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("01.01.2020"))
    def test_get_date_literal(self, mock_open):
        self.assert_token(tokens.TokenType.DATE_LITERAL, tokens.DateValue(1, 1, 2020))

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("01.01;"))
    def test_get_date_literal_unfinished(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("010.03.2015"))
    def test_get_date_literal_too_many_digits_day(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("01.010.2015"))
    def test_get_date_literal_too_many_digits_month(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('builtins.open', return_value=io.StringIO("01.01.20200"))
    def test_get_date_literal_digits_follow_year(self, mock_open):
        self.assert_token(tokens.TokenType.DATE_LITERAL, tokens.DateValue(1, 1, 2020))

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("35.10.2015"))
    def test_get_date_illegal_day(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("31.04.2020"))
    def test_get_date_illegal_day_of_month(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("30.02.2020"))
    def test_get_date_illegal_day_january(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("29.02.2019"))
    def test_get_date_illegal_day_january_not_leap_year(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("01.13.2020"))
    def test_get_date_illegal_month(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("01.01.0000"))
    def test_get_date_illegal_year(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)


# noinspection PyUnusedLocal
class LexerHourLiteralTestCase(BaseLexerTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("20:00:00"))
    def test_get_hour_literal(self, mock_open):
        self.assert_token(tokens.TokenType.HOUR_LITERAL, tokens.HourValue(20, 0, 0))

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("20:20;"))
    def test_get_hour_literal_unfinished(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("020:00:00"))
    def test_get_hour_literal_too_many_digits_hour(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("20:000:00"))
    def test_get_hour_literal_too_many_digits_minute(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('builtins.open', return_value=io.StringIO("20:00:001"))
    def test_get_hour_literal_digits_follow_second(self, mock_open):
        self.assert_token(tokens.TokenType.HOUR_LITERAL, tokens.HourValue(20, 0, 0))

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("25:00:00"))
    def test_get_hour_illegal_hour(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("20:60:00"))
    def test_get_hour_illegal_minute(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("20:00:60"))
    def test_get_hour_illegal_second(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)


# noinspection PyUnusedLocal
class LexerDateTimeLiteralTestCase(BaseLexerTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("01.01.2020~20:00:00"))
    def test_get_datetime_literal(self, mock_open):
        self.assert_token(tokens.TokenType.DATETIME_LITERAL, tokens.DateTimeValue(1, 1, 2020, 20, 0, 0))

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("01.01.2020~;"))
    def test_get_datetime_literal_unfinished(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)


# noinspection PyUnusedLocal
class LexerTimedeltaLiteralTestCase(BaseLexerTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("'1Y 2M 3W 4D 5h 6m 7s'"))
    def test_get_timedelta_literal_full(self, mock_open):
        self.assert_token(tokens.TokenType.TIMEDELTA_LITERAL, tokens.TimedeltaValue(1, 2, 3, 4, 5, 6, 7))

    @mock.patch('builtins.open', return_value=io.StringIO("'1M 10h'"))
    def test_get_timedelta_literal_partial(self, mock_open):
        self.assert_token(tokens.TokenType.TIMEDELTA_LITERAL, tokens.TimedeltaValue(months=1, hours=10))

    @mock.patch('builtins.open', return_value=io.StringIO("'1M2D3m'"))
    def test_get_timedelta_literal_no_whitespaces(self, mock_open):
        self.assert_token(tokens.TokenType.TIMEDELTA_LITERAL, tokens.TimedeltaValue(months=1, days=2, minutes=3))

    @mock.patch('builtins.open', return_value=io.StringIO("''"))
    def test_get_timedelta_literal_empty(self, mock_open):
        self.assert_token(tokens.TokenType.TIMEDELTA_LITERAL, tokens.TimedeltaValue())

    @mock.patch('builtins.open', return_value=io.StringIO("'                '"))
    def test_get_timedelta_literal_empty_with_whitespaces(self, mock_open):
        self.assert_token(tokens.TokenType.TIMEDELTA_LITERAL, tokens.TimedeltaValue())

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("'1Y 2M 3W abcdef'"))
    def test_get_timedelta_literal_illegal_characters(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("'1Y 2M 5M 6D'"))
    def test_get_timedelta_literal_duplicated_unit(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("'1Y 6M 00001h'"))
    def test_get_timedelta_literal_bad_number(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO("'" + '1' * (lexical_analysis.TimedeltaLiteralSubLexer.MAX_TIMEDELTA_LITERAL_LENGTH + 1) + "Y'"))
    def test_get_timedelta_literal_too_long(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_warning')
    @mock.patch('builtins.open', return_value=io.StringIO("'1Y 1M "))
    def test_get_timedelta_literal_unclosed(self, mock_report, mock_open):
        self.assert_token(tokens.TokenType.TIMEDELTA_LITERAL, tokens.TimedeltaValue(years=1, months=1))
        self.assertTrue(mock_report.called)


# noinspection PyUnusedLocal
class LexerStringLiteralTestCase(BaseLexerTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO('"abc"'))
    def test_get_string_literal(self, mock_open):
        self.assert_token(tokens.TokenType.STRING_LITERAL, "abc")

    @mock.patch('builtins.open', return_value=io.StringIO('"abc\\"abc"'))
    def test_get_string_literal_with_escape(self, mock_open):
        self.assert_token(tokens.TokenType.STRING_LITERAL, "abc\"abc")

    @mock.patch('builtins.open', return_value=io.StringIO('"abcreturnabc"'))
    def test_get_string_literal_with_keyword(self, mock_open):
        self.assert_token(tokens.TokenType.STRING_LITERAL, "abcreturnabc")

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO('"' + 'x' * (lexical_analysis.StringLiteralSubLexer.MAX_STRING_LITERAL_LENGTH + 1) + '"'))
    def test_get_string_literal_too_long(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)


# noinspection PyUnusedLocal
class LexerCommentTestCase(BaseLexerTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("#abc#defgh"))
    def test_get_skip_comment(self, mock_open):
        self.assert_token(tokens.TokenType.IDENTIFIER, "defgh")

    @mock.patch('builtins.open', return_value=io.StringIO("#aaa\naaa\naaa\naaa#bcd"))
    def test_get_skip_comment_multiline(self, mock_open):
        self.assert_token(tokens.TokenType.IDENTIFIER, "bcd")

    @mock.patch('builtins.open', return_value=io.StringIO("abc#def#ghi"))
    def test_get_divide_identifier_with_comment(self, mock_open):
        self.assert_tokens([(tokens.TokenType.IDENTIFIER, "abc"),
                            (tokens.TokenType.IDENTIFIER, "ghi")])

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO('#' + 'x' * (Lexer.MAX_COMMENT_LENGTH + 1) + '#'))
    def test_get_comment_too_long(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('timoninterpreter.error_handling.report_lexical_warning')
    @mock.patch('builtins.open', return_value=io.StringIO("#abc"))
    def test_get_comment_unclosed(self, mock_report, mock_open):
        self.assert_token(tokens.TokenType.END, None)
        self.assertTrue(mock_report.called)


# noinspection PyUnusedLocal
class LexerMiscellaneousTestCase(BaseLexerTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO(" a b c "))
    def test_get_whitespace(self, mock_open):
        self.assert_tokens([(tokens.TokenType.IDENTIFIER, "a"),
                            (tokens.TokenType.IDENTIFIER, "b"),
                            (tokens.TokenType.IDENTIFIER, "c")])

    @mock.patch('builtins.open', return_value=io.StringIO("a    \n   \n\n\n   \t\t\n\t   b"))
    def test_get_multiple_whitespace(self, mock_open):
        self.assert_tokens([(tokens.TokenType.IDENTIFIER, "a"),
                            (tokens.TokenType.IDENTIFIER, "b")])

    @mock.patch('builtins.open', return_value=io.StringIO("a \n #aaaa# \n\n\n #aaaaaaa##aa# #aa#\n#aaa# b"))
    def test_get_comments_and_whitespaces(self, mock_open):
        self.assert_tokens([(tokens.TokenType.IDENTIFIER, "a"),
                            (tokens.TokenType.IDENTIFIER, "b")])

    @mock.patch('timoninterpreter.error_handling.report_lexical_error')
    @mock.patch('builtins.open', return_value=io.StringIO(' ' * (Lexer.MAX_SKIPPABLE_CHARACTERS_LENGTH + 1)))
    def test_get_skippable_too_long(self, mock_report, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.LexicalError, Lexer(fr).get)
            self.assertTrue(mock_report.called)

    @mock.patch('builtins.open', return_value=io.StringIO("abc"))
    def test_get_token_position_at_start(self, mock_open):
        with FileReader("whatever") as fr:
            token = Lexer(fr).get()
            self.assertEqual(1, token.line_num)
            self.assertEqual(0, token.line_pos)
            self.assertEqual(0, token.absolute_pos)

    @mock.patch('builtins.open', return_value=io.StringIO("\n \n \nabc"))
    def test_get_token_position_at_line_start(self, mock_open):
        with FileReader("whatever") as fr:
            token = Lexer(fr).get()
            self.assertEqual(4, token.line_num)
            self.assertEqual(0, token.line_pos)
            self.assertEqual(5, token.absolute_pos)

    @mock.patch('builtins.open', return_value=io.StringIO("\n \n \n #abc# abc"))
    def test_get_token_position_at_line_middle(self, mock_open):
        with FileReader("whatever") as fr:
            token = Lexer(fr).get()
            self.assertEqual(4, token.line_num)
            self.assertEqual(7, token.line_pos)
            self.assertEqual(12, token.absolute_pos)