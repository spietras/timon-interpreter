import io
import unittest
import unittest.mock as mock

from timoninterpreter import error_handling
from timoninterpreter import syntax_nodes
from timoninterpreter import tokens
from timoninterpreter.lexical_analysis import Lexer
from timoninterpreter.source_readers import FileReader


class BaseParsingTestCase(unittest.TestCase):
    def assert_node(self, expected_type, expected_children_types):
        with FileReader("whatever") as fr:
            node = expected_type(Lexer(fr))
            children_types = [type(child) for child in node.get_children()]
            self.assertEqual(expected_children_types, children_types)
            return node


# noinspection PyUnusedLocal
class ParsingLeafNodeTestCase(BaseParsingTestCase):
    def assert_node(self, expected_type, token_type):
        node = super().assert_node(expected_type, [])
        self.assertEqual(token_type, node.token.get_type())
        return node

    @mock.patch('builtins.open', return_value=io.StringIO(";"))
    def test_semicolon(self, mock_open):
        self.assert_node(syntax_nodes.Semicolon, tokens.TokenType.SEMICOLON)

    @mock.patch('builtins.open', return_value=io.StringIO("fun"))
    def test_fun_keyword(self, mock_open):
        self.assert_node(syntax_nodes.FunKeyword, tokens.TokenType.FUN)

    @mock.patch('builtins.open', return_value=io.StringIO("var"))
    def test_var_keyword(self, mock_open):
        self.assert_node(syntax_nodes.VarKeyword, tokens.TokenType.VAR)

    @mock.patch('builtins.open', return_value=io.StringIO("if"))
    def test_if_keyword(self, mock_open):
        self.assert_node(syntax_nodes.IfKeyword, tokens.TokenType.IF)

    @mock.patch('builtins.open', return_value=io.StringIO("else"))
    def test_else_keyword(self, mock_open):
        self.assert_node(syntax_nodes.ElseKeyword, tokens.TokenType.ELSE)

    @mock.patch('builtins.open', return_value=io.StringIO("from"))
    def test_from_keyword(self, mock_open):
        self.assert_node(syntax_nodes.FromKeyword, tokens.TokenType.FROM)

    @mock.patch('builtins.open', return_value=io.StringIO("print"))
    def test_print_keyword(self, mock_open):
        self.assert_node(syntax_nodes.PrintKeyword, tokens.TokenType.PRINT)

    @mock.patch('builtins.open', return_value=io.StringIO("return"))
    def test_return_keyword(self, mock_open):
        self.assert_node(syntax_nodes.ReturnKeyword, tokens.TokenType.RETURN)

    @mock.patch('builtins.open', return_value=io.StringIO("to"))
    def test_to_keyword(self, mock_open):
        self.assert_node(syntax_nodes.ToKeyword, tokens.TokenType.TO)

    @mock.patch('builtins.open', return_value=io.StringIO("by"))
    def test_by_keyword(self, mock_open):
        self.assert_node(syntax_nodes.ByKeyword, tokens.TokenType.BY)

    @mock.patch('builtins.open', return_value=io.StringIO("as"))
    def test_as_keyword(self, mock_open):
        self.assert_node(syntax_nodes.AsKeyword, tokens.TokenType.AS)

    @mock.patch('builtins.open', return_value=io.StringIO("("))
    def test_left_parenthesis(self, mock_open):
        self.assert_node(syntax_nodes.LeftParenthesis, tokens.TokenType.LEFT_PARENTHESIS)

    @mock.patch('builtins.open', return_value=io.StringIO(")"))
    def test_right_parenthesis(self, mock_open):
        self.assert_node(syntax_nodes.RightParenthesis, tokens.TokenType.RIGHT_PARENTHESIS)

    @mock.patch('builtins.open', return_value=io.StringIO(","))
    def test_comma(self, mock_open):
        self.assert_node(syntax_nodes.Comma, tokens.TokenType.COMMA)

    @mock.patch('builtins.open', return_value=io.StringIO("{"))
    def test_left_bracket(self, mock_open):
        self.assert_node(syntax_nodes.LeftBracket, tokens.TokenType.LEFT_BRACKET)

    @mock.patch('builtins.open', return_value=io.StringIO("}"))
    def test_right_bracket(self, mock_open):
        self.assert_node(syntax_nodes.RightBracket, tokens.TokenType.RIGHT_BRACKET)

    @mock.patch('builtins.open', return_value=io.StringIO("="))
    def test_assign(self, mock_open):
        self.assert_node(syntax_nodes.Assign, tokens.TokenType.ASSIGN)

    @mock.patch('builtins.open', return_value=io.StringIO("."))
    def test_access(self, mock_open):
        self.assert_node(syntax_nodes.Access, tokens.TokenType.ACCESS)

    @mock.patch('builtins.open', return_value=io.StringIO("abc"))
    def test_identifier(self, mock_open):
        self.assert_node(syntax_nodes.Identifier, tokens.TokenType.IDENTIFIER)

    @mock.patch('builtins.open', return_value=io.StringIO("+"))
    def test_plus_operator(self, mock_open):
        self.assert_node(syntax_nodes.PlusOperator, tokens.TokenType.PLUS)

    @mock.patch('builtins.open', return_value=io.StringIO("-"))
    def test_minus_operator(self, mock_open):
        self.assert_node(syntax_nodes.MinusOperator, tokens.TokenType.MINUS)

    @mock.patch('builtins.open', return_value=io.StringIO("*"))
    def test_multiply_operator(self, mock_open):
        self.assert_node(syntax_nodes.MultiplyOperator, tokens.TokenType.MULTIPLICATION)

    @mock.patch('builtins.open', return_value=io.StringIO("/"))
    def test_division_operator(self, mock_open):
        self.assert_node(syntax_nodes.DivisionOperator, tokens.TokenType.DIVISION)

    @mock.patch('builtins.open', return_value=io.StringIO("|"))
    def test_or_operator(self, mock_open):
        self.assert_node(syntax_nodes.OrOperator, tokens.TokenType.LOGICAL_OR)

    @mock.patch('builtins.open', return_value=io.StringIO("&"))
    def test_and_operator(self, mock_open):
        self.assert_node(syntax_nodes.AndOperator, tokens.TokenType.LOGICAL_AND)

    @mock.patch('builtins.open', return_value=io.StringIO("=="))
    def test_equal_operator(self, mock_open):
        self.assert_node(syntax_nodes.EqualOperator, tokens.TokenType.EQUALS)

    @mock.patch('builtins.open', return_value=io.StringIO("!="))
    def test_notequal_operator(self, mock_open):
        self.assert_node(syntax_nodes.NotEqualOperator, tokens.TokenType.NOT_EQUALS)

    @mock.patch('builtins.open', return_value=io.StringIO(">"))
    def test_greater_operator(self, mock_open):
        self.assert_node(syntax_nodes.GreaterOperator, tokens.TokenType.GREATER)

    @mock.patch('builtins.open', return_value=io.StringIO(">="))
    def test_greater_or_equal_operator(self, mock_open):
        self.assert_node(syntax_nodes.GreaterOrEqualOperator, tokens.TokenType.GREATER_OR_EQUAL)

    @mock.patch('builtins.open', return_value=io.StringIO("<"))
    def test_less_operator(self, mock_open):
        self.assert_node(syntax_nodes.LessOperator, tokens.TokenType.LESS)

    @mock.patch('builtins.open', return_value=io.StringIO("<="))
    def test_less_or_equal_operator(self, mock_open):
        self.assert_node(syntax_nodes.LessOrEqualOperator, tokens.TokenType.LESS_OR_EQUAL)

    @mock.patch('builtins.open', return_value=io.StringIO("-"))
    def test_math_negation_operator(self, mock_open):
        self.assert_node(syntax_nodes.MathNegationOperator, tokens.TokenType.MINUS)

    @mock.patch('builtins.open', return_value=io.StringIO("!"))
    def test_logic_negation_operator(self, mock_open):
        self.assert_node(syntax_nodes.LogicNegationOperator, tokens.TokenType.NOT)

    @mock.patch('builtins.open', return_value=io.StringIO("years"))
    def test_years(self, mock_open):
        self.assert_node(syntax_nodes.Years, tokens.TokenType.YEARS)

    @mock.patch('builtins.open', return_value=io.StringIO("months"))
    def test_months(self, mock_open):
        self.assert_node(syntax_nodes.Months, tokens.TokenType.MONTHS)

    @mock.patch('builtins.open', return_value=io.StringIO("weeks"))
    def test_weeks(self, mock_open):
        self.assert_node(syntax_nodes.Weeks, tokens.TokenType.WEEKS)

    @mock.patch('builtins.open', return_value=io.StringIO("days"))
    def test_days(self, mock_open):
        self.assert_node(syntax_nodes.Days, tokens.TokenType.DAYS)

    @mock.patch('builtins.open', return_value=io.StringIO("hours"))
    def test_hours(self, mock_open):
        self.assert_node(syntax_nodes.Hours, tokens.TokenType.HOURS)

    @mock.patch('builtins.open', return_value=io.StringIO("minutes"))
    def test_minutes(self, mock_open):
        self.assert_node(syntax_nodes.Minutes, tokens.TokenType.MINUTES)

    @mock.patch('builtins.open', return_value=io.StringIO("seconds"))
    def test_seconds(self, mock_open):
        self.assert_node(syntax_nodes.Seconds, tokens.TokenType.SECONDS)

    @mock.patch('builtins.open', return_value=io.StringIO("123"))
    def test_number_literal(self, mock_open):
        self.assert_node(syntax_nodes.NumberLiteral, tokens.TokenType.NUMBER_LITERAL)

    @mock.patch('builtins.open', return_value=io.StringIO('"abc"'))
    def test_string_literal(self, mock_open):
        self.assert_node(syntax_nodes.StringLiteral, tokens.TokenType.STRING_LITERAL)

    @mock.patch('builtins.open', return_value=io.StringIO("01.01.2020"))
    def test_date_literal(self, mock_open):
        self.assert_node(syntax_nodes.DateLiteral, tokens.TokenType.DATE_LITERAL)

    @mock.patch('builtins.open', return_value=io.StringIO("20:00:00"))
    def test_time_literal(self, mock_open):
        self.assert_node(syntax_nodes.TimeLiteral, tokens.TokenType.TIME_LITERAL)

    @mock.patch('builtins.open', return_value=io.StringIO("01.01.2020~20:00:00"))
    def test_datetime_literal(self, mock_open):
        self.assert_node(syntax_nodes.DateTimeLiteral, tokens.TokenType.DATETIME_LITERAL)

    @mock.patch('builtins.open', return_value=io.StringIO("'1Y 5M'"))
    def test_timedelta_literal(self, mock_open):
        self.assert_node(syntax_nodes.TimedeltaLiteral, tokens.TokenType.TIMEDELTA_LITERAL)


# noinspection PyUnusedLocal
class ProgramNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO(""))
    def test_program_empty(self, mock_open):
        self.assert_node(syntax_nodes.Program, [])

    @mock.patch('builtins.open', return_value=io.StringIO("print 0;"))
    def test_program_single_statement(self, mock_open):
        self.assert_node(syntax_nodes.Program, [syntax_nodes.PrintStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("print 0; print 0; fun abc(){};"))
    def test_program_multiple_statements(self, mock_open):
        self.assert_node(syntax_nodes.Program, [syntax_nodes.PrintStatement,
                                                syntax_nodes.PrintStatement,
                                                syntax_nodes.FunctionDefinitionStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("bruh"))
    def test_program_bad_statement(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.Program, Lexer(fr))


# noinspection PyUnusedLocal
class VariableAssignmentStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a = 10;"))
    def test_variable_assignment_statement(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            node = syntax_nodes.VariableAssignmentStatement(lexer, syntax_nodes.Identifier(lexer))
            children_types = [type(child) for child in node.get_children()]
            self.assertEqual(children_types, [syntax_nodes.Identifier, syntax_nodes.NumberLiteral])

    @mock.patch('builtins.open', return_value=io.StringIO("a 10;"))
    def test_variable_assignment_statement_no_assign(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.VariableAssignmentStatement, lexer,
                              syntax_nodes.Identifier(lexer))

    @mock.patch('builtins.open', return_value=io.StringIO("a = fun;"))
    def test_variable_assignment_bad_expression(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.VariableAssignmentStatement, lexer,
                              syntax_nodes.Identifier(lexer))

    @mock.patch('builtins.open', return_value=io.StringIO("a != 10;"))
    def test_variable_assignment_bad_assign(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.VariableAssignmentStatement, lexer,
                              syntax_nodes.Identifier(lexer))


# noinspection PyUnusedLocal
class FunctionDefinitionStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("fun abc(a, b) { print 1; };"))
    def test_function_definition_statement(self, mock_open):
        self.assert_node(syntax_nodes.FunctionDefinitionStatement, [syntax_nodes.Identifier,
                                                                    syntax_nodes.ParametersDeclaration,
                                                                    syntax_nodes.Body])

    @mock.patch('builtins.open', return_value=io.StringIO("fun abc(a, b) {};"))
    def test_function_definition_statement_empty_body(self, mock_open):
        self.assert_node(syntax_nodes.FunctionDefinitionStatement, [syntax_nodes.Identifier,
                                                                    syntax_nodes.ParametersDeclaration,
                                                                    syntax_nodes.Body])

    @mock.patch('builtins.open', return_value=io.StringIO("fun abc() { print 1; };"))
    def test_function_definition_statement_empty_parameters(self, mock_open):
        self.assert_node(syntax_nodes.FunctionDefinitionStatement, [syntax_nodes.Identifier,
                                                                    syntax_nodes.ParametersDeclaration,
                                                                    syntax_nodes.Body])

    @mock.patch('builtins.open', return_value=io.StringIO("fun () {};"))
    def test_function_definition_statement_no_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FunctionDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("fun abc {};"))
    def test_function_definition_statement_no_parameters(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FunctionDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("fun abc();"))
    def test_function_definition_statement_no_body(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FunctionDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("var abc(a, b) { return 1; };"))
    def test_function_definition_statement_bad_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FunctionDefinitionStatement, Lexer(fr))


# noinspection PyUnusedLocal
class VariableDefinitionStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("var a = 10;"))
    def test_variable_definition_statement(self, mock_open):
        self.assert_node(syntax_nodes.VariableDefinitionStatement, [syntax_nodes.Identifier,
                                                                    syntax_nodes.VariableAssignmentStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("var a;"))
    def test_variable_definition_statement_no_assignment(self, mock_open):
        self.assert_node(syntax_nodes.VariableDefinitionStatement, [syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("var = 10;"))
    def test_variable_definition_statement_no_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.VariableDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("var;"))
    def test_variable_definition_statement_no_assignment_no_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.VariableDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("var var = 10;"))
    def test_variable_definition_statement_bad_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.VariableDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("var a = var;"))
    def test_variable_definition_statement_bad_value(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.VariableDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("var a = ;"))
    def test_variable_definition_statement_no_value(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.VariableDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("fun a = 10;"))
    def test_variable_definition_statement_bad_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.VariableDefinitionStatement, Lexer(fr))


# noinspection PyUnusedLocal
class IfStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("if a > b { print 1; } else { print 0; };"))
    def test_if_statement(self, mock_open):
        self.assert_node(syntax_nodes.IfStatement, [syntax_nodes.LogicRelationalExpression,
                                                    syntax_nodes.Body,
                                                    syntax_nodes.Body])

    @mock.patch('builtins.open', return_value=io.StringIO("if a > b { print 1; };"))
    def test_if_statement_no_else(self, mock_open):
        self.assert_node(syntax_nodes.IfStatement, [syntax_nodes.LogicRelationalExpression,
                                                    syntax_nodes.Body])

    @mock.patch('builtins.open', return_value=io.StringIO("if { print 1; } else { print 0; };"))
    def test_if_statement_no_condition(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.IfStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("if a > b else { print 0; };"))
    def test_if_statement_no_body(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.IfStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("if a > b { print 1; } else;"))
    def test_if_statement_no_else_body(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.IfStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("else a > b { print 1; } else { print 0; };"))
    def test_if_statement_bad_if_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.IfStatement, Lexer(fr))


# noinspection PyUnusedLocal
class FromStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("from a to b by days as c { print c; };"))
    def test_from_statement(self, mock_open):
        self.assert_node(syntax_nodes.FromStatement, [syntax_nodes.Identifier,
                                                      syntax_nodes.Identifier,
                                                      syntax_nodes.Days,
                                                      syntax_nodes.Identifier,
                                                      syntax_nodes.Body])

    @mock.patch('builtins.open', return_value=io.StringIO("from by days as c { print c; };"))
    def test_from_statement_no_range(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from a b by days as c { print c; };"))
    def test_from_statement_no_to_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from to to to by days as c { print c; };"))
    def test_from_statement_bad_range_expression(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from a return b by days as c { print c; };"))
    def test_from_statement_bad_range_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from a to b as c { print c; };"))
    def test_from_statement_no_step(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from a to b by as c { print c; };"))
    def test_from_statement_step_no_unit(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from a to b by bruh as c { print c; };"))
    def test_from_statement_step_bad_unit(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from a to b days as c { print c; };"))
    def test_from_statement_step_no_by_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from a to b return days as c { print c; };"))
    def test_from_statement_step_bad_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from a to b by days { print c; };"))
    def test_from_statement_no_iterator(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from a to by by days c { print c; };"))
    def test_from_statement_iterator_no_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from a to b by days as 10 { print c; };"))
    def test_from_statement_iterator_bad_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from a to b by days return c { print c; };"))
    def test_from_statement_iterator_bad_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from a to b by days as c;"))
    def test_from_statement_no_body(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("return a to b by days as c;"))
    def test_from_statement_bad_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FromStatement, Lexer(fr))


# noinspection PyUnusedLocal
class PrintStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("print 1;"))
    def test_print_statement(self, mock_open):
        self.assert_node(syntax_nodes.PrintStatement, [syntax_nodes.NumberLiteral])

    @mock.patch('builtins.open', return_value=io.StringIO("print;"))
    def test_print_statement_no_expression(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.PrintStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("print print;"))
    def test_print_statement_bad_expression(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.PrintStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("return 1;"))
    def test_print_statement_bad_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.PrintStatement, Lexer(fr))


# noinspection PyUnusedLocal
class ReturnStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("return 1;"))
    def test_return_statement(self, mock_open):
        self.assert_node(syntax_nodes.ReturnStatement, [syntax_nodes.NumberLiteral])

    @mock.patch('builtins.open', return_value=io.StringIO("return;"))
    def test_return_statement_empty(self, mock_open):
        self.assert_node(syntax_nodes.ReturnStatement, [])

    @mock.patch('builtins.open', return_value=io.StringIO("print 1;"))
    def test_return_statement_bad_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.ReturnStatement, Lexer(fr))


# noinspection PyUnusedLocal
class ParametersDeclarationNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("(a, b, c)"))
    def test_parameters_declaration(self, mock_open):
        self.assert_node(syntax_nodes.ParametersDeclaration, [syntax_nodes.Identifier,
                                                              syntax_nodes.Identifier,
                                                              syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("(a)"))
    def test_parameters_declaration_single_parameter(self, mock_open):
        self.assert_node(syntax_nodes.ParametersDeclaration, [syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("()"))
    def test_parameters_declaration_no_parameters(self, mock_open):
        self.assert_node(syntax_nodes.ParametersDeclaration, [])

    @mock.patch('builtins.open', return_value=io.StringIO("a, b, c)"))
    def test_parameters_declaration_no_left_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.ParametersDeclaration, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(a, b, c"))
    def test_parameters_declaration_no_right_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.ParametersDeclaration, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(a b c)"))
    def test_parameters_declaration_no_commas(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.ParametersDeclaration, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(a, 1+2, c)"))
    def test_parameters_declaration_bad_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.ParametersDeclaration, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("{a, 1+2, c}"))
    def test_parameters_declaration_bad_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.ParametersDeclaration, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(a, )"))
    def test_parameters_declaration_dangling_comma(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.ParametersDeclaration, Lexer(fr))


# noinspection PyUnusedLocal
class BodyNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("{ return; }"))
    def test_body(self, mock_open):
        self.assert_node(syntax_nodes.Body, [syntax_nodes.ReturnStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("{ print 1; print 2; }"))
    def test_body_multiple_statements(self, mock_open):
        self.assert_node(syntax_nodes.Body, [syntax_nodes.PrintStatement,
                                             syntax_nodes.PrintStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("{ }"))
    def test_body_empty(self, mock_open):
        self.assert_node(syntax_nodes.Body, [])

    @mock.patch('builtins.open', return_value=io.StringIO(" return; }"))
    def test_body_no_left_bracket(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.Body, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("{ fun abc() { return; }; }"))
    def test_body_non_nestable_statement(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.Body, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("{ return;"))
    def test_body_no_right_bracket(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.Body, Lexer(fr))


# noinspection PyUnusedLocal
class MathExpressionNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a + b"))
    def test_math_expression_plus(self, mock_open):
        self.assert_node(syntax_nodes.MathExpression, [syntax_nodes.Identifier,
                                                       syntax_nodes.PlusOperator,
                                                       syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a - b"))
    def test_math_expression_minus(self, mock_open):
        self.assert_node(syntax_nodes.MathExpression, [syntax_nodes.Identifier,
                                                       syntax_nodes.MinusOperator,
                                                       syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a - b + c - d"))
    def test_math_expression_multiple_operations(self, mock_open):
        self.assert_node(syntax_nodes.MathExpression, [syntax_nodes.Identifier,
                                                       syntax_nodes.MinusOperator,
                                                       syntax_nodes.Identifier,
                                                       syntax_nodes.PlusOperator,
                                                       syntax_nodes.Identifier,
                                                       syntax_nodes.MinusOperator,
                                                       syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_math_expression_no_operations(self, mock_open):
        self.assert_node(syntax_nodes.MathExpression, [syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a + b * c"))
    def test_math_expression_precedence(self, mock_open):
        self.assert_node(syntax_nodes.MathExpression, [syntax_nodes.Identifier,
                                                       syntax_nodes.PlusOperator,
                                                       syntax_nodes.MultiplicativeMathExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a +"))
    def test_math_expression_no_operand(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.MathExpression, Lexer(fr))


# noinspection PyUnusedLocal
class MultiplicativeMathExpressionNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a * b"))
    def test_math_expression_multiply(self, mock_open):
        self.assert_node(syntax_nodes.MultiplicativeMathExpression, [syntax_nodes.Identifier,
                                                                     syntax_nodes.MultiplyOperator,
                                                                     syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a / b"))
    def test_math_expression_divide(self, mock_open):
        self.assert_node(syntax_nodes.MultiplicativeMathExpression, [syntax_nodes.Identifier,
                                                                     syntax_nodes.DivisionOperator,
                                                                     syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a / b * c / d"))
    def test_math_expression_multiple_operations(self, mock_open):
        self.assert_node(syntax_nodes.MultiplicativeMathExpression, [syntax_nodes.Identifier,
                                                                     syntax_nodes.DivisionOperator,
                                                                     syntax_nodes.Identifier,
                                                                     syntax_nodes.MultiplyOperator,
                                                                     syntax_nodes.Identifier,
                                                                     syntax_nodes.DivisionOperator,
                                                                     syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_math_expression_no_operations(self, mock_open):
        self.assert_node(syntax_nodes.MultiplicativeMathExpression, [syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a *"))
    def test_math_expression_no_operand(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.MultiplicativeMathExpression, Lexer(fr))


# noinspection PyUnusedLocal
class MathTermNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_math_term_value(self, mock_open):
        self.assert_node(syntax_nodes.MathTerm, [syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("(a)"))
    def test_math_term_parenthesised_expression(self, mock_open):
        self.assert_node(syntax_nodes.MathTerm, [syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("-a"))
    def test_math_term_value_negation(self, mock_open):
        self.assert_node(syntax_nodes.MathTerm, [syntax_nodes.MathNegationOperator,
                                                 syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("-(a)"))
    def test_math_term_parenthesised_expression_negation(self, mock_open):
        self.assert_node(syntax_nodes.MathTerm, [syntax_nodes.MathNegationOperator,
                                                 syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("fun"))
    def test_math_term_bad_expression(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.MathTerm, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("-fun"))
    def test_math_term_bad_expression_negation(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.MathTerm, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("-"))
    def test_math_term_no_expression_negation(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.MathTerm, Lexer(fr))


# noinspection PyUnusedLocal
class ParenthesisedExpressionNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("(a + b)"))
    def test_parenthesised_expression(self, mock_open):
        self.assert_node(syntax_nodes.ParenthesisedExpression, [syntax_nodes.MathExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("(((a + b)))"))
    def test_parenthesised_expression_multiple_parenthesis(self, mock_open):
        self.assert_node(syntax_nodes.ParenthesisedExpression, [syntax_nodes.MathExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("()"))
    def test_parenthesised_expression_empty_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.ParenthesisedExpression, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(fun)"))
    def test_parenthesised_expression_bad_expression(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.ParenthesisedExpression, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("a)"))
    def test_parenthesised_expression_no_left_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.ParenthesisedExpression, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(a"))
    def test_parenthesised_expression_no_right_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.ParenthesisedExpression, Lexer(fr))


# noinspection PyUnusedLocal
class ExpressionNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a | b"))
    def test_expression(self, mock_open):
        self.assert_node(syntax_nodes.Expression, [syntax_nodes.Identifier,
                                                   syntax_nodes.OrOperator,
                                                   syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a | b | c | d"))
    def test_expression_multiple_operations(self, mock_open):
        self.assert_node(syntax_nodes.Expression, [syntax_nodes.Identifier,
                                                   syntax_nodes.OrOperator,
                                                   syntax_nodes.Identifier,
                                                   syntax_nodes.OrOperator,
                                                   syntax_nodes.Identifier,
                                                   syntax_nodes.OrOperator,
                                                   syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_expression_no_operations(self, mock_open):
        self.assert_node(syntax_nodes.Expression, [syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a | b & c"))
    def test_expression_precedence(self, mock_open):
        self.assert_node(syntax_nodes.Expression, [syntax_nodes.Identifier,
                                                   syntax_nodes.OrOperator,
                                                   syntax_nodes.LogicAndExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a |"))
    def test_expression_no_operand(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.Expression, Lexer(fr))


# noinspection PyUnusedLocal
class LogicAndExpressionNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a & b"))
    def test_logic_and_expression(self, mock_open):
        self.assert_node(syntax_nodes.LogicAndExpression, [syntax_nodes.Identifier,
                                                           syntax_nodes.AndOperator,
                                                           syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a & b & c & d"))
    def test_logic_and_expression_multiple_operations(self, mock_open):
        self.assert_node(syntax_nodes.LogicAndExpression, [syntax_nodes.Identifier,
                                                           syntax_nodes.AndOperator,
                                                           syntax_nodes.Identifier,
                                                           syntax_nodes.AndOperator,
                                                           syntax_nodes.Identifier,
                                                           syntax_nodes.AndOperator,
                                                           syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_logic_and_expression_no_operations(self, mock_open):
        self.assert_node(syntax_nodes.LogicAndExpression, [syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a &"))
    def test_logic_and_expression_no_operand(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.LogicAndExpression, Lexer(fr))


# noinspection PyUnusedLocal
class LogicEqualityExpressionNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a == b"))
    def test_logic_equality_expression(self, mock_open):
        self.assert_node(syntax_nodes.LogicEqualityExpression, [syntax_nodes.Identifier,
                                                                syntax_nodes.EqualOperator,
                                                                syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_logic_equality_expression_no_operations(self, mock_open):
        self.assert_node(syntax_nodes.LogicEqualityExpression, [syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a =="))
    def test_logic_equality_expression_no_operand(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.LogicEqualityExpression, Lexer(fr))


# noinspection PyUnusedLocal
class LogicRelationalExpressionNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a > b"))
    def test_logic_relational_expression(self, mock_open):
        self.assert_node(syntax_nodes.LogicRelationalExpression, [syntax_nodes.Identifier,
                                                                  syntax_nodes.GreaterOperator,
                                                                  syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_logic_relational_expression_no_operations(self, mock_open):
        self.assert_node(syntax_nodes.LogicRelationalExpression, [syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("a >"))
    def test_logic_relational_expression_no_operand(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.LogicRelationalExpression, Lexer(fr))


# noinspection PyUnusedLocal
class LogicTermNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_logic_term_value(self, mock_open):
        self.assert_node(syntax_nodes.LogicTerm, [syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("!a"))
    def test_logic_term_value_negation(self, mock_open):
        self.assert_node(syntax_nodes.LogicTerm, [syntax_nodes.LogicNegationOperator,
                                                  syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("fun"))
    def test_logic_term_bad_expression(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.LogicTerm, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("!fun"))
    def test_logic_term_bad_expression_negation(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.LogicTerm, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("!"))
    def test_logic_term_no_expression_negation(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.LogicTerm, Lexer(fr))


# noinspection PyUnusedLocal
class FunctionCallNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("abc(a)"))
    def test_function_call(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            node = syntax_nodes.FunctionCall(lexer, syntax_nodes.Identifier(lexer))
            children_types = [type(child) for child in node.get_children()]
            self.assertEqual(children_types, [syntax_nodes.Identifier, syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("abc"))
    def test_function_call_no_parameters(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FunctionCall, lexer,
                              syntax_nodes.Identifier(lexer))

    @mock.patch('builtins.open', return_value=io.StringIO("abc(a, 10, abc(15))"))
    def test_function_call_multiple_parameters(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            node = syntax_nodes.FunctionCall(lexer, syntax_nodes.Identifier(lexer))
            children_types = [type(child) for child in node.get_children()]
            self.assertEqual(children_types, [syntax_nodes.Identifier,
                                              syntax_nodes.Identifier,
                                              syntax_nodes.NumberLiteral,
                                              syntax_nodes.FunctionCall])

    @mock.patch('builtins.open', return_value=io.StringIO("abc(a)"))
    def test_function_call_single_parameter(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            node = syntax_nodes.FunctionCall(lexer, syntax_nodes.Identifier(lexer))
            children_types = [type(child) for child in node.get_children()]
            self.assertEqual(children_types, [syntax_nodes.Identifier, syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("abc()"))
    def test_function_call_empty_parameters(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            node = syntax_nodes.FunctionCall(lexer, syntax_nodes.Identifier(lexer))
            children_types = [type(child) for child in node.get_children()]
            self.assertEqual(children_types, [syntax_nodes.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("abc a, 10, abc(15))"))
    def test_function_call_no_left_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FunctionCall, lexer,
                              syntax_nodes.Identifier(lexer))

    @mock.patch('builtins.open', return_value=io.StringIO("abc(a, 10, abc(15)"))
    def test_function_call_no_right_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FunctionCall, lexer,
                              syntax_nodes.Identifier(lexer))

    @mock.patch('builtins.open', return_value=io.StringIO("abc(a 10 abc(15))"))
    def test_function_call_no_commas(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FunctionCall, lexer,
                              syntax_nodes.Identifier(lexer))

    @mock.patch('builtins.open', return_value=io.StringIO("abc(a, return, abc(15))"))
    def test_function_call_bad_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FunctionCall, lexer,
                              syntax_nodes.Identifier(lexer))

    @mock.patch('builtins.open', return_value=io.StringIO("abc{a, 10, abc(15)}"))
    def test_function_call_bad_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FunctionCall, lexer,
                              syntax_nodes.Identifier(lexer))

    @mock.patch('builtins.open', return_value=io.StringIO("abc(a, )"))
    def test_function_call_dangling_comma(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.FunctionCall, lexer,
                              syntax_nodes.Identifier(lexer))


# noinspection PyUnusedLocal
class TimeInfoAccessNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO(".days"))
    def test_time_info_access(self, mock_open):
        self.assert_node(syntax_nodes.TimeInfoAccess, [syntax_nodes.Days])

    @mock.patch('builtins.open', return_value=io.StringIO(" days"))
    def test_time_info_access_no_access(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.TimeInfoAccess, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("."))
    def test_time_info_access_no_unit(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.TimeInfoAccess, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO(",days"))
    def test_time_info_access_bad_access(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.TimeInfoAccess, Lexer(fr))


# noinspection PyUnusedLocal
class ParsingMiscellaneousTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a = 3 * (1 + 2);"))
    def test_math_with_parenthesis(self, mock_open):
        self.assert_node(syntax_nodes.Program, [syntax_nodes.VariableAssignmentStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("a = a > (1 + 2);"))
    def test_expression_with_logic_and_math(self, mock_open):
        self.assert_node(syntax_nodes.Program, [syntax_nodes.VariableAssignmentStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("a = a > (1 > 2);"))
    def test_expression_with_logic(self, mock_open):
        self.assert_node(syntax_nodes.Program, [syntax_nodes.VariableAssignmentStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("a = a + (1 > 2);"))
    def test_expression_with_math_and_logic(self, mock_open):
        self.assert_node(syntax_nodes.Program, [syntax_nodes.VariableAssignmentStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("a = (a + 0) & (1 + 2);"))
    def test_expression_with_logic_and_math_between_parenthesis(self, mock_open):
        self.assert_node(syntax_nodes.Program, [syntax_nodes.VariableAssignmentStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("a = (a > 0) & (1 > 2);"))
    def test_expression_with_logic_between_logic_parenthesis(self, mock_open):
        self.assert_node(syntax_nodes.Program, [syntax_nodes.VariableAssignmentStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("if a + b {};"))
    def test_if_with_math(self, mock_open):
        self.assert_node(syntax_nodes.Program, [syntax_nodes.IfStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("if a == b != c { return; };"))
    def test_multiple_equality_operations(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.Program, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("if a > b < c { return; };"))
    def test_multiple_relation_operations(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.Program, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("if a > b { print 1; } { print 1; };"))
    def test_no_else_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.Program, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("var a 10;"))
    def test_no_assign(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_nodes.Program, Lexer(fr))
