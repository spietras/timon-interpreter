import unittest

from timoninterpreter import tokens


class DateValueTestCase(unittest.TestCase):
    def test_date_value_correctly_construct(self):
        v = tokens.DateValue(27, 5, 2020)
        self.assertEqual(27, v.get_day())
        self.assertEqual(5, v.get_month())
        self.assertEqual(2020, v.get_year())

    def test_date_value_bad_day(self):
        self.assertRaises(ValueError, tokens.DateValue, 31, 4, 2020)

    def test_date_value_bad_month(self):
        self.assertRaises(ValueError, tokens.DateValue, 1, 13, 2020)

    def test_date_value_leap_year(self):
        v = tokens.DateValue(29, 2, 2020)
        self.assertEqual(29, v.get_day())
        self.assertEqual(2, v.get_month())
        self.assertEqual(2020, v.get_year())

    def test_date_value_not_leap_year(self):
        self.assertRaises(ValueError, tokens.DateValue, 29, 2, 2019)

    def test_date_value_equals_date_value(self):
        self.assertTrue(tokens.DateValue(27, 5, 2020) == tokens.DateValue(27, 5, 2020))

    def test_date_value_not_equals_date_value(self):
        self.assertFalse(tokens.DateValue(27, 5, 2020) == tokens.DateValue(28, 5, 2020))

    def test_date_value_equals_datetime_value(self):
        self.assertTrue(tokens.DateValue(27, 5, 2020) == tokens.DateTimeValue(27, 5, 2020, 0, 0, 0))

    def test_date_value_not_equals_datetime_value(self):
        self.assertFalse(tokens.DateValue(27, 5, 2020) == tokens.DateTimeValue(27, 5, 2020, 0, 0, 1))

    def test_date_value_equals_time_value(self):
        self.assertFalse(tokens.DateValue(27, 5, 2020) == tokens.TimeValue(19, 0, 0))

    def test_date_value_less_date_value(self):
        self.assertTrue(tokens.DateValue(27, 5, 2020) < tokens.DateValue(28, 5, 2020))

    def test_date_value_not_less_date_value(self):
        self.assertFalse(tokens.DateValue(27, 5, 2020) < tokens.DateValue(26, 5, 2020))

    def test_date_value_less_datetime_value(self):
        self.assertTrue(tokens.DateValue(27, 5, 2020) < tokens.DateTimeValue(27, 5, 2020, 0, 0, 1))

    def test_date_value_not_less_datetime_value(self):
        self.assertFalse(tokens.DateValue(27, 5, 2020) < tokens.DateTimeValue(26, 5, 2020, 23, 59, 59))

    def test_date_value_less_time_value(self):
        with self.assertRaises(TypeError):
            v = tokens.DateValue(27, 5, 2020) < tokens.TimeValue(19, 0, 0)

    def test_date_value_add_time_value(self):
        self.assertEqual(tokens.DateValue(27, 5, 2020) + tokens.TimeValue(19, 0, 0),
                         tokens.DateTimeValue(27, 5, 2020, 19, 0, 0))

    def test_date_value_add_timedelta_value(self):
        self.assertEqual(tokens.DateValue(27, 5, 2020) + tokens.TimedeltaValue(days=10),
                         tokens.DateTimeValue(6, 6, 2020, 0, 0, 0))

    def test_date_value_add_timedelta_value_different_month_days(self):
        self.assertEqual(tokens.DateValue(31, 5, 2020) + tokens.TimedeltaValue(months=1),
                         tokens.DateTimeValue(30, 6, 2020, 0, 0, 0))

    def test_date_value_add_timedelta_value_leap_year(self):
        self.assertEqual(tokens.DateValue(29, 2, 2020) + tokens.TimedeltaValue(years=1),
                         tokens.DateTimeValue(28, 2, 2021, 0, 0, 0))

    def test_date_value_add_timedelta_value_different_month_days_and_leap_year(self):
        self.assertEqual(tokens.DateValue(29, 2, 2020) + tokens.TimedeltaValue(years=1, months=1),
                         tokens.DateTimeValue(29, 3, 2021, 0, 0, 0))
        self.assertEqual(tokens.DateValue(31, 1, 2020) + tokens.TimedeltaValue(years=1, months=1),
                         tokens.DateTimeValue(28, 2, 2021, 0, 0, 0))

    def test_date_value_add_date_value(self):
        with self.assertRaises(TypeError):
            tokens.DateValue(27, 5, 2020) + tokens.DateValue(28, 5, 2020)

    def test_date_value_add_datetime_value(self):
        with self.assertRaises(TypeError):
            val = tokens.DateValue(27, 5, 2020) + tokens.DateTimeValue(28, 5, 2020, 19, 0, 0)

    def test_date_value_sub_timedelta_value(self):
        self.assertEqual(tokens.DateValue(6, 6, 2020) - tokens.TimedeltaValue(days=10),
                         tokens.DateTimeValue(27, 5, 2020, 0, 0, 0))

    def test_date_value_sub_timedelta_value_different_month_days(self):
        self.assertEqual(tokens.DateValue(31, 5, 2020) - tokens.TimedeltaValue(months=1),
                         tokens.DateTimeValue(30, 4, 2020, 0, 0, 0))

    def test_date_value_sub_timedelta_value_leap_year(self):
        self.assertEqual(tokens.DateValue(29, 2, 2020) + tokens.TimedeltaValue(years=1),
                         tokens.DateTimeValue(28, 2, 2021, 0, 0, 0))

    def test_date_value_sub_timedelta_value_different_month_days_and_leap_year(self):
        self.assertEqual(tokens.DateValue(29, 2, 2020) - tokens.TimedeltaValue(years=1, months=1),
                         tokens.DateTimeValue(29, 1, 2019, 0, 0, 0))
        self.assertEqual(tokens.DateValue(31, 3, 2020) - tokens.TimedeltaValue(years=1, months=1),
                         tokens.DateTimeValue(28, 2, 2019, 0, 0, 0))

    def test_date_value_sub_date_value(self):
        self.assertEqual(tokens.DateValue(29, 2, 2020) - tokens.DateValue(28, 2, 2020), tokens.TimedeltaValue(days=1))

    def test_date_value_sub_date_value_different_month_days(self):
        self.assertEqual(tokens.DateValue(30, 6, 2020) - tokens.DateValue(31, 5, 2020),
                         tokens.TimedeltaValue(months=1))

    def test_date_value_sub_date_value_leap_year(self):
        self.assertEqual(tokens.DateValue(28, 2, 2021) - tokens.DateValue(29, 2, 2020), tokens.TimedeltaValue(years=1))

    def test_date_value_sub_date_value_different_month_days_and_leap_year(self):
        self.assertEqual(tokens.DateValue(29, 3, 2021) - tokens.DateValue(29, 2, 2020),
                         tokens.TimedeltaValue(years=1, months=1))
        self.assertEqual(tokens.DateValue(28, 2, 2021) - tokens.DateValue(31, 1, 2020),
                         tokens.TimedeltaValue(years=1, months=1))

    def test_date_value_sub_datetime_value(self):
        self.assertEqual(tokens.DateValue(28, 2, 2021) - tokens.DateTimeValue(27, 2, 2021, 23, 59, 59),
                         tokens.TimedeltaValue(seconds=1))

    def test_date_value_sub_datetime_value_different_month_days(self):
        self.assertEqual(tokens.DateValue(30, 6, 2020) - tokens.DateTimeValue(31, 5, 2020, 0, 0, 0),
                         tokens.TimedeltaValue(months=1))

    def test_date_value_sub_datetime_value_leap_year(self):
        self.assertEqual(tokens.DateValue(28, 2, 2021) - tokens.DateTimeValue(29, 2, 2020, 0, 0, 0),
                         tokens.TimedeltaValue(years=1))

    def test_date_value_sub_datetime_value_different_month_days_and_leap_year(self):
        self.assertEqual(tokens.DateValue(29, 3, 2021) - tokens.DateTimeValue(29, 2, 2020, 0, 0, 0),
                         tokens.TimedeltaValue(years=1, months=1))
        self.assertEqual(tokens.DateValue(28, 2, 2021) - tokens.DateTimeValue(31, 1, 2020, 0, 0, 0),
                         tokens.TimedeltaValue(years=1, months=1))

    def test_date_value_sub_time_value(self):
        with self.assertRaises(TypeError):
            val = tokens.DateValue(27, 5, 2020) - tokens.TimeValue(19, 0, 0)


class TimeValueTestCase(unittest.TestCase):
    def test_time_value_correctly_construct(self):
        v = tokens.TimeValue(20, 37, 35)
        self.assertEqual(20, v.get_hour())
        self.assertEqual(37, v.get_minute())
        self.assertEqual(35, v.get_second())

    def test_time_value_bad_hour(self):
        self.assertRaises(ValueError, tokens.DateValue, 25, 37, 35)

    def test_time_value_bad_minute(self):
        self.assertRaises(ValueError, tokens.DateValue, 20, 60, 35)

    def test_time_value_bad_second(self):
        self.assertRaises(ValueError, tokens.DateValue, 20, 37, 60)

    def test_time_value_equals_time_value(self):
        self.assertTrue(tokens.TimeValue(20, 37, 35) == tokens.TimeValue(20, 37, 35))

    def test_time_value_not_equals_time_value(self):
        self.assertFalse(tokens.TimeValue(20, 37, 35) == tokens.TimeValue(20, 37, 36))

    def test_time_value_equals_datetime_value(self):
        self.assertTrue(tokens.TimeValue(20, 37, 35) == tokens.DateTimeValue(1, 1, 1, 20, 37, 35))

    def test_time_value_not_equals_datetime_value(self):
        self.assertFalse(tokens.TimeValue(20, 37, 35) == tokens.DateTimeValue(2, 1, 1, 20, 37, 35))

    def test_time_value_equals_date_value(self):
        self.assertFalse(tokens.TimeValue(19, 0, 0) == tokens.DateValue(27, 5, 2020))

    def test_time_value_less_time_value(self):
        self.assertTrue(tokens.TimeValue(20, 37, 35) < tokens.TimeValue(20, 37, 36))

    def test_time_value_not_less_time_value(self):
        self.assertFalse(tokens.TimeValue(20, 37, 35) < tokens.TimeValue(20, 37, 34))

    def test_time_value_less_datetime_value(self):
        self.assertTrue(tokens.TimeValue(20, 37, 35) < tokens.DateTimeValue(1, 1, 1, 20, 37, 36))

    def test_time_value_not_less_datetime_value(self):
        self.assertFalse(tokens.TimeValue(20, 37, 35) < tokens.DateTimeValue(1, 1, 1, 20, 37, 34))

    def test_time_value_less_date_value(self):
        with self.assertRaises(TypeError):
            v = tokens.TimeValue(19, 0, 0) < tokens.DateValue(27, 5, 2020)

    def test_time_value_add_date_value(self):
        self.assertEqual(tokens.TimeValue(19, 0, 0) + tokens.DateValue(27, 5, 2020),
                         tokens.DateTimeValue(27, 5, 2020, 19, 0, 0))

    def test_time_value_add_timedelta_value(self):
        self.assertEqual(tokens.TimeValue(20, 37, 35) + tokens.TimedeltaValue(minutes=30),
                         tokens.DateTimeValue(1, 1, 1, 21, 7, 35))

    def test_time_value_add_timedelta_value_another_day(self):
        self.assertEqual(tokens.TimeValue(20, 37, 35) + tokens.TimedeltaValue(hours=4),
                         tokens.DateTimeValue(2, 1, 1, 0, 37, 35))

    def test_time_value_add_time_value(self):
        with self.assertRaises(TypeError):
            tokens.TimeValue(20, 37, 35) + tokens.TimeValue(20, 37, 35)

    def test_time_value_add_datetime_value(self):
        with self.assertRaises(TypeError):
            val = tokens.TimeValue(20, 37, 35) + tokens.DateTimeValue(28, 5, 2020, 19, 0, 0)

    def test_time_value_sub_timedelta_value(self):
        self.assertEqual(tokens.TimeValue(20, 37, 35) - tokens.TimedeltaValue(minutes=40),
                         tokens.DateTimeValue(1, 1, 1, 19, 57, 35))

    def test_time_value_sub_timedelta_value_another_day(self):
        with self.assertRaises(OverflowError):
            val = tokens.TimeValue(20, 37, 35) - tokens.TimedeltaValue(hours=21)

    def test_time_value_sub_time_value(self):
        self.assertEqual(tokens.TimeValue(20, 37, 35) - tokens.TimeValue(19, 37, 35), tokens.TimedeltaValue(hours=1))

    def test_time_value_sub_datetime_value(self):
        self.assertEqual(tokens.TimeValue(20, 37, 35) - tokens.DateTimeValue(27, 2, 2021, 20, 27, 35),
                         tokens.TimedeltaValue(minutes=10))

    def test_time_value_sub_date_value(self):
        with self.assertRaises(TypeError):
            val = tokens.TimeValue(19, 0, 0) - tokens.DateValue(27, 5, 2020)


class DateTimeValueTestCase(unittest.TestCase):
    def test_datetime_value_correctly_construct(self):
        v = tokens.DateTimeValue(27, 5, 2020, 20, 37, 35)
        self.assertEqual(27, v.get_day())
        self.assertEqual(5, v.get_month())
        self.assertEqual(2020, v.get_year())
        self.assertEqual(20, v.get_hour())
        self.assertEqual(37, v.get_minute())
        self.assertEqual(35, v.get_second())

    def test_datetime_value_bad_day(self):
        self.assertRaises(ValueError, tokens.DateTimeValue, 31, 4, 2020, 0, 0, 0)

    def test_datetime_value_bad_month(self):
        self.assertRaises(ValueError, tokens.DateTimeValue, 1, 13, 2020, 0, 0, 0)

    def test_datetime_value_bad_hour(self):
        self.assertRaises(ValueError, tokens.DateTimeValue, 1, 1, 1, 25, 37, 35)

    def test_datetime_value_bad_minute(self):
        self.assertRaises(ValueError, tokens.DateTimeValue, 1, 1, 1, 20, 60, 35)

    def test_datetime_value_bad_second(self):
        self.assertRaises(ValueError, tokens.DateTimeValue, 1, 1, 1, 20, 37, 60)

    def test_datetime_value_leap_year(self):
        v = tokens.DateTimeValue(29, 2, 2020, 0, 0, 0)
        self.assertEqual(29, v.get_day())
        self.assertEqual(2, v.get_month())
        self.assertEqual(2020, v.get_year())

    def test_datetime_value_not_leap_year(self):
        self.assertRaises(ValueError, tokens.DateTimeValue, 29, 2, 2019, 0, 0, 0)

    def test_datetime_value_equals_datetime_value(self):
        self.assertTrue(tokens.DateTimeValue(27, 5, 2020, 20, 37, 35) == tokens.DateTimeValue(27, 5, 2020, 20, 37, 35))

    def test_datetime_value_not_equals_datetime_value(self):
        self.assertFalse(tokens.DateTimeValue(27, 5, 2020, 20, 37, 35) == tokens.DateTimeValue(28, 5, 2020, 20, 37, 36))

    def test_datetime_value_equals_date_value(self):
        self.assertTrue(tokens.DateTimeValue(27, 5, 2020, 0, 0, 0) == tokens.DateValue(27, 5, 2020))

    def test_datetime_value_not_equals_date_value(self):
        self.assertFalse(tokens.DateTimeValue(27, 5, 2020, 0, 0, 1) == tokens.DateValue(27, 5, 2020))

    def test_datetime_value_less_datetime_value(self):
        self.assertTrue(tokens.DateTimeValue(27, 5, 2020, 20, 37, 35) < tokens.DateTimeValue(27, 5, 2020, 20, 37, 36))

    def test_datetime_value_not_less_date_value(self):
        self.assertFalse(tokens.DateTimeValue(27, 5, 2020, 20, 37, 35) < tokens.DateTimeValue(27, 5, 2020, 20, 37, 34))

    def test_datetime_value_less_date_value(self):
        self.assertTrue(tokens.DateTimeValue(26, 5, 2020, 23, 59, 59) < tokens.DateValue(27, 5, 2020))

    def test_datetime_value_not_less_datetime_value(self):
        self.assertFalse(tokens.DateTimeValue(27, 5, 2020, 0, 0, 1) < tokens.DateValue(27, 5, 2020))

    def test_datetime_value_equals_time_value(self):
        self.assertTrue(tokens.DateTimeValue(1, 1, 1, 20, 37, 35) == tokens.TimeValue(20, 37, 35))

    def test_datetime_value_not_equals_time_value(self):
        self.assertFalse(tokens.DateTimeValue(2, 1, 1, 20, 37, 35) == tokens.TimeValue(20, 37, 35))

    def test_datetime_value_less_time_value(self):
        self.assertTrue(tokens.DateTimeValue(1, 1, 1, 20, 37, 35) < tokens.TimeValue(20, 37, 36))

    def test_datetime_value_not_less_time_value(self):
        self.assertFalse(tokens.DateTimeValue(1, 1, 1, 20, 37, 35) < tokens.TimeValue(20, 37, 34))

    def test_datetime_value_add_timedelta_value(self):
        self.assertEqual(tokens.DateTimeValue(27, 5, 2020, 20, 37, 35) + tokens.TimedeltaValue(days=10, minutes=30),
                         tokens.DateTimeValue(6, 6, 2020, 21, 7, 35))

    def test_datetime_value_add_timedelta_value_different_month_days(self):
        self.assertEqual(tokens.DateTimeValue(31, 5, 2020, 0, 0, 0) + tokens.TimedeltaValue(months=1),
                         tokens.DateTimeValue(30, 6, 2020, 0, 0, 0))

    def test_datetime_value_add_timedelta_value_leap_year(self):
        self.assertEqual(tokens.DateTimeValue(29, 2, 2020, 0, 0, 0) + tokens.TimedeltaValue(years=1),
                         tokens.DateTimeValue(28, 2, 2021, 0, 0, 0))

    def test_datetime_value_add_timedelta_value_different_month_days_and_leap_year(self):
        self.assertEqual(tokens.DateTimeValue(29, 2, 2020, 0, 0, 0) + tokens.TimedeltaValue(years=1, months=1),
                         tokens.DateTimeValue(29, 3, 2021, 0, 0, 0))
        self.assertEqual(tokens.DateTimeValue(31, 1, 2020, 0, 0, 0) + tokens.TimedeltaValue(years=1, months=1),
                         tokens.DateTimeValue(28, 2, 2021, 0, 0, 0))

    def test_datetime_value_add_timedelta_value_another_day(self):
        self.assertEqual(tokens.DateTimeValue(27, 5, 2020, 20, 37, 35) + tokens.TimedeltaValue(hours=4),
                         tokens.DateTimeValue(28, 5, 2020, 0, 37, 35))

    def test_datetime_value_add_date_value(self):
        with self.assertRaises(TypeError):
            tokens.DateTimeValue(27, 5, 2020, 20, 37, 35) + tokens.DateValue(28, 5, 2020)

    def test_datetime_value_add_time_value(self):
        with self.assertRaises(TypeError):
            tokens.DateTimeValue(27, 5, 2020, 20, 37, 35) + tokens.TimeValue(20, 37, 36)

    def test_datetime_value_add_datetime_value(self):
        with self.assertRaises(TypeError):
            tokens.DateTimeValue(27, 5, 2020, 20, 37, 35) + tokens.DateTimeValue(28, 5, 2020, 20, 37, 36)

    def test_datetime_value_sub_timedelta_value(self):
        self.assertEqual(tokens.DateTimeValue(6, 6, 2020, 20, 37, 35) - tokens.TimedeltaValue(days=10, minutes=40),
                         tokens.DateTimeValue(27, 5, 2020, 19, 57, 35))

    def test_datetime_value_sub_timedelta_value_different_month_days(self):
        self.assertEqual(tokens.DateTimeValue(31, 5, 2020, 0, 0, 0) - tokens.TimedeltaValue(months=1),
                         tokens.DateTimeValue(30, 4, 2020, 0, 0, 0))

    def test_datetime_value_sub_timedelta_value_leap_year(self):
        self.assertEqual(tokens.DateTimeValue(29, 2, 2020, 0, 0, 0) + tokens.TimedeltaValue(years=1),
                         tokens.DateTimeValue(28, 2, 2021, 0, 0, 0))

    def test_datetime_value_sub_timedelta_value_different_month_days_and_leap_year(self):
        self.assertEqual(tokens.DateTimeValue(29, 2, 2020, 0, 0, 0) - tokens.TimedeltaValue(years=1, months=1),
                         tokens.DateTimeValue(29, 1, 2019, 0, 0, 0))
        self.assertEqual(tokens.DateTimeValue(31, 3, 2020, 0, 0, 0) - tokens.TimedeltaValue(years=1, months=1),
                         tokens.DateTimeValue(28, 2, 2019, 0, 0, 0))

    def test_datetime_value_sub_date_value(self):
        self.assertEqual(tokens.DateTimeValue(29, 2, 2020, 0, 0, 0) - tokens.DateValue(28, 2, 2020),
                         tokens.TimedeltaValue(days=1))

    def test_datetime_value_sub_date_value_different_month_days(self):
        self.assertEqual(tokens.DateTimeValue(30, 6, 2020, 0, 0, 0) - tokens.DateValue(31, 5, 2020),
                         tokens.TimedeltaValue(months=1))

    def test_datetime_value_sub_date_value_leap_year(self):
        self.assertEqual(tokens.DateTimeValue(28, 2, 2021, 0, 0, 0) - tokens.DateValue(29, 2, 2020),
                         tokens.TimedeltaValue(years=1))

    def test_datetime_value_sub_date_value_different_month_days_and_leap_year(self):
        self.assertEqual(tokens.DateTimeValue(29, 3, 2021, 0, 0, 0) - tokens.DateValue(29, 2, 2020),
                         tokens.TimedeltaValue(years=1, months=1))
        self.assertEqual(tokens.DateTimeValue(28, 2, 2021, 0, 0, 0) - tokens.DateValue(31, 1, 2020),
                         tokens.TimedeltaValue(years=1, months=1))

    def test_datetime_value_sub_datetime_value(self):
        self.assertEqual(tokens.DateTimeValue(28, 2, 2021, 0, 0, 0) - tokens.DateTimeValue(27, 2, 2021, 23, 59, 59),
                         tokens.TimedeltaValue(seconds=1))

    def test_datetime_value_sub_datetime_value_different_month_days(self):
        self.assertEqual(tokens.DateTimeValue(30, 6, 2020, 0, 0, 0) - tokens.DateTimeValue(31, 5, 2020, 0, 0, 0),
                         tokens.TimedeltaValue(months=1))

    def test_datetime_value_sub_datetime_value_leap_year(self):
        self.assertEqual(tokens.DateTimeValue(28, 2, 2021, 0, 0, 0) - tokens.DateTimeValue(29, 2, 2020, 0, 0, 0),
                         tokens.TimedeltaValue(years=1))

    def test_datetime_value_sub_datetime_value_different_month_days_and_leap_year(self):
        self.assertEqual(tokens.DateTimeValue(29, 3, 2021, 0, 0, 0) - tokens.DateTimeValue(29, 2, 2020, 0, 0, 0),
                         tokens.TimedeltaValue(years=1, months=1))
        self.assertEqual(tokens.DateTimeValue(28, 2, 2021, 0, 0, 0) - tokens.DateTimeValue(31, 1, 2020, 0, 0, 0),
                         tokens.TimedeltaValue(years=1, months=1))

    def test_datetime_value_sub_timedelta_value_overflow(self):
        with self.assertRaises(OverflowError):
            val = tokens.DateTimeValue(1, 1, 1, 20, 37, 35) - tokens.TimedeltaValue(hours=21)

    def test_datetime_value_sub_time_value(self):
        self.assertEqual(tokens.DateTimeValue(1, 1, 1, 20, 37, 35) - tokens.TimeValue(19, 37, 35),
                         tokens.TimedeltaValue(hours=1))


class TimedeltaValueTestCase(unittest.TestCase):
    def test_timedelta_value_correctly_construct(self):
        v = tokens.TimedeltaValue(1, 2, 3, 4, 5, 6, 7)
        self.assertEqual(1, v.get_years())
        self.assertEqual(2, v.get_months())
        self.assertEqual(3, v.get_weeks())
        self.assertEqual(4, v.get_days())
        self.assertEqual(5, v.get_hours())
        self.assertEqual(6, v.get_minutes())
        self.assertEqual(7, v.get_seconds())

    def test_timedelta_value_equals_timedelta_value(self):
        self.assertTrue(tokens.TimedeltaValue(1, 2, 3, 4, 5, 6, 7) == tokens.TimedeltaValue(1, 2, 3, 4, 5, 6, 7))

    def test_timedelta_value_not_equals_timedelta_value(self):
        self.assertFalse(tokens.TimedeltaValue(1, 2, 3, 4, 5, 6, 7) == tokens.TimedeltaValue(1, 2, 3, 4, 5, 6, 8))

    def test_timedelta_value_equals_timedelta_value_with_different_representation(self):
        self.assertTrue(tokens.TimedeltaValue(weeks=1) == tokens.TimedeltaValue(days=7))

    def test_timedelta_value_months_not_equals_days(self):
        self.assertFalse(tokens.TimedeltaValue(months=1) == tokens.TimedeltaValue(days=28))
        self.assertFalse(tokens.TimedeltaValue(months=1) == tokens.TimedeltaValue(days=29))
        self.assertFalse(tokens.TimedeltaValue(months=1) == tokens.TimedeltaValue(days=30))
        self.assertFalse(tokens.TimedeltaValue(months=1) == tokens.TimedeltaValue(days=31))

    def test_timedelta_value_less_timedelta_value(self):
        self.assertTrue(tokens.TimedeltaValue(days=3, hours=5) < tokens.TimedeltaValue(days=4, hours=4))

    def test_timedelta_value_less_timedelta_value_with_different_representation(self):
        self.assertTrue(tokens.TimedeltaValue(weeks=1) < tokens.TimedeltaValue(days=8))

    def test_timedelta_value_months_not_less_peak_days(self):
        self.assertFalse(tokens.TimedeltaValue(months=1) < tokens.TimedeltaValue(days=28))
        self.assertFalse(tokens.TimedeltaValue(months=1) < tokens.TimedeltaValue(days=29))
        self.assertFalse(tokens.TimedeltaValue(months=1) < tokens.TimedeltaValue(days=30))
        self.assertFalse(tokens.TimedeltaValue(months=1) < tokens.TimedeltaValue(days=31))

    def test_timedelta_value_months_less_more_than_31_days(self):
        self.assertTrue(tokens.TimedeltaValue(months=1) < tokens.TimedeltaValue(days=32))

    def test_timedelta_value_less_negative(self):
        self.assertTrue(tokens.TimedeltaValue(months=0, days=20) < tokens.TimedeltaValue(months=1, weeks=-1))
        self.assertFalse(tokens.TimedeltaValue(months=0, days=27) < tokens.TimedeltaValue(months=1, weeks=-1))

    def test_timedelta_value_add_timedelta_value(self):
        self.assertTrue(
            tokens.TimedeltaValue(months=1) + tokens.TimedeltaValue(years=1) == tokens.TimedeltaValue(years=1,
                                                                                                      months=1))

    def test_timedelta_value_add_timedelta_value_negative(self):
        self.assertTrue(
            tokens.TimedeltaValue(months=1) + tokens.TimedeltaValue(years=-1) == tokens.TimedeltaValue(years=-1,
                                                                                                       months=1))

    def test_timedelta_value_sub_timedelta_value(self):
        self.assertTrue(
            tokens.TimedeltaValue(months=1) - tokens.TimedeltaValue(years=1) == tokens.TimedeltaValue(years=-1,
                                                                                                      months=1))

    def test_timedelta_value_sub_timedelta_value_negative(self):
        self.assertTrue(
            tokens.TimedeltaValue(months=1) - tokens.TimedeltaValue(years=-1) == tokens.TimedeltaValue(years=1,
                                                                                                       months=1))

    def test_timedelta_value_mul_timedelta_value(self):
        self.assertTrue(tokens.TimedeltaValue(months=1, days=5) * 2 == tokens.TimedeltaValue(months=2, days=10))

    def test_timedelta_value_mul_timedelta_value_negative(self):
        self.assertTrue(tokens.TimedeltaValue(months=1, days=5) * -2 == tokens.TimedeltaValue(months=-2, days=-10))

    def test_timedelta_value_div_timedelta_value(self):
        self.assertTrue(tokens.TimedeltaValue(months=2, days=10) // 2 == tokens.TimedeltaValue(months=1, days=5))

    def test_timedelta_value_div_timedelta_value_negative(self):
        self.assertTrue(tokens.TimedeltaValue(months=-2, days=-10) // -2 == tokens.TimedeltaValue(months=1, days=5))
