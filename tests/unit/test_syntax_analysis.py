import io
import unittest
import unittest.mock as mock

from timoninterpreter import error_handling
from timoninterpreter import syntax_analysis
from timoninterpreter import tokens
from timoninterpreter.lexical_analysis import Lexer
from timoninterpreter.source_readers import FileReader


class BaseParsingTestCase(unittest.TestCase):
    def assert_node(self, expected_type, expected_children_types):
        with FileReader("whatever") as fr:
            node = expected_type(Lexer(fr))
            children_types = [type(child) for child in node.children]
            self.assertEqual(children_types, expected_children_types)
            return node

    def assert_tree(self, expected_structure):
        with FileReader("whatever") as fr:
            node = expected_structure[0](Lexer(fr))
            self._asert_tree_node(node, expected_structure)

    def _asert_tree_node(self, node, expected_structure):
        self.assertIsInstance(node, expected_structure[0])
        if expected_structure[1] is None:
            return
        for i, expected_child in enumerate(expected_structure[1]):
            self._asert_tree_node(node.children[i], expected_child)


# noinspection PyUnusedLocal
class ParsingLeafNodeTestCase(BaseParsingTestCase):
    def assert_node(self, expected_type, token_type):
        node = super().assert_node(expected_type, [])
        self.assertEqual(node.token.type, token_type)
        return node

    @mock.patch('builtins.open', return_value=io.StringIO(";"))
    def test_semicolon(self, mock_open):
        self.assert_node(syntax_analysis.Semicolon, tokens.TokenType.SEMICOLON)

    @mock.patch('builtins.open', return_value=io.StringIO("fun"))
    def test_fun_keyword(self, mock_open):
        self.assert_node(syntax_analysis.FunKeyword, tokens.TokenType.FUN)

    @mock.patch('builtins.open', return_value=io.StringIO("var"))
    def test_var_keyword(self, mock_open):
        self.assert_node(syntax_analysis.VarKeyword, tokens.TokenType.VAR)

    @mock.patch('builtins.open', return_value=io.StringIO("if"))
    def test_if_keyword(self, mock_open):
        self.assert_node(syntax_analysis.IfKeyword, tokens.TokenType.IF)

    @mock.patch('builtins.open', return_value=io.StringIO("else"))
    def test_else_keyword(self, mock_open):
        self.assert_node(syntax_analysis.ElseKeyword, tokens.TokenType.ELSE)

    @mock.patch('builtins.open', return_value=io.StringIO("from"))
    def test_from_keyword(self, mock_open):
        self.assert_node(syntax_analysis.FromKeyword, tokens.TokenType.FROM)

    @mock.patch('builtins.open', return_value=io.StringIO("print"))
    def test_print_keyword(self, mock_open):
        self.assert_node(syntax_analysis.PrintKeyword, tokens.TokenType.PRINT)

    @mock.patch('builtins.open', return_value=io.StringIO("return"))
    def test_return_keyword(self, mock_open):
        self.assert_node(syntax_analysis.ReturnKeyword, tokens.TokenType.RETURN)

    @mock.patch('builtins.open', return_value=io.StringIO("to"))
    def test_to_keyword(self, mock_open):
        self.assert_node(syntax_analysis.ToKeyword, tokens.TokenType.TO)

    @mock.patch('builtins.open', return_value=io.StringIO("by"))
    def test_by_keyword(self, mock_open):
        self.assert_node(syntax_analysis.ByKeyword, tokens.TokenType.BY)

    @mock.patch('builtins.open', return_value=io.StringIO("as"))
    def test_as_keyword(self, mock_open):
        self.assert_node(syntax_analysis.AsKeyword, tokens.TokenType.AS)

    @mock.patch('builtins.open', return_value=io.StringIO("("))
    def test_left_parenthesis(self, mock_open):
        self.assert_node(syntax_analysis.LeftParenthesis, tokens.TokenType.LEFT_PARENTHESIS)

    @mock.patch('builtins.open', return_value=io.StringIO(")"))
    def test_right_parenthesis(self, mock_open):
        self.assert_node(syntax_analysis.RightParenthesis, tokens.TokenType.RIGHT_PARENTHESIS)

    @mock.patch('builtins.open', return_value=io.StringIO(","))
    def test_comma(self, mock_open):
        self.assert_node(syntax_analysis.Comma, tokens.TokenType.COMMA)

    @mock.patch('builtins.open', return_value=io.StringIO("{"))
    def test_left_bracket(self, mock_open):
        self.assert_node(syntax_analysis.LeftBracket, tokens.TokenType.LEFT_BRACKET)

    @mock.patch('builtins.open', return_value=io.StringIO("}"))
    def test_right_bracket(self, mock_open):
        self.assert_node(syntax_analysis.RightBracket, tokens.TokenType.RIGHT_BRACKET)

    @mock.patch('builtins.open', return_value=io.StringIO("="))
    def test_assign(self, mock_open):
        self.assert_node(syntax_analysis.Assign, tokens.TokenType.ASSIGN)

    @mock.patch('builtins.open', return_value=io.StringIO("."))
    def test_access(self, mock_open):
        self.assert_node(syntax_analysis.Access, tokens.TokenType.ACCESS)

    @mock.patch('builtins.open', return_value=io.StringIO("abc"))
    def test_identifier(self, mock_open):
        self.assert_node(syntax_analysis.Identifier, tokens.TokenType.IDENTIFIER)

    @mock.patch('builtins.open', return_value=io.StringIO("+"))
    def test_plus_operator(self, mock_open):
        self.assert_node(syntax_analysis.PlusOperator, tokens.TokenType.PLUS)

    @mock.patch('builtins.open', return_value=io.StringIO("-"))
    def test_minus_operator(self, mock_open):
        self.assert_node(syntax_analysis.MinusOperator, tokens.TokenType.MINUS)

    @mock.patch('builtins.open', return_value=io.StringIO("*"))
    def test_multiply_operator(self, mock_open):
        self.assert_node(syntax_analysis.MultiplyOperator, tokens.TokenType.MULTIPLICATION)

    @mock.patch('builtins.open', return_value=io.StringIO("/"))
    def test_division_operator(self, mock_open):
        self.assert_node(syntax_analysis.DivisionOperator, tokens.TokenType.DIVISION)

    @mock.patch('builtins.open', return_value=io.StringIO("|"))
    def test_or_operator(self, mock_open):
        self.assert_node(syntax_analysis.OrOperator, tokens.TokenType.LOGICAL_OR)

    @mock.patch('builtins.open', return_value=io.StringIO("&"))
    def test_and_operator(self, mock_open):
        self.assert_node(syntax_analysis.AndOperator, tokens.TokenType.LOGICAL_AND)

    @mock.patch('builtins.open', return_value=io.StringIO("=="))
    def test_equal_operator(self, mock_open):
        self.assert_node(syntax_analysis.EqualOperator, tokens.TokenType.EQUALS)

    @mock.patch('builtins.open', return_value=io.StringIO("!="))
    def test_notequal_operator(self, mock_open):
        self.assert_node(syntax_analysis.NotEqualOperator, tokens.TokenType.NOT_EQUALS)

    @mock.patch('builtins.open', return_value=io.StringIO(">"))
    def test_greater_operator(self, mock_open):
        self.assert_node(syntax_analysis.GreaterOperator, tokens.TokenType.GREATER)

    @mock.patch('builtins.open', return_value=io.StringIO(">="))
    def test_greater_or_equal_operator(self, mock_open):
        self.assert_node(syntax_analysis.GreaterOrEqualOperator, tokens.TokenType.GREATER_OR_EQUAL)

    @mock.patch('builtins.open', return_value=io.StringIO("<"))
    def test_less_operator(self, mock_open):
        self.assert_node(syntax_analysis.LessOperator, tokens.TokenType.LESS)

    @mock.patch('builtins.open', return_value=io.StringIO("<="))
    def test_less_or_equal_operator(self, mock_open):
        self.assert_node(syntax_analysis.LessOrEqualOperator, tokens.TokenType.LESS_OR_EQUAL)

    @mock.patch('builtins.open', return_value=io.StringIO("-"))
    def test_math_negation_operator(self, mock_open):
        self.assert_node(syntax_analysis.MathNegationOperator, tokens.TokenType.MINUS)

    @mock.patch('builtins.open', return_value=io.StringIO("!"))
    def test_logic_negation_operator(self, mock_open):
        self.assert_node(syntax_analysis.LogicNegationOperator, tokens.TokenType.NOT)

    @mock.patch('builtins.open', return_value=io.StringIO("years"))
    def test_years(self, mock_open):
        self.assert_node(syntax_analysis.Years, tokens.TokenType.YEARS)

    @mock.patch('builtins.open', return_value=io.StringIO("months"))
    def test_months(self, mock_open):
        self.assert_node(syntax_analysis.Months, tokens.TokenType.MONTHS)

    @mock.patch('builtins.open', return_value=io.StringIO("weeks"))
    def test_weeks(self, mock_open):
        self.assert_node(syntax_analysis.Weeks, tokens.TokenType.WEEKS)

    @mock.patch('builtins.open', return_value=io.StringIO("days"))
    def test_days(self, mock_open):
        self.assert_node(syntax_analysis.Days, tokens.TokenType.DAYS)

    @mock.patch('builtins.open', return_value=io.StringIO("hours"))
    def test_hours(self, mock_open):
        self.assert_node(syntax_analysis.Hours, tokens.TokenType.HOURS)

    @mock.patch('builtins.open', return_value=io.StringIO("minutes"))
    def test_minutes(self, mock_open):
        self.assert_node(syntax_analysis.Minutes, tokens.TokenType.MINUTES)

    @mock.patch('builtins.open', return_value=io.StringIO("seconds"))
    def test_seconds(self, mock_open):
        self.assert_node(syntax_analysis.Seconds, tokens.TokenType.SECONDS)

    @mock.patch('builtins.open', return_value=io.StringIO("123"))
    def test_number_literal(self, mock_open):
        self.assert_node(syntax_analysis.NumberLiteral, tokens.TokenType.NUMBER_LITERAL)

    @mock.patch('builtins.open', return_value=io.StringIO('"abc"'))
    def test_string_literal(self, mock_open):
        self.assert_node(syntax_analysis.StringLiteral, tokens.TokenType.STRING_LITERAL)

    @mock.patch('builtins.open', return_value=io.StringIO("01.01.2020"))
    def test_date_literal(self, mock_open):
        self.assert_node(syntax_analysis.DateLiteral, tokens.TokenType.DATE_LITERAL)

    @mock.patch('builtins.open', return_value=io.StringIO("20:00:00"))
    def test_time_literal(self, mock_open):
        self.assert_node(syntax_analysis.TimeLiteral, tokens.TokenType.TIME_LITERAL)

    @mock.patch('builtins.open', return_value=io.StringIO("01.01.2020~20:00:00"))
    def test_datetime_literal(self, mock_open):
        self.assert_node(syntax_analysis.DateTimeLiteral, tokens.TokenType.DATETIME_LITERAL)

    @mock.patch('builtins.open', return_value=io.StringIO("'1Y 5M'"))
    def test_timedelta_literal(self, mock_open):
        self.assert_node(syntax_analysis.TimedeltaLiteral, tokens.TokenType.TIMEDELTA_LITERAL)


# noinspection PyUnusedLocal
class ProgramNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO(""))
    def test_program_empty(self, mock_open):
        self.assert_node(syntax_analysis.Program, [])

    @mock.patch('builtins.open', return_value=io.StringIO("print 0;"))
    def test_program_single_statement(self, mock_open):
        self.assert_node(syntax_analysis.Program, [syntax_analysis.NestableStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("print 0; print 0; fun abc(){};"))
    def test_program_multiple_statements(self, mock_open):
        self.assert_node(syntax_analysis.Program, [syntax_analysis.NestableStatement,
                                                   syntax_analysis.NestableStatement,
                                                   syntax_analysis.NonNestableStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("bruh"))
    def test_program_bad_statement(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.Program, Lexer(fr))


# noinspection PyUnusedLocal
class NonNestableStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("fun abc(){};"))
    def test_non_nestable_statement_function_definition(self, mock_open):
        self.assert_node(syntax_analysis.NonNestableStatement, [syntax_analysis.FunctionDefinitionStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("fun abc(){}"))
    def test_non_nestable_statement_no_semicolon(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.NonNestableStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("var a = 10;"))
    def test_non_nestable_statement_bad_statement(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.NonNestableStatement, Lexer(fr))


# noinspection PyUnusedLocal
class NestableStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("abc();"))
    def test_nestable_statement_identifier_first_statement(self, mock_open):
        self.assert_node(syntax_analysis.NestableStatement, [syntax_analysis.IdentifierFirstStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("var a;"))
    def test_nestable_statement_variable_definition_statement(self, mock_open):
        self.assert_node(syntax_analysis.NestableStatement, [syntax_analysis.VariableDefinitionStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("if a > b {};"))
    def test_nestable_statement_if_statement(self, mock_open):
        self.assert_node(syntax_analysis.NestableStatement, [syntax_analysis.IfStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("from a to b by days as c {};"))
    def test_nestable_statement_from_statement(self, mock_open):
        self.assert_node(syntax_analysis.NestableStatement, [syntax_analysis.FromStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("print 1;"))
    def test_nestable_statement_print_statement(self, mock_open):
        self.assert_node(syntax_analysis.NestableStatement, [syntax_analysis.PrintStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("return 1;"))
    def test_nestable_statement_return_statement(self, mock_open):
        self.assert_node(syntax_analysis.NestableStatement, [syntax_analysis.ReturnStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("print 1"))
    def test_nestable_statement_no_semicolon(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.NestableStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("fun abc() {};"))
    def test_nestable_statement_bad_statement(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.NestableStatement, Lexer(fr))


# noinspection PyUnusedLocal
class IdentifierFirstStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("abc()"))
    def test_identifier_first_statement_function_call(self, mock_open):
        self.assert_node(syntax_analysis.IdentifierFirstStatement, [syntax_analysis.FunctionCall])

    @mock.patch('builtins.open', return_value=io.StringIO("a = 10"))
    def test_identifier_first_statement_variable_assignment_statement(self, mock_open):
        self.assert_node(syntax_analysis.IdentifierFirstStatement, [syntax_analysis.VariableAssignmentStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("()"))
    def test_identifier_first_statement_no_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.IdentifierFirstStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("abc)"))
    def test_identifier_first_statement_bad_statement(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.IdentifierFirstStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("abc{}"))
    def test_identifier_first_statement_bad_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.IdentifierFirstStatement, Lexer(fr))


# noinspection PyUnusedLocal
class VariableAssignmentStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a = 10"))
    def test_variable_assignment_statement(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            node = syntax_analysis.VariableAssignmentStatement(lexer, syntax_analysis.Identifier(lexer))
            children_types = [type(child) for child in node.children]
            self.assertEqual(children_types, [syntax_analysis.Identifier, syntax_analysis.Expression])

    @mock.patch('builtins.open', return_value=io.StringIO("a 10"))
    def test_variable_assignment_statement_no_assign(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.VariableAssignmentStatement, lexer,
                              syntax_analysis.Identifier(lexer))

    @mock.patch('builtins.open', return_value=io.StringIO("a = fun"))
    def test_variable_assignment_bad_expression(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.VariableAssignmentStatement, lexer,
                              syntax_analysis.Identifier(lexer))

    @mock.patch('builtins.open', return_value=io.StringIO("a != 10"))
    def test_variable_assignment_bad_assign(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.VariableAssignmentStatement, lexer,
                              syntax_analysis.Identifier(lexer))


# noinspection PyUnusedLocal
class FunctionDefinitionStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("fun abc(a, b) { print 1; }"))
    def test_function_definition_statement(self, mock_open):
        self.assert_node(syntax_analysis.FunctionDefinitionStatement, [syntax_analysis.Identifier,
                                                                       syntax_analysis.ParametersDeclaration,
                                                                       syntax_analysis.Body])

    @mock.patch('builtins.open', return_value=io.StringIO("fun abc(a, b) {}"))
    def test_function_definition_statement_empty_body(self, mock_open):
        self.assert_node(syntax_analysis.FunctionDefinitionStatement, [syntax_analysis.Identifier,
                                                                       syntax_analysis.ParametersDeclaration,
                                                                       syntax_analysis.Body])

    @mock.patch('builtins.open', return_value=io.StringIO("fun abc() { print 1; }"))
    def test_function_definition_statement_empty_parameters(self, mock_open):
        self.assert_node(syntax_analysis.FunctionDefinitionStatement, [syntax_analysis.Identifier,
                                                                       syntax_analysis.ParametersDeclaration,
                                                                       syntax_analysis.Body])

    @mock.patch('builtins.open', return_value=io.StringIO("fun () {}"))
    def test_function_definition_statement_no_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FunctionDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("fun abc {}"))
    def test_function_definition_statement_no_parameters(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FunctionDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("fun abc()"))
    def test_function_definition_statement_no_body(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FunctionDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("var abc(a, b) { return 1; }"))
    def test_function_definition_statement_bad_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FunctionDefinitionStatement, Lexer(fr))


# noinspection PyUnusedLocal
class VariableDefinitionStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("var a = 10"))
    def test_variable_definition_statement(self, mock_open):
        self.assert_node(syntax_analysis.VariableDefinitionStatement, [syntax_analysis.Identifier,
                                                                       syntax_analysis.VariableAssignmentStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("var a"))
    def test_variable_definition_statement_no_assignment(self, mock_open):
        self.assert_node(syntax_analysis.VariableDefinitionStatement, [syntax_analysis.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("var = 10"))
    def test_variable_definition_statement_no_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.VariableDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("var"))
    def test_variable_definition_statement_no_assignment_no_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.VariableDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("var var = 10"))
    def test_variable_definition_statement_bad_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.VariableDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("var a = var"))
    def test_variable_definition_statement_bad_value(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.VariableDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("var a = "))
    def test_variable_definition_statement_no_value(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.VariableDefinitionStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("fun a = 10"))
    def test_variable_definition_statement_bad_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.VariableDefinitionStatement, Lexer(fr))


# noinspection PyUnusedLocal
class IfStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("if a > b { print 1; } else { print 0; }"))
    def test_if_statement(self, mock_open):
        self.assert_node(syntax_analysis.IfStatement, [syntax_analysis.Expression,
                                                       syntax_analysis.Body,
                                                       syntax_analysis.Body])

    @mock.patch('builtins.open', return_value=io.StringIO("if a > b { print 1; }"))
    def test_if_statement_no_else(self, mock_open):
        self.assert_node(syntax_analysis.IfStatement, [syntax_analysis.Expression,
                                                       syntax_analysis.Body])

    @mock.patch('builtins.open', return_value=io.StringIO("if { print 1; } else { print 0; }"))
    def test_if_statement_no_condition(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.IfStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("if a > b else { print 0; }"))
    def test_if_statement_no_body(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.IfStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("if a > b { print 1; } else"))
    def test_if_statement_no_else_body(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.IfStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("else a > b { print 1; } else { print 0; }"))
    def test_if_statement_bad_if_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.IfStatement, Lexer(fr))


# noinspection PyUnusedLocal
class FromStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("from a to b by days as c { print c; }"))
    def test_from_statement(self, mock_open):
        self.assert_node(syntax_analysis.FromStatement, [syntax_analysis.FromRange,
                                                         syntax_analysis.FromStep,
                                                         syntax_analysis.FromIterator,
                                                         syntax_analysis.Body])

    @mock.patch('builtins.open', return_value=io.StringIO("from by days as c { print c; }"))
    def test_from_statement_no_range(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from a to b as c { print c; }"))
    def test_from_statement_no_step(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from a to b by days { print c; }"))
    def test_from_statement_no_iterator(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("from a to b by days as c"))
    def test_from_statement_no_body(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FromStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("return a to b by days as c"))
    def test_from_statement_bad_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FromStatement, Lexer(fr))


# noinspection PyUnusedLocal
class PrintStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("print 1"))
    def test_print_statement(self, mock_open):
        self.assert_node(syntax_analysis.PrintStatement, [syntax_analysis.Expression])

    @mock.patch('builtins.open', return_value=io.StringIO("print"))
    def test_print_statement_no_expression(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.PrintStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("print print"))
    def test_print_statement_bad_expression(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.PrintStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("return 1"))
    def test_print_statement_bad_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.PrintStatement, Lexer(fr))


# noinspection PyUnusedLocal
class ReturnStatementNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("return 1"))
    def test_return_statement(self, mock_open):
        self.assert_node(syntax_analysis.ReturnStatement, [syntax_analysis.Expression])

    @mock.patch('builtins.open', return_value=io.StringIO("return"))
    def test_return_statement_empty(self, mock_open):
        self.assert_node(syntax_analysis.ReturnStatement, [])

    @mock.patch('builtins.open', return_value=io.StringIO("print 1"))
    def test_return_statement_bad_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ReturnStatement, Lexer(fr))


# noinspection PyUnusedLocal
class ParametersDeclarationNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("(a, b, c)"))
    def test_parameters_declaration(self, mock_open):
        self.assert_node(syntax_analysis.ParametersDeclaration, [syntax_analysis.Identifier,
                                                                 syntax_analysis.Identifier,
                                                                 syntax_analysis.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("(a)"))
    def test_parameters_declaration_single_parameter(self, mock_open):
        self.assert_node(syntax_analysis.ParametersDeclaration, [syntax_analysis.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("()"))
    def test_parameters_declaration_no_parameters(self, mock_open):
        self.assert_node(syntax_analysis.ParametersDeclaration, [])

    @mock.patch('builtins.open', return_value=io.StringIO("a, b, c)"))
    def test_parameters_declaration_no_left_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParametersDeclaration, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(a, b, c"))
    def test_parameters_declaration_no_right_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParametersDeclaration, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(a b c)"))
    def test_parameters_declaration_no_commas(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParametersDeclaration, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(a, 1+2, c)"))
    def test_parameters_declaration_bad_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParametersDeclaration, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("{a, 1+2, c}"))
    def test_parameters_declaration_bad_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParametersDeclaration, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(a, )"))
    def test_parameters_declaration_dangling_comma(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParametersDeclaration, Lexer(fr))


# noinspection PyUnusedLocal
class BodyNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("{ return; }"))
    def test_body(self, mock_open):
        self.assert_node(syntax_analysis.Body, [syntax_analysis.NestableStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("{ print 1; print 2; }"))
    def test_body_multiple_statements(self, mock_open):
        self.assert_node(syntax_analysis.Body, [syntax_analysis.NestableStatement,
                                                syntax_analysis.NestableStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("{ }"))
    def test_body_empty(self, mock_open):
        self.assert_node(syntax_analysis.Body, [])

    @mock.patch('builtins.open', return_value=io.StringIO(" return; }"))
    def test_body_no_left_bracket(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.Body, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("{ fun abc() { return; }; }"))
    def test_body_non_nestable_statement(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.Body, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("{ return;"))
    def test_body_no_right_bracket(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.Body, Lexer(fr))


# noinspection PyUnusedLocal
class FromRangeNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a to b"))
    def test_from_range(self, mock_open):
        self.assert_node(syntax_analysis.FromRange, [syntax_analysis.Expression,
                                                     syntax_analysis.Expression])

    @mock.patch('builtins.open', return_value=io.StringIO("a b"))
    def test_return_statement_no_to_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ReturnStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("to to to"))
    def test_return_statement_bad_expression(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ReturnStatement, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("a return b"))
    def test_return_statement_bad_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ReturnStatement, Lexer(fr))


# noinspection PyUnusedLocal
class FromStepNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("by days"))
    def test_from_step(self, mock_open):
        self.assert_node(syntax_analysis.FromStep, [syntax_analysis.TimeUnit])

    @mock.patch('builtins.open', return_value=io.StringIO("by"))
    def test_from_step_no_unit(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FromStep, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("by bruh"))
    def test_from_step_bad_unit(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FromStep, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("days"))
    def test_from_step_no_by_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FromStep, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("return days"))
    def test_from_step_bad_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FromStep, Lexer(fr))


# noinspection PyUnusedLocal
class FromIteratorNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("as c"))
    def test_from_iterator(self, mock_open):
        self.assert_node(syntax_analysis.FromIterator, [syntax_analysis.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("c"))
    def test_from_iterator_no_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FromIterator, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("as 10"))
    def test_from_iterator_bad_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FromIterator, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("return c"))
    def test_from_iterator_bad_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FromIterator, Lexer(fr))


# noinspection PyUnusedLocal
class MathExpressionNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a + b"))
    def test_math_expression_plus(self, mock_open):
        self.assert_node(syntax_analysis.MathExpression, [syntax_analysis.MultiplicativeMathExpression,
                                                          syntax_analysis.AdditiveOperator,
                                                          syntax_analysis.MultiplicativeMathExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a - b"))
    def test_math_expression_minus(self, mock_open):
        self.assert_node(syntax_analysis.MathExpression, [syntax_analysis.MultiplicativeMathExpression,
                                                          syntax_analysis.AdditiveOperator,
                                                          syntax_analysis.MultiplicativeMathExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a - b + c - d"))
    def test_math_expression_multiple_operations(self, mock_open):
        self.assert_node(syntax_analysis.MathExpression, [syntax_analysis.MultiplicativeMathExpression,
                                                          syntax_analysis.AdditiveOperator,
                                                          syntax_analysis.MultiplicativeMathExpression,
                                                          syntax_analysis.AdditiveOperator,
                                                          syntax_analysis.MultiplicativeMathExpression,
                                                          syntax_analysis.AdditiveOperator,
                                                          syntax_analysis.MultiplicativeMathExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_math_expression_no_operations(self, mock_open):
        self.assert_node(syntax_analysis.MathExpression, [syntax_analysis.MultiplicativeMathExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a + b * c"))
    def test_math_expression_precedence(self, mock_open):
        self.assert_node(syntax_analysis.MathExpression, [syntax_analysis.MultiplicativeMathExpression,
                                                          syntax_analysis.AdditiveOperator,
                                                          syntax_analysis.MultiplicativeMathExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a +"))
    def test_math_expression_no_operand(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.MathExpression, Lexer(fr))


# noinspection PyUnusedLocal
class MultiplicativeMathExpressionNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a * b"))
    def test_math_expression_multiply(self, mock_open):
        self.assert_node(syntax_analysis.MultiplicativeMathExpression, [syntax_analysis.MathTerm,
                                                                        syntax_analysis.MultiplicativeOperator,
                                                                        syntax_analysis.MathTerm])

    @mock.patch('builtins.open', return_value=io.StringIO("a / b"))
    def test_math_expression_divide(self, mock_open):
        self.assert_node(syntax_analysis.MultiplicativeMathExpression, [syntax_analysis.MathTerm,
                                                                        syntax_analysis.MultiplicativeOperator,
                                                                        syntax_analysis.MathTerm])

    @mock.patch('builtins.open', return_value=io.StringIO("a / b * c / d"))
    def test_math_expression_multiple_operations(self, mock_open):
        self.assert_node(syntax_analysis.MultiplicativeMathExpression, [syntax_analysis.MathTerm,
                                                                        syntax_analysis.MultiplicativeOperator,
                                                                        syntax_analysis.MathTerm,
                                                                        syntax_analysis.MultiplicativeOperator,
                                                                        syntax_analysis.MathTerm,
                                                                        syntax_analysis.MultiplicativeOperator,
                                                                        syntax_analysis.MathTerm])

    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_math_expression_no_operations(self, mock_open):
        self.assert_node(syntax_analysis.MultiplicativeMathExpression, [syntax_analysis.MathTerm])

    @mock.patch('builtins.open', return_value=io.StringIO("a *"))
    def test_math_expression_no_operand(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.MultiplicativeMathExpression, Lexer(fr))


# noinspection PyUnusedLocal
class MathTermNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_math_term_value(self, mock_open):
        self.assert_node(syntax_analysis.MathTerm, [syntax_analysis.Value])

    @mock.patch('builtins.open', return_value=io.StringIO("(a)"))
    def test_math_term_parenthesised_expression(self, mock_open):
        self.assert_node(syntax_analysis.MathTerm, [syntax_analysis.ParenthesisedExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("-a"))
    def test_math_term_value_negation(self, mock_open):
        self.assert_node(syntax_analysis.MathTerm, [syntax_analysis.MathNegationOperator,
                                                    syntax_analysis.Value])

    @mock.patch('builtins.open', return_value=io.StringIO("-(a)"))
    def test_math_term_parenthesised_expression_negation(self, mock_open):
        self.assert_node(syntax_analysis.MathTerm, [syntax_analysis.MathNegationOperator,
                                                    syntax_analysis.ParenthesisedExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("fun"))
    def test_math_term_bad_expression(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.MathTerm, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("-fun"))
    def test_math_term_bad_expression_negation(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.MathTerm, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("-"))
    def test_math_term_no_expression_negation(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.MathTerm, Lexer(fr))


# noinspection PyUnusedLocal
class ParenthesisedExpressionNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("(a + b)"))
    def test_parenthesised_expression(self, mock_open):
        self.assert_node(syntax_analysis.ParenthesisedExpression, [syntax_analysis.Expression])

    @mock.patch('builtins.open', return_value=io.StringIO("(((a + b)))"))
    def test_parenthesised_expression_multiple_parenthesis(self, mock_open):
        self.assert_node(syntax_analysis.ParenthesisedExpression, [syntax_analysis.Expression])

    @mock.patch('builtins.open', return_value=io.StringIO("()"))
    def test_parenthesised_expression_empty_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParenthesisedExpression, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(fun)"))
    def test_parenthesised_expression_bad_expression(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParenthesisedExpression, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("a)"))
    def test_parenthesised_expression_no_left_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParenthesisedExpression, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(a"))
    def test_parenthesised_expression_no_right_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParenthesisedExpression, Lexer(fr))


# noinspection PyUnusedLocal
class ExpressionNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a | b"))
    def test_expression(self, mock_open):
        self.assert_node(syntax_analysis.Expression, [syntax_analysis.LogicAndExpression,
                                                      syntax_analysis.OrOperator,
                                                      syntax_analysis.LogicAndExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a | b | c | d"))
    def test_expression_multiple_operations(self, mock_open):
        self.assert_node(syntax_analysis.Expression, [syntax_analysis.LogicAndExpression,
                                                      syntax_analysis.OrOperator,
                                                      syntax_analysis.LogicAndExpression,
                                                      syntax_analysis.OrOperator,
                                                      syntax_analysis.LogicAndExpression,
                                                      syntax_analysis.OrOperator,
                                                      syntax_analysis.LogicAndExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_expression_no_operations(self, mock_open):
        self.assert_node(syntax_analysis.Expression, [syntax_analysis.LogicAndExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a | b & c"))
    def test_expression_precedence(self, mock_open):
        self.assert_node(syntax_analysis.Expression, [syntax_analysis.LogicAndExpression,
                                                      syntax_analysis.OrOperator,
                                                      syntax_analysis.LogicAndExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a |"))
    def test_expression_no_operand(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.Expression, Lexer(fr))


# noinspection PyUnusedLocal
class LogicAndExpressionNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a & b"))
    def test_logic_and_expression(self, mock_open):
        self.assert_node(syntax_analysis.LogicAndExpression, [syntax_analysis.LogicEqualityExpression,
                                                              syntax_analysis.AndOperator,
                                                              syntax_analysis.LogicEqualityExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a & b & c & d"))
    def test_logic_and_expression_multiple_operations(self, mock_open):
        self.assert_node(syntax_analysis.LogicAndExpression, [syntax_analysis.LogicEqualityExpression,
                                                              syntax_analysis.AndOperator,
                                                              syntax_analysis.LogicEqualityExpression,
                                                              syntax_analysis.AndOperator,
                                                              syntax_analysis.LogicEqualityExpression,
                                                              syntax_analysis.AndOperator,
                                                              syntax_analysis.LogicEqualityExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_logic_and_expression_no_operations(self, mock_open):
        self.assert_node(syntax_analysis.LogicAndExpression, [syntax_analysis.LogicEqualityExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a &"))
    def test_logic_and_expression_no_operand(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.LogicAndExpression, Lexer(fr))


# noinspection PyUnusedLocal
class LogicEqualityExpressionNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a == b"))
    def test_logic_equality_expression(self, mock_open):
        self.assert_node(syntax_analysis.LogicEqualityExpression, [syntax_analysis.LogicRelationalExpression,
                                                                   syntax_analysis.EqualityOperator,
                                                                   syntax_analysis.LogicRelationalExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_logic_equality_expression_no_operations(self, mock_open):
        self.assert_node(syntax_analysis.LogicEqualityExpression, [syntax_analysis.LogicRelationalExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("a =="))
    def test_logic_equality_expression_no_operand(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.LogicEqualityExpression, Lexer(fr))


# noinspection PyUnusedLocal
class LogicRelationalExpressionNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a > b"))
    def test_logic_relational_expression(self, mock_open):
        self.assert_node(syntax_analysis.LogicRelationalExpression, [syntax_analysis.LogicTerm,
                                                                     syntax_analysis.RelationOperator,
                                                                     syntax_analysis.LogicTerm])

    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_logic_relational_expression_no_operations(self, mock_open):
        self.assert_node(syntax_analysis.LogicRelationalExpression, [syntax_analysis.LogicTerm])

    @mock.patch('builtins.open', return_value=io.StringIO("a >"))
    def test_logic_relational_expression_no_operand(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.LogicRelationalExpression, Lexer(fr))


# noinspection PyUnusedLocal
class LogicTermNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_logic_term_value(self, mock_open):
        self.assert_node(syntax_analysis.LogicTerm, [syntax_analysis.MathExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("!a"))
    def test_logic_term_value_negation(self, mock_open):
        self.assert_node(syntax_analysis.LogicTerm, [syntax_analysis.LogicNegationOperator,
                                                     syntax_analysis.MathExpression])

    @mock.patch('builtins.open', return_value=io.StringIO("fun"))
    def test_logic_term_bad_expression(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.LogicTerm, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("!fun"))
    def test_logic_term_bad_expression_negation(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.LogicTerm, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("!"))
    def test_logic_term_no_expression_negation(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.LogicTerm, Lexer(fr))


# noinspection PyUnusedLocal
class AdditiveOperatorNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("+"))
    def test_additive_operator_plus(self, mock_open):
        self.assert_node(syntax_analysis.AdditiveOperator, [syntax_analysis.PlusOperator])

    @mock.patch('builtins.open', return_value=io.StringIO("-"))
    def test_additive_operator_minus(self, mock_open):
        self.assert_node(syntax_analysis.AdditiveOperator, [syntax_analysis.MinusOperator])

    @mock.patch('builtins.open', return_value=io.StringIO("*"))
    def test_additive_operator_bad_operator(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.AdditiveOperator, Lexer(fr))


# noinspection PyUnusedLocal
class MultiplicativeOperatorNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("*"))
    def test_multiplicative_operator_multiply(self, mock_open):
        self.assert_node(syntax_analysis.MultiplicativeOperator, [syntax_analysis.MultiplyOperator])

    @mock.patch('builtins.open', return_value=io.StringIO("/"))
    def test_multiplicative_operator_divide(self, mock_open):
        self.assert_node(syntax_analysis.MultiplicativeOperator, [syntax_analysis.DivisionOperator])

    @mock.patch('builtins.open', return_value=io.StringIO("+"))
    def test_multiplicative_operator_bad_operator(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.MultiplicativeOperator, Lexer(fr))


# noinspection PyUnusedLocal
class EqualityOperatorNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("=="))
    def test_equality_operator_equals(self, mock_open):
        self.assert_node(syntax_analysis.EqualityOperator, [syntax_analysis.EqualOperator])

    @mock.patch('builtins.open', return_value=io.StringIO("!="))
    def test_equality_operator_not_equals(self, mock_open):
        self.assert_node(syntax_analysis.EqualityOperator, [syntax_analysis.NotEqualOperator])

    @mock.patch('builtins.open', return_value=io.StringIO(">"))
    def test_equality_operator_bad_operator(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.EqualityOperator, Lexer(fr))


# noinspection PyUnusedLocal
class RelationOperatorNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO(">"))
    def test_relation_operator_greater(self, mock_open):
        self.assert_node(syntax_analysis.RelationOperator, [syntax_analysis.GreaterOperator])

    @mock.patch('builtins.open', return_value=io.StringIO(">="))
    def test_relation_operator_greater_or_equal(self, mock_open):
        self.assert_node(syntax_analysis.RelationOperator, [syntax_analysis.GreaterOrEqualOperator])

    @mock.patch('builtins.open', return_value=io.StringIO("<"))
    def test_relation_operator_less(self, mock_open):
        self.assert_node(syntax_analysis.RelationOperator, [syntax_analysis.LessOperator])

    @mock.patch('builtins.open', return_value=io.StringIO("<="))
    def test_relation_operator_less_or_equal(self, mock_open):
        self.assert_node(syntax_analysis.RelationOperator, [syntax_analysis.LessOrEqualOperator])

    @mock.patch('builtins.open', return_value=io.StringIO("=="))
    def test_relation_operator_bad_operator(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.RelationOperator, Lexer(fr))


# noinspection PyUnusedLocal
class TimeUnitNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("years"))
    def test_time_unit_years(self, mock_open):
        self.assert_node(syntax_analysis.TimeUnit, [syntax_analysis.Years])

    @mock.patch('builtins.open', return_value=io.StringIO("months"))
    def test_time_unit_months(self, mock_open):
        self.assert_node(syntax_analysis.TimeUnit, [syntax_analysis.Months])

    @mock.patch('builtins.open', return_value=io.StringIO("weeks"))
    def test_time_unit_weeks(self, mock_open):
        self.assert_node(syntax_analysis.TimeUnit, [syntax_analysis.Weeks])

    @mock.patch('builtins.open', return_value=io.StringIO("days"))
    def test_time_unit_days(self, mock_open):
        self.assert_node(syntax_analysis.TimeUnit, [syntax_analysis.Days])

    @mock.patch('builtins.open', return_value=io.StringIO("hours"))
    def test_time_unit_hours(self, mock_open):
        self.assert_node(syntax_analysis.TimeUnit, [syntax_analysis.Hours])

    @mock.patch('builtins.open', return_value=io.StringIO("minutes"))
    def test_time_unit_minutes(self, mock_open):
        self.assert_node(syntax_analysis.TimeUnit, [syntax_analysis.Minutes])

    @mock.patch('builtins.open', return_value=io.StringIO("seconds"))
    def test_time_unit_seconds(self, mock_open):
        self.assert_node(syntax_analysis.TimeUnit, [syntax_analysis.Seconds])

    @mock.patch('builtins.open', return_value=io.StringIO("bruh"))
    def test_time_unit_bad_unit(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.TimeUnit, Lexer(fr))


# noinspection PyUnusedLocal
class ValueNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("10"))
    def test_value_literal(self, mock_open):
        self.assert_node(syntax_analysis.Value, [syntax_analysis.Literal])

    @mock.patch('builtins.open', return_value=io.StringIO("a"))
    def test_value_identifier_first_value(self, mock_open):
        self.assert_node(syntax_analysis.Value, [syntax_analysis.IdentifierFirstValue])

    @mock.patch('builtins.open', return_value=io.StringIO("return"))
    def test_value_bad_value(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.Value, Lexer(fr))


# noinspection PyUnusedLocal
class LiteralNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("10"))
    def test_literal_number(self, mock_open):
        self.assert_node(syntax_analysis.Literal, [syntax_analysis.NumberLiteral])

    @mock.patch('builtins.open', return_value=io.StringIO('"abc"'))
    def test_literal_string(self, mock_open):
        self.assert_node(syntax_analysis.Literal, [syntax_analysis.StringLiteral])

    @mock.patch('builtins.open', return_value=io.StringIO("01.01.2020"))
    def test_literal_date(self, mock_open):
        self.assert_node(syntax_analysis.Literal, [syntax_analysis.DateLiteral])

    @mock.patch('builtins.open', return_value=io.StringIO("10:00:00"))
    def test_literal_time(self, mock_open):
        self.assert_node(syntax_analysis.Literal, [syntax_analysis.TimeLiteral])

    @mock.patch('builtins.open', return_value=io.StringIO("01.01.2020~10:00:00"))
    def test_literal_datetime(self, mock_open):
        self.assert_node(syntax_analysis.Literal, [syntax_analysis.DateTimeLiteral])

    @mock.patch('builtins.open', return_value=io.StringIO("'1Y 5D'"))
    def test_literal_timedelta(self, mock_open):
        self.assert_node(syntax_analysis.Literal, [syntax_analysis.TimedeltaLiteral])

    @mock.patch('builtins.open', return_value=io.StringIO("return"))
    def test_literal_bad_literal(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.Literal, Lexer(fr))


# noinspection PyUnusedLocal
class IdentifierFirstValueNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("abc"))
    def test_identifier_first_value_identifier(self, mock_open):
        self.assert_node(syntax_analysis.IdentifierFirstValue, [syntax_analysis.Identifier])

    @mock.patch('builtins.open', return_value=io.StringIO("abc()"))
    def test_identifier_first_value_function_call(self, mock_open):
        self.assert_node(syntax_analysis.IdentifierFirstValue, [syntax_analysis.FunctionCall])

    @mock.patch('builtins.open', return_value=io.StringIO("abc.days"))
    def test_identifier_first_value_time_info_access(self, mock_open):
        self.assert_node(syntax_analysis.IdentifierFirstValue, [syntax_analysis.TimeInfoAccess])

    @mock.patch('builtins.open', return_value=io.StringIO("()"))
    def test_identifier_first_value_function_call_no_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.IdentifierFirstValue, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO(".days"))
    def test_identifier_first_value_time_info_access_no_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.IdentifierFirstValue, Lexer(fr))


# noinspection PyUnusedLocal
class FunctionCallNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("abc(a)"))
    def test_function_call(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            node = syntax_analysis.FunctionCall(lexer, syntax_analysis.Identifier(lexer))
            children_types = [type(child) for child in node.children]
            self.assertEqual(children_types, [syntax_analysis.Identifier, syntax_analysis.ParametersCall])

    @mock.patch('builtins.open', return_value=io.StringIO("abc"))
    def test_function_call_no_parameters(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.FunctionCall, lexer,
                              syntax_analysis.Identifier(lexer))


# noinspection PyUnusedLocal
class ParametersCallNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("(a, 10, abc(15))"))
    def test_parameters_call(self, mock_open):
        self.assert_node(syntax_analysis.ParametersCall, [syntax_analysis.Expression,
                                                          syntax_analysis.Expression,
                                                          syntax_analysis.Expression])

    @mock.patch('builtins.open', return_value=io.StringIO("(a)"))
    def test_parameters_call_single_parameter(self, mock_open):
        self.assert_node(syntax_analysis.ParametersCall, [syntax_analysis.Expression])

    @mock.patch('builtins.open', return_value=io.StringIO("()"))
    def test_parameters_call_no_parameters(self, mock_open):
        self.assert_node(syntax_analysis.ParametersCall, [])

    @mock.patch('builtins.open', return_value=io.StringIO("a, 10, abc(15))"))
    def test_parameters_call_no_left_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParametersCall, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(a, 10, abc(15)"))
    def test_parameters_call_no_right_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParametersCall, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(a 10 abc(15))"))
    def test_parameters_call_no_commas(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParametersCall, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(a, return, abc(15))"))
    def test_parameters_call_bad_identifier(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParametersCall, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("{a, 10, abc(15)}"))
    def test_parameters_call_bad_parenthesis(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParametersCall, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("(a, )"))
    def test_parameters_call_dangling_comma(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.ParametersDeclaration, Lexer(fr))


# noinspection PyUnusedLocal
class TimeInfoAccessNodeTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a.days"))
    def test_time_info_access(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            node = syntax_analysis.TimeInfoAccess(lexer, syntax_analysis.Identifier(lexer))
            children_types = [type(child) for child in node.children]
            self.assertEqual(children_types, [syntax_analysis.Identifier, syntax_analysis.TimeUnit])

    @mock.patch('builtins.open', return_value=io.StringIO("a days"))
    def test_time_info_access_no_access(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.TimeInfoAccess, lexer,
                              syntax_analysis.Identifier(lexer))

    @mock.patch('builtins.open', return_value=io.StringIO("a."))
    def test_time_info_access_no_unit(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.TimeInfoAccess, lexer,
                              syntax_analysis.Identifier(lexer))

    @mock.patch('builtins.open', return_value=io.StringIO("a,days"))
    def test_time_info_access_bad_access(self, mock_open):
        with FileReader("whatever") as fr:
            lexer = Lexer(fr)
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.TimeInfoAccess, lexer,
                              syntax_analysis.Identifier(lexer))


# noinspection PyUnusedLocal
class ParsingMiscellaneousTestCase(BaseParsingTestCase):
    @mock.patch('builtins.open', return_value=io.StringIO("a = 3 * (1 + 2);"))
    def test_math_with_parenthesis(self, mock_open):
        self.assert_node(syntax_analysis.Program, [syntax_analysis.NestableStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("a = a > (1 + 2);"))
    def test_expression_with_logic_and_math(self, mock_open):
        self.assert_node(syntax_analysis.Program, [syntax_analysis.NestableStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("a = a > (1 > 2);"))
    def test_expression_with_logic(self, mock_open):
        self.assert_node(syntax_analysis.Program, [syntax_analysis.NestableStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("a = a + (1 > 2);"))
    def test_expression_with_math_and_logic(self, mock_open):
        self.assert_node(syntax_analysis.Program, [syntax_analysis.NestableStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("a = (a + 0) & (1 + 2);"))
    def test_expression_with_logic_and_math_between_parenthesis(self, mock_open):
        self.assert_node(syntax_analysis.Program, [syntax_analysis.NestableStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("a = (a > 0) & (1 > 2);"))
    def test_expression_with_logic_between_logic_parenthesis(self, mock_open):
        self.assert_node(syntax_analysis.Program, [syntax_analysis.NestableStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("if a + b {};"))
    def test_if_with_math(self, mock_open):
        self.assert_node(syntax_analysis.Program, [syntax_analysis.NestableStatement])

    @mock.patch('builtins.open', return_value=io.StringIO("if a == b != c { return; };"))
    def test_multiple_equality_operations(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.Program, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("if a > b < c { return; };"))
    def test_multiple_relation_operations(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.Program, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("if a > b { print 1; } { print 1; };"))
    def test_no_else_keyword(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.Program, Lexer(fr))

    @mock.patch('builtins.open', return_value=io.StringIO("var a 10;"))
    def test_no_assign(self, mock_open):
        with FileReader("whatever") as fr:
            self.assertRaises(error_handling.SyntacticError, syntax_analysis.Program, Lexer(fr))
