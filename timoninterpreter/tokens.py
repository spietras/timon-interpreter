"""

Module containing lexical tokens and related info

"""

from enum import Enum, auto
from datetime import date, time


class NoValueEnum(Enum):
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)


class TokenType(NoValueEnum):
    IDENTIFIER          = auto()
    FUN                 = auto()
    VAR                 = auto()
    IF                  = auto()
    ELSE                = auto()
    FROM                = auto()
    PRINT               = auto()
    RETURN              = auto()
    TO                  = auto()
    BY                  = auto()
    AS                  = auto()
    YEARS               = auto()
    MONTHS              = auto()
    WEEKS               = auto()
    DAYS                = auto()
    HOURS               = auto()
    MINUTES             = auto()
    SECONDS             = auto()
    SEMICOLON           = auto()
    LEFT_PARENTHESIS    = auto()
    RIGHT_PARENTHESIS   = auto()
    COMMA               = auto()
    LEFT_BRACKET        = auto()
    RIGHT_BRACKET       = auto()
    ASSIGN              = auto()
    LOGICAL_OR          = auto()
    LOGICAL_AND         = auto()
    EQUALS              = auto()
    NOT_EQUALS          = auto()
    GREATER             = auto()
    GREATER_OR_EQUAL    = auto()
    LESS                = auto()
    LESS_OR_EQUAL       = auto()
    NOT                 = auto()
    PLUS                = auto()
    MINUS               = auto()
    MULTIPLICATION      = auto()
    DIVISION            = auto()
    ACCESS              = auto()
    END                 = auto()
    STRING_LITERAL      = auto()
    NUMBER_LITERAL      = auto()
    DATE_LITERAL        = auto()
    DATETIME_LITERAL    = auto()
    TIME_LITERAL        = auto()
    TIMEDELTA_LITERAL   = auto()


# Processed from bound to bound
COMMENT_BOUND = '#'
STRING_BOUND = '"'
TIMEDELTA_BOUND = "'"

DATE_SEPARATOR = '.'
TIME_SEPARATOR = ':'
DATETIME_SEPARATOR = '~'

ESCAPE = '\\'

# Ambiguous characters, determining token after first and second character
ambiguous_binary_token_type_map = {
    '=': {"second_character": '=', "first_case_token_type": TokenType.ASSIGN, "second_case_token_type": TokenType.EQUALS},
    '!': {"second_character": '=', "first_case_token_type": TokenType.NOT, "second_case_token_type": TokenType.NOT_EQUALS},
    '>': {"second_character": '=', "first_case_token_type": TokenType.GREATER, "second_case_token_type": TokenType.GREATER_OR_EQUAL},
    '<': {"second_character": '=', "first_case_token_type": TokenType.LESS, "second_case_token_type": TokenType.LESS_OR_EQUAL},
}

# Unambiguous single character tokens
unambiguous_singular_token_type_map = {
    ';': TokenType.SEMICOLON,
    '(': TokenType.LEFT_PARENTHESIS,
    ')': TokenType.RIGHT_PARENTHESIS,
    '{': TokenType.LEFT_BRACKET,
    '}': TokenType.RIGHT_BRACKET,
    '.': TokenType.ACCESS,
    '|': TokenType.LOGICAL_OR,
    '&': TokenType.LOGICAL_AND,
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MULTIPLICATION,
    '/': TokenType.DIVISION,
    ',': TokenType.COMMA,
}


keyword_token_type_map = {
    "fun"       : TokenType.FUN,
    "var"       : TokenType.VAR,
    "if"        : TokenType.IF,
    "else"      : TokenType.ELSE,
    "from"      : TokenType.FROM,
    "print"     : TokenType.PRINT,
    "return"    : TokenType.RETURN,
    "to"        : TokenType.TO,
    "by"        : TokenType.BY,
    "as"        : TokenType.AS,
    "years"     : TokenType.YEARS,
    "months"    : TokenType.MONTHS,
    "weeks"     : TokenType.WEEKS,
    "days"      : TokenType.DAYS,
    "hours"     : TokenType.HOURS,
    "minutes"   : TokenType.MINUTES,
    "seconds"   : TokenType.SECONDS
}

additional_identifier_characters = ['_']

static_type_to_string_map = {}
static_type_to_string_map.update({v: k for k, v in keyword_token_type_map.items()})
static_type_to_string_map.update({v: k for k, v in unambiguous_singular_token_type_map.items()})
static_type_to_string_map.update({v["first_case_token_type"]: k for k, v in ambiguous_binary_token_type_map.items()})
static_type_to_string_map.update({v["second_case_token_type"]: k + v["second_character"] for k, v in ambiguous_binary_token_type_map.items()})


class DateValue:
    def __init__(self, day, month, year):
        try:
            self._date = date(year, month, day)
        except ValueError as e:
            raise ValueError("{}. Passed values were: year={}, month={}, day={}".format(str(e).capitalize(), year, month, day))

    def __eq__(self, other):
        if not isinstance(other, DateValue):
            return NotImplemented

        return self._date == other._date

    def get_year(self):
        return self._date.year

    def get_month(self):
        return self._date.month

    def get_day(self):
        return self._date.day

    def __str__(self):
        return self._date.strftime("%d{0}%m{0}%Y".format(DATE_SEPARATOR))


class TimeValue:
    def __init__(self, hour, minute, second):
        try:
            self._time = time(hour, minute, second)
        except ValueError as e:
            raise ValueError("{}. Passed values were: hour={}, minute={}, second={}".format(str(e).capitalize(), hour, minute, second))

    def __eq__(self, other):
        if not isinstance(other, TimeValue):
            return NotImplemented

        return self._time == other._time

    def get_hour(self):
        return self._time.hour

    def get_minute(self):
        return self._time.minute

    def get_second(self):
        return self._time.second

    def __str__(self):
        return self._time.strftime("%H{0}%M{0}%S".format(TIME_SEPARATOR))


class DateTimeValue(DateValue, TimeValue):
    def __init__(self, day, month, year, hour, minute, second):
        DateValue.__init__(self, day, month, year)
        TimeValue.__init__(self, hour, minute, second)

    def __eq__(self, other):
        if not isinstance(other, DateTimeValue):
            return NotImplemented

        return DateValue.__eq__(self, other) and TimeValue.__eq__(self, other)

    def __str__(self):
        return DateValue.__str__(self) + DATETIME_SEPARATOR + TimeValue.__str__(self)


class TimedeltaValue:
    def __init__(self, years=None, months=None, weeks=None, days=None, hours=None, minutes=None, seconds=None):
        self._set_time_value("_years",   years)
        self._set_time_value("_months",  months)
        self._set_time_value("_weeks",   weeks)
        self._set_time_value("_days",    days)
        self._set_time_value("_hours",   hours)
        self._set_time_value("_minutes", minutes)
        self._set_time_value("_seconds", seconds)

    def _set_time_value(self, attribute_name, value):
        value = int(value or 0)

        if value < 0:
            raise ValueError("Attribute {} can't be negative. Passed value was {}".format(attribute_name, value))

        setattr(self, attribute_name, value)

    def __eq__(self, other):
        if not isinstance(other, TimedeltaValue):
            return NotImplemented

        return vars(self) == vars(other)

    def get_years(self):
        return self._years

    def get_months(self):
        return self._months

    def get_weeks(self):
        return self._weeks

    def get_days(self):
        return self._days

    def get_hours(self):
        return self._hours

    def get_minutes(self):
        return self._minutes

    def get_seconds(self):
        return self._seconds

    def _time_value_to_string(self, attribute_name):
        abbreviations_map = {
            "_years": "Y",
            "_months": "M",
            "_weeks": "W",
            "_days": "D",
            "_hours": "h",
            "_minutes": "m",
            "_seconds": "s"
        }

        return str(getattr(self, attribute_name)) + abbreviations_map[attribute_name]

    def __str__(self):
        return "{0}{1}{0}".format(TIMEDELTA_BOUND, ' '.join(self._time_value_to_string(a) for a in ['_years',
                                                                                                    '_months',
                                                                                                    '_weeks',
                                                                                                    '_days',
                                                                                                    '_hours',
                                                                                                    '_minutes',
                                                                                                    '_seconds']))


token_value_valid_types_map = {
    TokenType.IDENTIFIER        : str,
    TokenType.STRING_LITERAL    : str,
    TokenType.NUMBER_LITERAL    : int,
    TokenType.DATE_LITERAL      : DateValue,
    TokenType.DATETIME_LITERAL  : DateTimeValue,
    TokenType.TIME_LITERAL      : TimeValue,
    TokenType.TIMEDELTA_LITERAL : TimedeltaValue
}


class Token:
    """
    Token class

    Attributes:
        type: type of the token
        value: value of the token
               - string for IDENTIFIER
               - string for STRING_LITERAL
               - int for NUMBER_LITERAL
               - DateValue for DATE_LITERAL
               - DateTimeValue for DATETIME_LITERAL
               - TimeValue for TIME_LITERAL
               - TimedeltaValue for TIMEDELTA_LITERAL
               - None for others
        line_num: number of line where the token was found
        line_pos: position in line where the token was found
        absolute_pos: position from the beginning where the token was found
    """
    def __init__(self, token_type, line_num, line_pos, absolute_pos, value=None):
        value_type = token_value_valid_types_map.get(token_type, type(None))
        if type(value) is not value_type:
            raise ValueError("Token value type mismatch. Expected {}, but got {} for {}".format(value_type, type(value), token_type))
        self.type = token_type
        self.value = value
        self.line_num = line_num
        self.line_pos = line_pos
        self.absolute_pos = absolute_pos

    def __str__(self):
        if self.type == TokenType.END:
            return "END"

        if self.type == TokenType.STRING_LITERAL:
            return '{0}{1}{0}'.format(STRING_BOUND, self.value)

        if self.value is None:
            return static_type_to_string_map[self.type]

        return str(self.value)
