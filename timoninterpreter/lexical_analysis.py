"""

Lexical analysis module

"""
from abc import ABC, abstractmethod

from . import tokens
from . import error_handling


class BaseLexer(ABC):
    """
    Lexer base class

    Lexer's job is to change characters into tokens
    """

    def __init__(self, source_reader):
        """
        Args:
            source_reader: opened source reader
        """
        self.source_reader = source_reader

    @abstractmethod
    def get(self):
        """
        Get next token and consume it

        Returns:
            next token
        """
        pass


def is_white(character):
    return character.isspace()


def is_comment_bound(character):
    return character == tokens.COMMENT_BOUND


def is_escape(character):
    return character == tokens.ESCAPE


def is_skippable(character):
    return is_white(character) or is_comment_bound(character)


def is_identifier_start(character):
    return character.isalpha() or character in tokens.additional_identifier_characters


def is_identifier_middle(character):
    return character.isalpha() or character.isdigit() or character in tokens.additional_identifier_characters


def is_numeric_start(character):
    return character.isdigit()


def is_string_literal_bound(character):
    return character == tokens.STRING_BOUND


def is_timedelta_literal_bound(character):
    return character == tokens.TIMEDELTA_BOUND


def is_ambiguous_binary_start(character):
    return character in tokens.ambiguous_binary_token_type_map


def is_unambiguous_singular_start(character):
    return character in tokens.unambiguous_singular_token_type_map


def is_keyword(string):
    return string in tokens.keyword_token_type_map


class SubLexer(BaseLexer, ABC):
    def __init__(self, source_reader):
        super().__init__(source_reader)
        self.start_line_num = self.source_reader.line_num
        self.start_line_pos = self.source_reader.line_pos
        self.start_absolute_pos = self.source_reader.absolute_pos

    def make_error(self, message):
        error_handling.report_lexical_error(self.start_line_num,
                                            self.start_line_pos,
                                            self.start_absolute_pos,
                                            self.source_reader,
                                            message)
        raise error_handling.LexicalError(message)


class IdentifierSubLexer(SubLexer):
    MAX_IDENTIFIER_LENGTH = 256

    def get(self):
        identifier = self.source_reader.get()

        counter = 1

        next_character = self.source_reader.peek()
        while is_identifier_middle(next_character):
            counter += 1
            if counter > self.MAX_IDENTIFIER_LENGTH:
                self.make_error("Identifier is too long. Maximum size is {} characters".format(self.MAX_IDENTIFIER_LENGTH))

            identifier += self.source_reader.get()
            next_character = self.source_reader.peek()

        if is_keyword(identifier):
            return tokens.Token(tokens.keyword_token_type_map[identifier],
                                self.start_line_num,
                                self.start_line_pos,
                                self.start_absolute_pos)

        return tokens.Token(tokens.TokenType.IDENTIFIER,
                            self.start_line_num,
                            self.start_line_pos,
                            self.start_absolute_pos,
                            identifier)


def digits_to_int(digit_list):
    return int(''.join(str(i) for i in digit_list))


class NumberLiteralSubLexer(SubLexer):
    MAX_NUMBER_LITERAL_LENGTH = 256

    def get(self):
        number_string = self.source_reader.get()

        if number_string == '0':
            return tokens.Token(tokens.TokenType.NUMBER_LITERAL,
                                self.start_line_num,
                                self.start_line_pos,
                                self.start_absolute_pos,
                                0)

        counter = 1

        next_character = self.source_reader.peek()
        while next_character.isdigit():
            counter += 1
            if counter > self.MAX_NUMBER_LITERAL_LENGTH:
                self.make_error("Digit is too long. Maximum size is {} characters".format(self.MAX_NUMBER_LITERAL_LENGTH))
            number_string += self.source_reader.get()
            next_character = self.source_reader.peek()

        return tokens.Token(tokens.TokenType.NUMBER_LITERAL,
                            self.start_line_num,
                            self.start_line_pos,
                            self.start_absolute_pos,
                            digits_to_int(number_string))


class NumericalLiteralSubLexer(SubLexer):
    def get(self):
        number_token = NumberLiteralSubLexer(self.source_reader).get()

        next_character = self.source_reader.peek()

        if next_character.isdigit():  # only when number_token is 0
            first_value = digits_to_int([next_character])
            self.source_reader.get()
            next_character = self.source_reader.peek()
        elif number_token.value < 10:  # if the next character is not a digit and number is only a single digit it has to be a standalone number
            return number_token
        else:
            first_value = number_token.value

        if next_character == '.':
            return self._get_date_or_datetime_token(first_value)

        if next_character == ':':
            return self._get_hour_token(first_value)

        if next_character.isdigit():
            self.make_error("Unexpected digit")

        return number_token

    def _check_for_character(self, character):
        next_character = self.source_reader.peek()
        if next_character != character:
            self.make_error("Unexpected character, expected '{}'".format(character))
        self.source_reader.get()

    def _get_two_digits(self):
        first_digit = self.source_reader.peek()
        if not first_digit.isdigit():
            self.make_error("Unexpected character, expected digit")
        self.source_reader.get()
        second_digit = self.source_reader.peek()
        if not second_digit.isdigit():
            self.make_error("Unexpected digit")
        self.source_reader.get()

        return first_digit, second_digit

    def _get_four_digits(self):
        return self._get_two_digits() + self._get_two_digits()

    def _get_date_or_datetime_token(self, first_value):
        self.source_reader.get()
        values = [first_value]

        digits = self._get_two_digits()
        values.append(digits_to_int(digits))

        self._check_for_character('.')

        digits = self._get_four_digits()
        values.append(digits_to_int(digits))

        next_character = self.source_reader.peek()
        if next_character != '~':
            try:
                return tokens.Token(tokens.TokenType.DATE_LITERAL,
                                    self.start_line_num,
                                    self.start_line_pos,
                                    self.start_absolute_pos,
                                    tokens.DateValue(values[0], values[1], values[2]))
            except error_handling.LexicalError as e:
                self.make_error(e.message)
        self.source_reader.get()

        digits = self._get_two_digits()
        values.append(digits_to_int(digits))

        self._check_for_character(':')

        digits = self._get_two_digits()
        values.append(digits_to_int(digits))

        self._check_for_character(':')

        digits = self._get_two_digits()
        values.append(digits_to_int(digits))

        try:
            return tokens.Token(tokens.TokenType.DATETIME_LITERAL,
                                self.start_line_num,
                                self.start_line_pos,
                                self.start_absolute_pos,
                                tokens.DateTimeValue(values[0], values[1], values[2], values[3], values[4], values[5]))
        except error_handling.LexicalError as e:
            self.make_error(e.message)

    def _get_hour_token(self, first_value):
        self.source_reader.get()
        values = [first_value]

        digits = self._get_two_digits()
        values.append(digits_to_int(digits))

        self._check_for_character(':')

        digits = self._get_two_digits()
        values.append(digits_to_int(digits))

        try:
            return tokens.Token(tokens.TokenType.TIME_LITERAL,
                                self.start_line_num,
                                self.start_line_pos,
                                self.start_absolute_pos,
                                tokens.TimeValue(values[0], values[1], values[2]))
        except error_handling.LexicalError as e:
            self.make_error(e.message)


class StringLiteralSubLexer(SubLexer):
    MAX_STRING_LITERAL_LENGTH = 4096

    def get(self):
        self.source_reader.get()

        string_value = ""
        counter = 0

        next_character = self.source_reader.peek()
        while not is_string_literal_bound(next_character):
            counter += 1
            if counter > self.MAX_STRING_LITERAL_LENGTH:
                self.make_error("String literal is too long. Maximum size is {} characters (excluding bounds and escapes)".format(self.MAX_STRING_LITERAL_LENGTH))
            if is_escape(next_character):
                self.source_reader.get()
            string_value += self.source_reader.get()
            next_character = self.source_reader.peek()

        self.source_reader.get()

        return tokens.Token(tokens.TokenType.STRING_LITERAL,
                            self.start_line_num,
                            self.start_line_pos,
                            self.start_absolute_pos,
                            string_value)


class TimedeltaLiteralSubLexer(SubLexer):
    MAX_TIMEDELTA_LITERAL_LENGTH = 7*256

    def get(self):
        self.source_reader.get()

        values_map = {
            "Y": None,
            "M": None,
            "W": None,
            "D": None,
            "h": None,
            "m": None,
            "s": None
        }

        counter = 0

        next_character = self.source_reader.peek()
        while not is_timedelta_literal_bound(next_character):
            counter += 1
            if counter > self.MAX_TIMEDELTA_LITERAL_LENGTH:
                self.make_error("Timedelta literal is too long. Maximum size is {} characters (excluding bounds)".format(self.MAX_TIMEDELTA_LITERAL_LENGTH))
            if next_character.isdigit():
                number_value = NumberLiteralSubLexer(self.source_reader).get().value

                next_character = self.source_reader.peek()

                if next_character not in values_map:
                    self.make_error("Unexpected time unit. Only possible ones are: {}".format(values_map.keys()))

                if values_map[next_character] is not None:
                    self.make_error("Unexpected {}, can't define time unit twice".format(next_character))

                values_map[next_character] = number_value
                self.source_reader.get()
                next_character = self.source_reader.peek()
            elif is_white(next_character):  # skip white characters
                self.source_reader.get()
                next_character = self.source_reader.peek()
            elif self.source_reader.ended():
                error_handling.report_lexical_warning(self.start_line_num,
                                                      self.start_line_pos,
                                                      self.start_absolute_pos,
                                                      self.source_reader,
                                                      "File ended before end of timedelta bounds",
                                                      "Ignoring")
                next_character = tokens.TIMEDELTA_BOUND
            else:
                self.make_error("Unexpected character inside timedelta bounds")

        self.source_reader.get()  # consume ending bound

        return tokens.Token(tokens.TokenType.TIMEDELTA_LITERAL,
                            self.start_line_num,
                            self.start_line_pos,
                            self.start_absolute_pos,
                            tokens.TimedeltaValue(values_map["Y"],
                                                  values_map["M"],
                                                  values_map["W"],
                                                  values_map["D"],
                                                  values_map["h"],
                                                  values_map["m"],
                                                  values_map["s"]))


class AmbiguousBinarySubLexer(SubLexer):
    def get(self):
        first_character = self.source_reader.get()  # get first
        second_character = self.source_reader.peek()  # peek second

        if second_character == tokens.ambiguous_binary_token_type_map[first_character]['second_character']:  # if first+second is known
            self.source_reader.get()  # consume second
            token_type = tokens.ambiguous_binary_token_type_map[first_character]['second_case_token_type']  # lookup first+second
        else:
            token_type = tokens.ambiguous_binary_token_type_map[first_character]['first_case_token_type']  # lookup first

        return tokens.Token(token_type,
                            self.start_line_num,
                            self.start_line_pos,
                            self.start_absolute_pos,
                            None)


class UnambiguousSingularSubLexer(SubLexer):
    def get(self):
        return tokens.Token(tokens.unambiguous_singular_token_type_map[self.source_reader.get()],
                            self.start_line_num,
                            self.start_line_pos,
                            self.start_absolute_pos,
                            None)


class Lexer(BaseLexer):
    """
    Lexer's job is to change characters into tokens
    """

    MAX_SKIPPABLE_CHARACTERS_LENGTH = 65536
    MAX_COMMENT_LENGTH = 16384

    def get(self):
        """
        Get next token and consume it

        Returns:
            next token

        Raises:
            LexicalError when input can't be processed into token
        """

        if is_skippable(self.source_reader.peek()):
            self._skip_to_unskippable()

        return self._tokenize()

    def _skip_to_unskippable(self):
        start_line_num, start_line_pos, start_absolute_pos = (self.source_reader.line_num,
                                                              self.source_reader.line_pos,
                                                              self.source_reader.absolute_pos)
        character = self.source_reader.peek()

        counter = 0

        while is_skippable(character):
            if counter >= self.MAX_SKIPPABLE_CHARACTERS_LENGTH:  # >= because we increase counter later
                message = "Too many skippable characters. Maximum size is {} characters".format(self.MAX_SKIPPABLE_CHARACTERS_LENGTH)
                error_handling.report_lexical_error(start_line_num,
                                                    start_line_pos,
                                                    start_absolute_pos,
                                                    self.source_reader,
                                                    message)
                raise error_handling.LexicalError(message)

            if is_comment_bound(character):
                counter += self._skip_comment()
            else:  # if not comment skip character by character
                self.source_reader.get()
                counter += 1

            character = self.source_reader.peek()

    def _skip_comment(self):
        start_line_num, start_line_pos, start_absolute_pos = (self.source_reader.line_num,
                                                              self.source_reader.line_pos,
                                                              self.source_reader.absolute_pos)

        self.source_reader.get()  # consume opening comment bound

        counter = 0

        character = self.source_reader.peek()
        while not is_comment_bound(character):
            counter += 1
            if counter > self.MAX_COMMENT_LENGTH:
                message = "Comment is too long. Maximum size is {} characters (excluding bounds)".format(self.MAX_COMMENT_LENGTH)
                error_handling.report_lexical_error(start_line_num,
                                                    start_line_pos,
                                                    start_absolute_pos,
                                                    self.source_reader,
                                                    message)
                raise error_handling.LexicalError(message)
            if self.source_reader.ended():  # comment unclosed before end of file
                error_handling.report_lexical_warning(start_line_num,
                                                      start_line_pos,
                                                      start_absolute_pos,
                                                      self.source_reader,
                                                      "File ended before end of comment",
                                                      "Ignoring")
                return counter + 1
            self.source_reader.get()
            character = self.source_reader.peek()
        self.source_reader.get()  # consume closing comment bound
        return counter + 2  # inside + bounds

    def _tokenize(self):
        first_character = self.source_reader.peek()

        if self.source_reader.ended():
            return tokens.Token(tokens.TokenType.END,
                                self.source_reader.line_num,
                                self.source_reader.line_pos,
                                self.source_reader.absolute_pos,)

        if is_identifier_start(first_character):
            return IdentifierSubLexer(self.source_reader).get()

        if is_numeric_start(first_character):
            return NumericalLiteralSubLexer(self.source_reader).get()

        if is_string_literal_bound(first_character):
            return StringLiteralSubLexer(self.source_reader).get()

        if is_timedelta_literal_bound(first_character):
            return TimedeltaLiteralSubLexer(self.source_reader).get()

        if is_ambiguous_binary_start(first_character):
            return AmbiguousBinarySubLexer(self.source_reader).get()

        if is_unambiguous_singular_start(first_character):
            return UnambiguousSingularSubLexer(self.source_reader).get()

        message = "Unexpected character, not recognizable by any rule"
        error_handling.report_lexical_error(self.source_reader.line_num,
                                            self.source_reader.line_pos,
                                            self.source_reader.absolute_pos,
                                            self.source_reader,
                                            message)
        raise error_handling.LexicalError(message)
