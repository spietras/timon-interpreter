import io
import unittest
import unittest.mock as mock

from timoninterpreter import error_handling
from timoninterpreter.lexical_analysis import Lexer
from timoninterpreter.source_readers import FileReader
from timoninterpreter.syntax_nodes import Program
from timoninterpreter.execution import Environment


class BaseExecutionTestCase(unittest.TestCase):
    def assert_return_value(self, expected_value):
        with FileReader("whatever") as fr:
            self.assertEquals(expected_value, Program(Lexer(fr)).execute(Environment()))

    def assert_raises(self, expected_error):
        with FileReader("whatever") as fr:
            self.assertRaises(expected_error, Program(Lexer(fr)).execute, Environment())


# noinspection PyUnusedLocal
class ExecutionReturnTestCase(BaseExecutionTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("return 5;"))
    def test_return_value(self, mock_open):
        self.assert_return_value(5)

    @mock.patch('builtins.open', return_value=io.StringIO("return;"))
    def test_return_no_value(self, mock_open):
        self.assert_return_value(0)


# noinspection PyUnusedLocal
class ExecutionVariablesTestCase(BaseExecutionTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("var a = 5;"
                                                          "return a;"))
    def test_variable_definition(self, mock_open):
        self.assert_return_value(5)

    @mock.patch('builtins.open', return_value=io.StringIO("var a;"
                                                          "a = 5;"
                                                          "return a;"))
    def test_variable_assignment(self, mock_open):
        self.assert_return_value(5)

    @mock.patch('builtins.open', return_value=io.StringIO("var a;"
                                                          "return a;"))
    def test_variable_without_value(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("a = 5;"
                                                          "return a;"))
    def test_variable_assign_undeclared(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)


# noinspection PyUnusedLocal
class ExecutionFunctionsTestCase(BaseExecutionTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("fun a(){ "
                                                          "    return 5; "
                                                          "}; "
                                                          "return a();"))
    def test_function(self, mock_open):
        self.assert_return_value(5)

    @mock.patch('builtins.open', return_value=io.StringIO("var a = 5;"
                                                          "fun b(c){ "
                                                          "    return c + 1; "
                                                          "}; "
                                                          "return b(a);"))
    def test_function_with_parameters(self, mock_open):
        self.assert_return_value(6)

    @mock.patch('builtins.open', return_value=io.StringIO("fun a(){};"
                                                          "return a();"))
    def test_function_no_return(self, mock_open):
        self.assert_return_value(0)

    @mock.patch('builtins.open', return_value=io.StringIO("fun a(){ "
                                                          "    if 1 {"
                                                          "        return 5;"
                                                          "    };"
                                                          "}; "
                                                          "return a();"))
    def test_function_nested_return(self, mock_open):
        self.assert_return_value(5)

    @mock.patch('builtins.open', return_value=io.StringIO("fun a(b){ "
                                                          "    return c + 1; "
                                                          "}; "
                                                          "return a(1);"))
    def test_function_access_undeclared_variable(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return a();"))
    def test_function_call_undeclared(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)


# noinspection PyUnusedLocal
class ExecutionIfTestCase(BaseExecutionTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("var a;"
                                                          "if 1 { a = 5; }"
                                                          "else { a = 6; };"
                                                          "return a;"))
    def test_if(self, mock_open):
        self.assert_return_value(5)

    @mock.patch('builtins.open', return_value=io.StringIO("var a;"
                                                          "if 0 { a = 5; }"
                                                          "else { a = 6; };"
                                                          "return a;"))
    def test_if_else(self, mock_open):
        self.assert_return_value(6)


# noinspection PyUnusedLocal
class ExecutionFromTestCase(BaseExecutionTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("var a = 0;"
                                                          "from 00:00:00 to 00:00:05 by seconds as d {"
                                                          "    a = a + 1;"
                                                          "};"
                                                          "return a;"))
    def test_from_condition(self, mock_open):
        self.assert_return_value(6)

    @mock.patch('builtins.open', return_value=io.StringIO("var a = 0;"
                                                          "from 00:00:00 to 00:00:02 by seconds as d {"
                                                          "    a = a + d.seconds;"
                                                          "};"
                                                          "return a;"))
    def test_from_variable(self, mock_open):
        self.assert_return_value(3)

    @mock.patch('builtins.open', return_value=io.StringIO("var a = 0;"
                                                          "from 00:00:00 to 00:00:10 by seconds as a {"
                                                          "    a = a + '1s';"
                                                          "};"
                                                          "return a;"))
    def test_from_shadows_variable(self, mock_open):
        self.assert_return_value(0)

    @mock.patch('builtins.open', return_value=io.StringIO("from 5 to 6 by seconds as d {};"))
    def test_from_bad_range_type(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("from 00:00:00 to 01.01.2000 by years as d {};"))
    def test_from_mixed_range_type(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)


# noinspection PyUnusedLocal
class ExecutionExpressionsTestCase(BaseExecutionTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("return 1 + 2 * 3;"))
    def test_expression1(self, mock_open):
        self.assert_return_value(7)

    @mock.patch('builtins.open', return_value=io.StringIO("return (1 + 2) * 3;"))
    def test_expression2(self, mock_open):
        self.assert_return_value(9)

    @mock.patch('builtins.open', return_value=io.StringIO("return (1 + 2) * 3 & 0;"))
    def test_expression3(self, mock_open):
        self.assert_return_value(0)

    @mock.patch('builtins.open', return_value=io.StringIO("return (1 < 2) * 5;"))
    def test_expression4(self, mock_open):
        self.assert_return_value(5)


# noinspection PyUnusedLocal
class ExecutionOperatorsTestCase(BaseExecutionTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("return 1 + 1;"))
    def test_plus(self, mock_open):
        self.assert_return_value(2)

    @mock.patch('builtins.open', return_value=io.StringIO("return 05:05:05 + 1;"))
    def test_plus_bad_types(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return 2 - 1;"))
    def test_minus(self, mock_open):
        self.assert_return_value(1)

    @mock.patch('builtins.open', return_value=io.StringIO("return 05:05:05 - 1;"))
    def test_minus_bad_types(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return 2 * 2;"))
    def test_multiply(self, mock_open):
        self.assert_return_value(4)

    @mock.patch('builtins.open', return_value=io.StringIO("return 05:05:05 * 01.01.2000;"))
    def test_multiply_bad_types(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return 4 / 2;"))
    def test_division(self, mock_open):
        self.assert_return_value(2)

    @mock.patch('builtins.open', return_value=io.StringIO("return 05:05:05 / 01.01.2000;"))
    def test_division_bad_types(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return 1 | 0;"))
    def test_or1(self, mock_open):
        self.assert_return_value(1)

    @mock.patch('builtins.open', return_value=io.StringIO("return 1 | 1;"))
    def test_or2(self, mock_open):
        self.assert_return_value(1)

    @mock.patch('builtins.open', return_value=io.StringIO("return 0 | 0;"))
    def test_or3(self, mock_open):
        self.assert_return_value(0)

    @mock.patch('builtins.open', return_value=io.StringIO("return 1 & 0;"))
    def test_and1(self, mock_open):
        self.assert_return_value(0)

    @mock.patch('builtins.open', return_value=io.StringIO("return 1 & 1;"))
    def test_and2(self, mock_open):
        self.assert_return_value(1)

    @mock.patch('builtins.open', return_value=io.StringIO("return 0 & 0;"))
    def test_and3(self, mock_open):
        self.assert_return_value(0)

    @mock.patch('builtins.open', return_value=io.StringIO("return 1 == 1;"))
    def test_equal(self, mock_open):
        self.assert_return_value(1)

    @mock.patch('builtins.open', return_value=io.StringIO("return 1 != 1;"))
    def test_not_equal(self, mock_open):
        self.assert_return_value(0)

    @mock.patch('builtins.open', return_value=io.StringIO("return 2 > 1;"))
    def test_greater(self, mock_open):
        self.assert_return_value(1)

    @mock.patch('builtins.open', return_value=io.StringIO("return 05:05:05 > 1;"))
    def test_greater_bad_types(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return 2 >= 1;"))
    def test_greater_equal(self, mock_open):
        self.assert_return_value(1)

    @mock.patch('builtins.open', return_value=io.StringIO("return 05:05:05 >= 1;"))
    def test_greater_equal_bad_types(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return 2 < 1;"))
    def test_less(self, mock_open):
        self.assert_return_value(0)

    @mock.patch('builtins.open', return_value=io.StringIO("return 05:05:05 < 1;"))
    def test_less_bad_types(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return 2 <= 1;"))
    def test_less_equal(self, mock_open):
        self.assert_return_value(0)

    @mock.patch('builtins.open', return_value=io.StringIO("return 05:05:05 <= 1;"))
    def test_less_equal_bad_types(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return -5;"))
    def test_math_negation(self, mock_open):
        self.assert_return_value(-5)

    @mock.patch('builtins.open', return_value=io.StringIO("return -05:05:05;"))
    def test_math_negation_bad_types(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return !1;"))
    def test_logic_negation(self, mock_open):
        self.assert_return_value(0)


# noinspection PyUnusedLocal
class ExecutionTimeAccessTestCase(BaseExecutionTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("return 01.02.2003.years;"))
    def test_years(self, mock_open):
        self.assert_return_value(2003)

    @mock.patch('builtins.open', return_value=io.StringIO("return 1.years;"))
    def test_years_bad_type(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return 01.02.2003.months;"))
    def test_months(self, mock_open):
        self.assert_return_value(2)

    @mock.patch('builtins.open', return_value=io.StringIO("return 1.months;"))
    def test_months_bad_type(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return '5W 5D'.weeks;"))
    def test_weeks(self, mock_open):
        self.assert_return_value(5)

    @mock.patch('builtins.open', return_value=io.StringIO("return 01.01.2000.weeks;"))
    def test_weeks_bad_type(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return 01.02.2003.days;"))
    def test_days(self, mock_open):
        self.assert_return_value(1)

    @mock.patch('builtins.open', return_value=io.StringIO("return 1.days;"))
    def test_days_bad_type(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return 01:02:03.hours;"))
    def test_hours(self, mock_open):
        self.assert_return_value(1)

    @mock.patch('builtins.open', return_value=io.StringIO("return 1.hours;"))
    def test_hours_bad_type(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return 01:02:03.minutes;"))
    def test_minutes(self, mock_open):
        self.assert_return_value(2)

    @mock.patch('builtins.open', return_value=io.StringIO("return 1.minutes;"))
    def test_minutes_bad_type(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)

    @mock.patch('builtins.open', return_value=io.StringIO("return 01:02:03.seconds;"))
    def test_seconds(self, mock_open):
        self.assert_return_value(3)

    @mock.patch('builtins.open', return_value=io.StringIO("return 1.seconds;"))
    def test_seconds_bad_type(self, mock_open):
        self.assert_raises(error_handling.ExecutionError)
