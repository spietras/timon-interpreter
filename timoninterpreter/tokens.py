"""

Module containing lexical tokens and related info

"""
import calendar

from datetime import date, time, datetime, timedelta
from enum import Enum, auto
from functools import total_ordering


class NoValueEnum(Enum):
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)


class TokenType(NoValueEnum):
    IDENTIFIER = auto()
    FUN = auto()
    VAR = auto()
    IF = auto()
    ELSE = auto()
    FROM = auto()
    PRINT = auto()
    RETURN = auto()
    TO = auto()
    BY = auto()
    AS = auto()
    YEARS = auto()
    MONTHS = auto()
    WEEKS = auto()
    DAYS = auto()
    HOURS = auto()
    MINUTES = auto()
    SECONDS = auto()
    SEMICOLON = auto()
    LEFT_PARENTHESIS = auto()
    RIGHT_PARENTHESIS = auto()
    COMMA = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    ASSIGN = auto()
    LOGICAL_OR = auto()
    LOGICAL_AND = auto()
    EQUALS = auto()
    NOT_EQUALS = auto()
    GREATER = auto()
    GREATER_OR_EQUAL = auto()
    LESS = auto()
    LESS_OR_EQUAL = auto()
    NOT = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()
    ACCESS = auto()
    END = auto()
    STRING_LITERAL = auto()
    NUMBER_LITERAL = auto()
    DATE_LITERAL = auto()
    DATETIME_LITERAL = auto()
    TIME_LITERAL = auto()
    TIMEDELTA_LITERAL = auto()

    def __str__(self):
        if self in static_type_to_string_map:
            return static_type_to_string_map[self]

        return str(self.name)

    def __repr__(self):
        return self.__str__()


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
    '=': {"second_character": '=', "first_case_token_type": TokenType.ASSIGN,
          "second_case_token_type": TokenType.EQUALS},
    '!': {"second_character": '=', "first_case_token_type": TokenType.NOT,
          "second_case_token_type": TokenType.NOT_EQUALS},
    '>': {"second_character": '=', "first_case_token_type": TokenType.GREATER,
          "second_case_token_type": TokenType.GREATER_OR_EQUAL},
    '<': {"second_character": '=', "first_case_token_type": TokenType.LESS,
          "second_case_token_type": TokenType.LESS_OR_EQUAL},
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
    "fun": TokenType.FUN,
    "var": TokenType.VAR,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "from": TokenType.FROM,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "to": TokenType.TO,
    "by": TokenType.BY,
    "as": TokenType.AS,
    "years": TokenType.YEARS,
    "months": TokenType.MONTHS,
    "weeks": TokenType.WEEKS,
    "days": TokenType.DAYS,
    "hours": TokenType.HOURS,
    "minutes": TokenType.MINUTES,
    "seconds": TokenType.SECONDS
}

additional_identifier_characters = ['_']

static_type_to_string_map = {}
static_type_to_string_map.update({v: k for k, v in keyword_token_type_map.items()})
static_type_to_string_map.update({v: k for k, v in unambiguous_singular_token_type_map.items()})
static_type_to_string_map.update({v["first_case_token_type"]: k for k, v in ambiguous_binary_token_type_map.items()})
static_type_to_string_map.update(
    {v["second_case_token_type"]: k + v["second_character"] for k, v in ambiguous_binary_token_type_map.items()})


@total_ordering
class DateValue:
    def __init__(self, day, month, year):
        try:
            self._date = date(year, month, day)
        except ValueError as e:
            raise ValueError(
                "{}. Passed values were: year={}, month={}, day={}".format(str(e).capitalize(), year, month, day))

    def __eq__(self, other):
        if isinstance(other, DateTimeValue):
            return DateTimeValue(self.get_day(), self.get_month(), self.get_year(), 0, 0, 0) == other
        if isinstance(other, DateValue):
            return self._date == other._date
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, DateTimeValue):
            return DateTimeValue(self.get_day(), self.get_month(), self.get_year(), 0, 0, 0) < other
        if isinstance(other, DateValue):
            return self._date < other._date
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, TimeValue):
            return DateTimeValue(self.get_day(), self.get_month(), self.get_year(),
                                 other.get_hour(), other.get_minute(), other.get_second())
        if isinstance(other, TimedeltaValue):
            return DateTimeValue(self.get_day(), self.get_month(), self.get_year(), 0, 0, 0) + other
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, DateValue):
            return DateTimeValue(self.get_day(), self.get_month(), self.get_year(), 0, 0, 0) - DateTimeValue(
                other.get_day(), other.get_month(), other.get_year(), 0, 0, 0)
        if isinstance(other, DateTimeValue):
            return DateTimeValue(self.get_day(), self.get_month(), self.get_year(), 0, 0, 0) - other
        if isinstance(other, TimedeltaValue):
            return self + (-other)

        return NotImplemented

    def get_date(self):
        return self._date

    def get_year(self):
        return self._date.year

    def get_month(self):
        return self._date.month

    def get_day(self):
        return self._date.day

    def __str__(self):
        return self._date.strftime("%d{0}%m{0}%Y".format(DATE_SEPARATOR))


@total_ordering
class TimeValue:
    def __init__(self, hour, minute, second):
        try:
            self._time = time(hour, minute, second)
        except ValueError as e:
            raise ValueError(
                "{}. Passed values were: hour={}, minute={}, second={}".format(str(e).capitalize(), hour, minute,
                                                                               second))

    def __eq__(self, other):
        if isinstance(other, DateTimeValue):
            return DateTimeValue(1, 1, 1, self.get_hour(), self.get_minute(), self.get_second()) == other
        if isinstance(other, TimeValue):
            return self._time == other._time
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, DateTimeValue):
            return DateTimeValue(1, 1, 1, self.get_hour(), self.get_minute(), self.get_second()) < other
        if isinstance(other, TimeValue):
            return self._time < other._time
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, DateValue):
            return DateTimeValue(other.get_day(), other.get_month(), other.get_year(),
                                 self.get_hour(), self.get_minute(), self.get_second())
        if isinstance(other, TimedeltaValue):
            return DateTimeValue(1, 1, 1, self.get_hour(), self.get_minute(), self.get_second()) + other
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, TimeValue):
            return DateTimeValue(1, 1, 1, self.get_hour(), self.get_minute(), self.get_second()) - DateTimeValue(1, 1,
                                                                                                                 1,
                                                                                                                 other.get_hour(),
                                                                                                                 other.get_minute(),
                                                                                                                 other.get_second())
        if isinstance(other, DateTimeValue):
            return DateTimeValue(other.get_day(), other.get_month(), other.get_year(), self.get_hour(),
                                 self.get_minute(), self.get_second()) - other
        if isinstance(other, TimedeltaValue):
            return self + (-other)

        return NotImplemented

    def get_time(self):
        return self._time

    def get_hour(self):
        return self._time.hour

    def get_minute(self):
        return self._time.minute

    def get_second(self):
        return self._time.second

    def __str__(self):
        return self._time.strftime("%H{0}%M{0}%S".format(TIME_SEPARATOR))


@total_ordering
class DateTimeValue:
    @staticmethod
    def add_years_and_months(source_date, years=0, months=0):
        new_month = source_date.month - 1 + months
        new_year = source_date.year + new_month // 12
        new_month = new_month % 12 + 1
        new_day = min(source_date.day, calendar.monthrange(new_year, new_month)[1])
        new_date = source_date.replace(year=new_year, month=new_month, day=new_day)
        try:
            return new_date.replace(year=new_date.year + years)
        except ValueError:
            return new_date.replace(year=new_date.year + years, month=2, day=28)

    @staticmethod
    def get_years_and_months_diff(left_date, right_date):
        if isinstance(left_date, datetime):
            left_date = left_date.date()
        if isinstance(right_date, datetime):
            right_date = right_date.date()
        t = date(left_date.year, right_date.month,
                 min(right_date.day, calendar.monthrange(left_date.year, right_date.month)[1]))
        years_diff = (left_date.year - right_date.year) - (1 if left_date < t else 0)
        t = date(left_date.year, left_date.month,
                 min(right_date.day, calendar.monthrange(left_date.year, left_date.month)[1]))
        month_diff = ((left_date.month - right_date.month) - (1 if left_date < t else 0)) % 12
        return years_diff, month_diff

    @staticmethod
    def get_weeks_days_hours_minutes_seconds_diff(left_date, right_date):
        td = left_date - right_date
        weeks = td.days // 7
        td -= timedelta(weeks=weeks)
        days = td.days
        td -= timedelta(days=days)
        hours = td.seconds // 3600
        td -= timedelta(hours=hours)
        minutes = td.seconds // 60
        td -= timedelta(minutes=minutes)
        seconds = td.seconds
        return weeks, days, hours, minutes, seconds

    def __init__(self, day, month, year, hour, minute, second):
        self._date_value = DateValue(day, month, year)
        self._time_value = TimeValue(hour, minute, second)

    def __eq__(self, other):
        if isinstance(other, DateTimeValue):
            return self._date_value == other._date_value and self._time_value == other._time_value
        if isinstance(other, DateValue):
            return self == DateTimeValue(other.get_day(), other.get_month(), other.get_year(), 0, 0, 0)
        if isinstance(other, TimeValue):
            return self == DateTimeValue(1, 1, 1, self.get_hour(), self.get_minute(), self.get_second())
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, DateTimeValue):
            return self._date_value < other._date_value or (
                    self._date_value == other._date_value and self._time_value < other._time_value)
        if isinstance(other, DateValue):
            return self < DateTimeValue(other.get_day(), other.get_month(), other.get_year(), 0, 0, 0)
        if isinstance(other, TimeValue):
            return self < DateTimeValue(1, 1, 1, other.get_hour(), other.get_minute(), other.get_second())
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, TimedeltaValue):
            dt = self.get_datetime()
            dt = self.add_years_and_months(dt, other.get_years(), other.get_months())
            dt = dt + timedelta(weeks=other.get_weeks(),
                                days=other.get_days(),
                                hours=other.get_hours(),
                                minutes=other.get_minutes(),
                                seconds=other.get_seconds())
            return DateTimeValue(dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second)

        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, DateTimeValue):
            self_dt = self.get_datetime()
            other_dt = other.get_datetime()
            years, months = self.get_years_and_months_diff(self_dt, other_dt)
            other_dt = self.add_years_and_months(other_dt, years, months)
            weeks, days, hours, minutes, seconds = self.get_weeks_days_hours_minutes_seconds_diff(self_dt, other_dt)
            return TimedeltaValue(years, months, weeks, days, hours, minutes, seconds)
        if isinstance(other, DateValue):
            return self - DateTimeValue(other.get_day(), other.get_month(), other.get_year(), 0, 0, 0)
        if isinstance(other, TimeValue):
            return self - DateTimeValue(1, 1, 1, other.get_hour(), other.get_minute(), other.get_second())
        if isinstance(other, TimedeltaValue):
            return self + (-other)

        return NotImplemented

    def get_datetime(self):
        return datetime.combine(self._date_value.get_date(), self._time_value.get_time())

    def get_year(self):
        return self._date_value.get_year()

    def get_month(self):
        return self._date_value.get_month()

    def get_day(self):
        return self._date_value.get_day()

    def get_hour(self):
        return self._time_value.get_hour()

    def get_minute(self):
        return self._time_value.get_minute()

    def get_second(self):
        return self._time_value.get_second()

    def __str__(self):
        return str(self._date_value) + DATETIME_SEPARATOR + str(self._time_value)


@total_ordering
class TimedeltaValue:
    def __init__(self, years=0, months=0, weeks=0, days=0, hours=0, minutes=0, seconds=0):
        self._years = years or 0
        self._months = months or 0
        self._weeks = weeks or 0
        self._days = days or 0
        self._hours = hours or 0
        self._minutes = minutes or 0
        self._seconds = seconds or 0

    def __eq__(self, other):
        if not isinstance(other, TimedeltaValue):
            return NotImplemented

        self_total_months = self._years * 12 + self._months
        other_total_months = other._years * 12 + other._months
        self_total_seconds_less_than_month = self._seconds + 60 * (self._minutes + 60 * (self._days + 7 * self._weeks))
        other_total_seconds_less_than_month = other._seconds + 60 * (
                other._minutes + 60 * (other._days + 7 * other._weeks))

        if self_total_seconds_less_than_month != other_total_seconds_less_than_month:
            return False

        return self_total_months == other_total_months

    def __lt__(self, other):
        if not isinstance(other, TimedeltaValue):
            return NotImplemented

        self_total_months = self._years * 12 + self._months
        other_total_months = other._years * 12 + other._months
        self_total_seconds_less_than_month = self._seconds + 60 * (
                    self._minutes + 60 * (self._hours + 24 * (self._days + 7 * self._weeks)))
        other_total_seconds_less_than_month = other._seconds + 60 * (
                other._minutes + 60 * (other._hours + 24 * (other._days + 7 * other._weeks)))

        return (self_total_months * 31) + (self_total_seconds_less_than_month // (60 * 60 * 24)) < (
                other_total_months * 31) + (other_total_seconds_less_than_month // (60 * 60 * 24))

    def __add__(self, other):
        if isinstance(other, TimedeltaValue):
            return TimedeltaValue(self.get_years() + other.get_years(),
                                  self.get_months() + other.get_months(),
                                  self.get_weeks() + other.get_weeks(),
                                  self.get_days() + other.get_days(),
                                  self.get_hours() + other.get_hours(),
                                  self.get_minutes() + other.get_minutes(),
                                  self.get_seconds() + other.get_seconds())

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, TimedeltaValue):
            return self + (-other)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, int):
            return TimedeltaValue(self.get_years() * other,
                                  self.get_months() * other,
                                  self.get_weeks() * other,
                                  self.get_days() * other,
                                  self.get_hours() * other,
                                  self.get_minutes() * other,
                                  self.get_seconds() * other)
        return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, (int, float)):
            return TimedeltaValue(self.get_years() // other,
                                  self.get_months() // other,
                                  self.get_weeks() // other,
                                  self.get_days() // other,
                                  self.get_hours() // other,
                                  self.get_minutes() // other,
                                  self.get_seconds() // other)
        return NotImplemented

    def __neg__(self):
        return TimedeltaValue(-self.get_years(),
                              -self.get_months(),
                              -self.get_weeks(),
                              -self.get_days(),
                              -self.get_hours(),
                              -self.get_minutes(),
                              -self.get_seconds())

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
    TokenType.IDENTIFIER: str,
    TokenType.STRING_LITERAL: str,
    TokenType.NUMBER_LITERAL: int,
    TokenType.DATE_LITERAL: DateValue,
    TokenType.DATETIME_LITERAL: DateTimeValue,
    TokenType.TIME_LITERAL: TimeValue,
    TokenType.TIMEDELTA_LITERAL: TimedeltaValue
}


class Token:
    """
    Token class
    """

    def __init__(self, token_type, file_pos, value=None):
        value_type = token_value_valid_types_map.get(token_type, type(None))
        if type(value) is not value_type:
            raise ValueError(
                "Token value type mismatch. Expected {}, but got {} for {}".format(value_type, type(value), token_type))
        self._type = token_type
        self._value = value
        self._file_pos = file_pos

    def __str__(self):
        if self._type == TokenType.END:
            return "END"

        if self._type == TokenType.STRING_LITERAL:
            return '{0}{1}{0}'.format(STRING_BOUND, self._value)

        if self._value is None:
            return static_type_to_string_map[self._type]

        return str(self._value)

    def get_type(self):
        """
        Returns:
            type of the token
        """
        return self._type

    def get_value(self):
        """
        Returns:
            value of the token:
               - string for IDENTIFIER
               - string for STRING_LITERAL
               - int for NUMBER_LITERAL
               - DateValue for DATE_LITERAL
               - DateTimeValue for DATETIME_LITERAL
               - TimeValue for TIME_LITERAL
               - TimedeltaValue for TIMEDELTA_LITERAL
               - None for others
        """
        return self._value

    def get_file_pos(self):
        """
        Returns:
            position of token in the file
        """
        return self._file_pos
