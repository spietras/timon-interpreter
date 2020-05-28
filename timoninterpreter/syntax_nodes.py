"""

Syntax analysis module

"""

from abc import ABC, abstractmethod

from timoninterpreter import tokens
from timoninterpreter.error_handling import SyntacticError


class BaseNode(ABC):
    """
    Node base class
    """

    def reduce(self):
        return self

    @classmethod
    def starting_token_types(cls):
        """
        Get token types that this rule can start with

        Returns:
            Set of token types
        """
        return {t for n in cls._starting_nodes() for t in n.starting_token_types()}

    @classmethod
    @abstractmethod
    def _starting_nodes(cls):
        """
        Get nodes that this rules can start with

        Returns:
            Set of node classes
        """
        pass

    @abstractmethod
    def get_children(self):
        """
        Get children on this node

        Returns:
            List of nodes
        """
        pass

    @staticmethod
    def choose_and_build_node(lexer, possible_nodes, required=True):
        token = lexer.peek()

        for node in possible_nodes:
            if token.get_type() in node.starting_token_types():
                return node(lexer).reduce()

        if not required:
            return None

        BaseNode.make_error(token, {t for n in possible_nodes for t in n.starting_token_types()}, lexer)

    @staticmethod
    def make_error(token, expected_tokens, lexer):
        raise SyntacticError(token,
                             "Expected one of {} but got {}".format(expected_tokens, token.get_type()))


class LeafNode(BaseNode, ABC):
    """
    Node that doesn't have children, therefore must contain token
    """

    def __init__(self, lexer):
        super().__init__()
        self.token = lexer.peek()
        if self.token.get_type() != self.token_type():
            self.make_error(self.token, {self.token_type()}, lexer)
        lexer.get()

    @classmethod
    @abstractmethod
    def token_type(cls):
        """
        Get token type of this node
        """
        pass

    @classmethod
    def starting_token_types(cls):
        return {cls.token_type()}

    @classmethod
    def _starting_nodes(cls):
        return None

    def get_children(self):
        return []


class ReducibleNode(BaseNode, ABC):
    def reduce(self):
        if len(self.get_children()) == 1:
            return self.get_children()[0]

        return self


class BinaryEvaluable(ABC):
    @abstractmethod
    def binary_evaluate(self, lhs, rhs, environment):
        pass


class UnaryEvaluable(ABC):
    @abstractmethod
    def unary_evaluate(self, rhs, environment):
        pass


class SelfEvaluable(ABC):
    @abstractmethod
    def self_evaluate(self, environment):
        pass


class Executable(ABC):
    @abstractmethod
    def execute(self, environment):
        pass


class Semicolon(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.SEMICOLON


class FunKeyword(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.FUN


class VarKeyword(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.VAR


class IfKeyword(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.IF


class ElseKeyword(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.ELSE


class FromKeyword(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.FROM


class PrintKeyword(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.PRINT


class ReturnKeyword(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.RETURN


class ToKeyword(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.TO


class ByKeyword(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.BY


class AsKeyword(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.AS


class LeftParenthesis(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.LEFT_PARENTHESIS


class RightParenthesis(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.RIGHT_PARENTHESIS


class Comma(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.COMMA


class LeftBracket(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.LEFT_BRACKET


class RightBracket(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.RIGHT_BRACKET


class Assign(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.ASSIGN


class Access(LeafNode):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.ACCESS


class Identifier(LeafNode, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.IDENTIFIER

    def self_evaluate(self, environment):
        return environment.get_var(self.token.get_value())


class Program(BaseNode, Executable):
    def __init__(self, lexer):
        self.statements = []
        token = lexer.peek()
        while token.get_type() != tokens.TokenType.END:
            self.statements.append(self.choose_and_build_node(lexer, self._starting_nodes()))
            token = lexer.peek()

    @classmethod
    def _starting_nodes(cls):
        return {FunctionDefinitionStatement,
                IdentifierFirstStatement,
                VariableDefinitionStatement,
                IfStatement, FromStatement,
                PrintStatement,
                ReturnStatement}

    def get_children(self):
        return self.statements

    def execute(self, environment):
        for statement in self.statements:
            if isinstance(statement, ReturnStatement):
                return statement.execute(environment)
            statement.execute(environment)

        return None


class IdentifierFirstStatement(ReducibleNode, Executable):
    def __init__(self, lexer):
        identifier = Identifier(lexer)
        token = lexer.peek()
        if token.get_type() in FunctionCall.starting_token_types():
            self.statement = FunctionCall(lexer, identifier)
        elif token.get_type() in VariableAssignmentStatement.starting_token_types():
            self.statement = VariableAssignmentStatement(lexer, identifier)
        else:
            self.make_error(token,
                            FunctionCall.starting_token_types() | VariableAssignmentStatement.starting_token_types(),
                            lexer)
        Semicolon(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {Identifier}

    def get_children(self):
        return [self.statement]

    def execute(self, environment):
        self.statement.execute(environment)


class VariableAssignmentStatement(BaseNode, Executable):
    def __init__(self, lexer,
                 identifier):  # have to pass identifier as it was already parsed above (because of ambiguity)
        self.identifier = identifier
        Assign(lexer)
        self.expression = Expression(lexer).reduce()

    @classmethod
    def _starting_nodes(cls):
        return {Assign}

    def get_children(self):
        return [self.identifier, self.expression]

    def execute(self, environment):
        environment.set_var(self.identifier.token.get_value(), self.expression.self_evaluate(environment))


class FunctionDefinitionStatement(BaseNode, Executable):
    def __init__(self, lexer):
        FunKeyword(lexer)
        self.identifier = Identifier(lexer)
        self.parameters = ParametersDeclaration(lexer)
        self.body = Body(lexer)
        Semicolon(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {FunKeyword}

    def get_children(self):
        return [self.identifier, self.parameters, self.body]

    def execute(self, environment):
        environment.set_fun(self.identifier.token.get_value(), self)


class VariableDefinitionStatement(BaseNode, Executable):
    def __init__(self, lexer):
        VarKeyword(lexer)
        self.identifier = Identifier(lexer)
        self.assignment = None
        token = lexer.peek()
        if token.get_type() in VariableAssignmentStatement.starting_token_types():
            self.assignment = VariableAssignmentStatement(lexer, self.identifier)
        Semicolon(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {VarKeyword}

    def get_children(self):
        if self.assignment is None:
            return [self.identifier]

        return [self.identifier, self.assignment]

    def execute(self, environment):
        environment.add_var(self.identifier.token.get_value())
        if self.assignment:
            self.assignment.execute(environment)


class IfStatement(BaseNode, Executable):
    def __init__(self, lexer):
        IfKeyword(lexer)
        self.expression = Expression(lexer).reduce()
        self.body = Body(lexer)
        self.else_body = None
        token = lexer.peek()
        if token.get_type() in ElseKeyword.starting_token_types():
            ElseKeyword(lexer)
            self.else_body = Body(lexer)
        Semicolon(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {IfKeyword}

    def get_children(self):
        if self.else_body is None:
            return [self.expression, self.body]

        return [self.expression, self.body, self.else_body]

    def execute(self, environment):
        if self.expression.self_evaluate(environment):
            environment.push_scope()
            self.body.execute(environment)
            environment.pop_scope()
        elif self.else_body:
            environment.push_scope()
            self.else_body.execute(environment)
            environment.pop_scope()


class FromStatement(BaseNode, Executable):
    def __init__(self, lexer):
        FromKeyword(lexer)
        self.start = Expression(lexer).reduce()
        ToKeyword(lexer)
        self.end = Expression(lexer).reduce()
        ByKeyword(lexer)
        self.time_unit = self.choose_and_build_node(lexer, {Years,
                                                            Months,
                                                            Weeks,
                                                            Days,
                                                            Hours,
                                                            Minutes,
                                                            Seconds})
        AsKeyword(lexer)
        self.identifier = Identifier(lexer)
        self.body = Body(lexer)
        Semicolon(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {FromKeyword}

    def get_children(self):
        return [self.start, self.end, self.time_unit, self.identifier, self.body]

    def execute(self, environment):
        environment.push_scope()
        start = self.start.self_evaluate(environment)
        end = self.end.self_evaluate(environment)
        step = self.time_unit.self_evaluate(environment)

        while start <= end:
            environment.push_scope()
            environment.add_var(self.identifier.token.get_value())
            environment.set_var(self.identifier.token.get_value(), start)
            self.body.execute(environment)
            environment.pop_scope()
            start += step


class PrintStatement(BaseNode, Executable):
    def __init__(self, lexer):
        PrintKeyword(lexer)
        self.expression = Expression(lexer).reduce()
        Semicolon(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {PrintKeyword}

    def get_children(self):
        return [self.expression]

    def execute(self, environment):
        print(self.expression.self_evaluate(environment))


class ReturnStatement(BaseNode, Executable):
    def __init__(self, lexer):
        ReturnKeyword(lexer)
        self.expression = self.choose_and_build_node(lexer, {Expression}, required=False)
        if self.expression:
            self.expression = self.expression.reduce()
        Semicolon(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {ReturnKeyword}

    def get_children(self):
        if self.expression is None:
            return []

        return [self.expression]

    def execute(self, environment):
        pass


class ParametersDeclaration(BaseNode, Executable):
    def __init__(self, lexer):
        LeftParenthesis(lexer)
        self.parameters = []
        token = lexer.peek()
        if token.get_type() in Identifier.starting_token_types():
            self.parameters.append(Identifier(lexer))
            token = lexer.peek()
            while token.get_type() in Comma.starting_token_types():
                Comma(lexer)
                self.parameters.append(Identifier(lexer))
                token = lexer.peek()
        RightParenthesis(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {LeftParenthesis}

    def get_children(self):
        return self.parameters

    def execute(self, environment):
        for parameter in self.parameters:
            environment.add_var(parameter.token.get_value())


class Body(BaseNode, Executable):
    def __init__(self, lexer):
        LeftBracket(lexer)
        self.statements = []
        node = self.choose_and_build_node(lexer, {IdentifierFirstStatement,
                                                  VariableDefinitionStatement,
                                                  IfStatement, FromStatement,
                                                  PrintStatement,
                                                  ReturnStatement}, required=False)
        while node:
            self.statements.append(node)
            node = self.choose_and_build_node(lexer, {IdentifierFirstStatement,
                                                      VariableDefinitionStatement,
                                                      IfStatement, FromStatement,
                                                      PrintStatement,
                                                      ReturnStatement}, required=False)
        RightBracket(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {LeftBracket}

    def get_children(self):
        return self.statements

    def execute(self, environment):
        for statement in self.statements:
            if isinstance(statement, ReturnStatement):
                return statement.execute(environment)
            statement.execute(environment)

        return None


class Expression(ReducibleNode, SelfEvaluable):
    def __init__(self, lexer):
        self.first_expression = LogicAndExpression(lexer).reduce()
        self.operations = []
        token = lexer.peek()
        while token.get_type() in OrOperator.starting_token_types():
            self.operations.append((OrOperator(lexer), LogicAndExpression(lexer).reduce()))
            token = lexer.peek()

    @classmethod
    def _starting_nodes(cls):
        return {LogicAndExpression}

    def get_children(self):
        return [self.first_expression] + [x for operation in self.operations for x in operation]

    def self_evaluate(self, environment):
        value = self.first_expression.self_evaluate(environment)
        for operator, expression in self.operations:
            value = operator.binary_evaluate(value, expression.self_evaluate(environment), environment)
        return value


class LogicAndExpression(ReducibleNode, SelfEvaluable):
    def __init__(self, lexer):
        self.first_expression = LogicEqualityExpression(lexer).reduce()
        self.operations = []
        token = lexer.peek()
        while token.get_type() in AndOperator.starting_token_types():
            self.operations.append((AndOperator(lexer), LogicEqualityExpression(lexer).reduce()))
            token = lexer.peek()

    @classmethod
    def _starting_nodes(cls):
        return {LogicEqualityExpression}

    def get_children(self):
        return [self.first_expression] + [x for operation in self.operations for x in operation]

    def self_evaluate(self, environment):
        value = self.first_expression.self_evaluate(environment)
        for operator, expression in self.operations:
            value = operator.binary_evaluate(value, expression.self_evaluate(environment), environment)
        return value


class LogicEqualityExpression(ReducibleNode, SelfEvaluable):
    def __init__(self, lexer):
        self.first_expression = LogicRelationalExpression(lexer).reduce()
        self.operator = self.choose_and_build_node(lexer, {EqualOperator, NotEqualOperator}, required=False)
        if self.operator:
            self.second_expression = LogicRelationalExpression(lexer).reduce()

    @classmethod
    def _starting_nodes(cls):
        return {LogicRelationalExpression}

    def get_children(self):
        if self.operator is None:
            return [self.first_expression]

        return [self.first_expression, self.operator, self.second_expression]

    def self_evaluate(self, environment):
        value = self.first_expression.self_evaluate(environment)
        if self.operator:
            value = self.operator.binary_evaluate(value, self.second_expression.self_evaluate(environment), environment)
        return value


class LogicRelationalExpression(ReducibleNode, SelfEvaluable):
    def __init__(self, lexer):
        self.first_expression = LogicTerm(lexer).reduce()
        self.operator = self.choose_and_build_node(lexer, {GreaterOperator, GreaterOrEqualOperator, LessOperator,
                                                           LessOrEqualOperator}, required=False)
        if self.operator:
            self.second_expression = LogicTerm(lexer).reduce()

    @classmethod
    def _starting_nodes(cls):
        return {LogicTerm}

    def get_children(self):
        if self.operator is None:
            return [self.first_expression]

        return [self.first_expression, self.operator, self.second_expression]

    def self_evaluate(self, environment):
        value = self.first_expression.self_evaluate(environment)
        if self.operator:
            value = self.operator.binary_evaluate(value, self.second_expression.self_evaluate(environment), environment)
        return value


class LogicTerm(ReducibleNode, SelfEvaluable):
    def __init__(self, lexer):
        self.negation = self.choose_and_build_node(lexer, {LogicNegationOperator}, required=False)
        self.expression = MathExpression(lexer).reduce()

    @classmethod
    def _starting_nodes(cls):
        return {LogicNegationOperator, MathExpression}

    def get_children(self):
        if self.negation is None:
            return [self.expression]

        return [self.negation, self.expression]

    def self_evaluate(self, environment):
        value = self.expression.self_evaluate(environment)
        if self.negation:
            return self.negation.unary_evaluate(value, environment)
        return value


class MathExpression(ReducibleNode, SelfEvaluable):
    def __init__(self, lexer):
        self.first_expression = MultiplicativeMathExpression(lexer).reduce()
        self.operations = []
        operator = self.choose_and_build_node(lexer, {PlusOperator, MinusOperator}, required=False)
        while operator:
            self.operations.append((operator, MultiplicativeMathExpression(lexer).reduce()))
            operator = self.choose_and_build_node(lexer, {PlusOperator, MinusOperator}, required=False)

    @classmethod
    def _starting_nodes(cls):
        return {MultiplicativeMathExpression}

    def get_children(self):
        return [self.first_expression] + [x for operation in self.operations for x in operation]

    def self_evaluate(self, environment):
        value = self.first_expression.self_evaluate(environment)
        for operator, expression in self.operations:
            value = operator.binary_evaluate(value, expression.self_evaluate(environment), environment)
        return value


class MultiplicativeMathExpression(ReducibleNode, SelfEvaluable):
    def __init__(self, lexer):
        self.first_expression = MathTerm(lexer).reduce()
        self.operations = []
        operator = self.choose_and_build_node(lexer, {MultiplyOperator, DivisionOperator}, required=False)
        while operator:
            self.operations.append((operator, MathTerm(lexer).reduce()))
            operator = self.choose_and_build_node(lexer, {MultiplyOperator, DivisionOperator}, required=False)

    @classmethod
    def _starting_nodes(cls):
        return {MathTerm}

    def get_children(self):
        return [self.first_expression] + [x for operation in self.operations for x in operation]

    def self_evaluate(self, environment):
        value = self.first_expression.self_evaluate(environment)
        for operator, expression in self.operations:
            value = operator.binary_evaluate(value, expression.self_evaluate(environment), environment)
        return value


class MathTerm(ReducibleNode, SelfEvaluable):
    def __init__(self, lexer):
        self.negation = self.choose_and_build_node(lexer, {MathNegationOperator}, required=False)
        self.term = self.choose_and_build_node(lexer, {NumberLiteral,
                                                       StringLiteral,
                                                       DateLiteral,
                                                       TimeLiteral,
                                                       DateTimeLiteral,
                                                       TimedeltaLiteral,
                                                       IdentifierFirstValue,
                                                       ParenthesisedExpression})

    @classmethod
    def _starting_nodes(cls):
        return {MathNegationOperator,
                NumberLiteral,
                StringLiteral,
                DateLiteral,
                TimeLiteral,
                DateTimeLiteral,
                TimedeltaLiteral,
                IdentifierFirstValue,
                ParenthesisedExpression}

    def get_children(self):
        if self.negation is None:
            return [self.term]

        return [self.negation, self.term]

    def self_evaluate(self, environment):
        value = self.term.self_evaluate(environment)
        if self.negation:
            return self.negation.unary_evaluate(value, environment)
        return value


class ParenthesisedExpression(ReducibleNode, SelfEvaluable):
    def __init__(self, lexer):
        LeftParenthesis(lexer)
        self.expression = Expression(lexer).reduce()
        RightParenthesis(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {LeftParenthesis}

    def get_children(self):
        return [self.expression]

    def self_evaluate(self, environment):
        return self.expression.self_evaluate(environment)


class PlusOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.PLUS

    def binary_evaluate(self, lhs, rhs, environment):
        if isinstance(lhs, str) or isinstance(rhs, str):
            lhs, rhs = str(lhs), str(rhs)
        return lhs + rhs


class MinusOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.MINUS

    def binary_evaluate(self, lhs, rhs, environment):
        return lhs - rhs


class MultiplyOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.MULTIPLICATION

    def binary_evaluate(self, lhs, rhs, environment):
        return lhs * rhs


class DivisionOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.DIVISION

    def binary_evaluate(self, lhs, rhs, environment):
        return lhs // rhs


class OrOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.LOGICAL_OR

    def binary_evaluate(self, lhs, rhs, environment):
        return bool(lhs) or bool(rhs)


class AndOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.LOGICAL_AND

    def binary_evaluate(self, lhs, rhs, environment):
        return bool(lhs) and bool(rhs)


class EqualOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.EQUALS

    def binary_evaluate(self, lhs, rhs, environment):
        return lhs == rhs


class NotEqualOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.NOT_EQUALS

    def binary_evaluate(self, lhs, rhs, environment):
        return lhs != rhs


class GreaterOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.GREATER

    def binary_evaluate(self, lhs, rhs, environment):
        return lhs > rhs


class GreaterOrEqualOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.GREATER_OR_EQUAL

    def binary_evaluate(self, lhs, rhs, environment):
        return lhs >= rhs


class LessOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.LESS

    def binary_evaluate(self, lhs, rhs, environment):
        return lhs < rhs


class LessOrEqualOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.LESS_OR_EQUAL

    def binary_evaluate(self, lhs, rhs, environment):
        return lhs <= rhs


class MathNegationOperator(LeafNode, UnaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.MINUS

    def unary_evaluate(self, rhs, environment):
        return -rhs


class LogicNegationOperator(LeafNode, UnaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.NOT

    def unary_evaluate(self, rhs, environment):
        return not bool(rhs)


class Years(LeafNode, UnaryEvaluable, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.YEARS

    def unary_evaluate(self, rhs, environment):
        return rhs.get_years()

    def self_evaluate(self, environment):
        return tokens.TimedeltaValue(years=1)


class Months(LeafNode, UnaryEvaluable, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.MONTHS

    def unary_evaluate(self, rhs, environment):
        return rhs.get_months()

    def self_evaluate(self, environment):
        return tokens.TimedeltaValue(months=1)


class Weeks(LeafNode, UnaryEvaluable, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.WEEKS

    def unary_evaluate(self, rhs, environment):
        return rhs.get_weeks()

    def self_evaluate(self, environment):
        return tokens.TimedeltaValue(weeks=1)


class Days(LeafNode, UnaryEvaluable, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.DAYS

    def unary_evaluate(self, rhs, environment):
        return rhs.get_days()

    def self_evaluate(self, environment):
        return tokens.TimedeltaValue(days=1)


class Hours(LeafNode, UnaryEvaluable, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.HOURS

    def unary_evaluate(self, rhs, environment):
        return rhs.get_hours()

    def self_evaluate(self, environment):
        return tokens.TimedeltaValue(hours=1)


class Minutes(LeafNode, UnaryEvaluable, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.MINUTES

    def unary_evaluate(self, rhs, environment):
        return rhs.get_minutes()

    def self_evaluate(self, environment):
        return tokens.TimedeltaValue(minutes=1)


class Seconds(LeafNode, UnaryEvaluable, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.SECONDS

    def unary_evaluate(self, rhs, environment):
        return rhs.get_seconds()

    def self_evaluate(self, environment):
        return tokens.TimedeltaValue(seconds=1)


class NumberLiteral(LeafNode, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.NUMBER_LITERAL

    def self_evaluate(self, environment):
        return self.token.get_value()


class StringLiteral(LeafNode, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.STRING_LITERAL

    def self_evaluate(self, environment):
        return self.token.get_value()


class DateLiteral(LeafNode, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.DATE_LITERAL

    def self_evaluate(self, environment):
        return self.token.get_value()


class TimeLiteral(LeafNode, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.TIME_LITERAL

    def self_evaluate(self, environment):
        return self.token.get_value()


class DateTimeLiteral(LeafNode, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.DATETIME_LITERAL

    def self_evaluate(self, environment):
        return self.token.get_value()


class TimedeltaLiteral(LeafNode, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.TIMEDELTA_LITERAL

    def self_evaluate(self, environment):
        return self.token.get_value()


class IdentifierFirstValue(ReducibleNode, SelfEvaluable):
    def __init__(self, lexer):
        identifier = Identifier(lexer)
        token = lexer.peek()
        if token.get_type() in FunctionCall.starting_token_types():
            self.value = FunctionCall(lexer, identifier)
        elif token.get_type() in TimeInfoAccess.starting_token_types():
            self.value = TimeInfoAccess(lexer, identifier)
        else:
            self.value = identifier

    @classmethod
    def _starting_nodes(cls):
        return {Identifier}

    def get_children(self):
        return [self.value]

    def self_evaluate(self, environment):
        return self.value.self_evaluate(environment)


class FunctionCall(BaseNode, Executable, SelfEvaluable):
    def __init__(self, lexer,
                 identifier):  # have to pass identifier as it was already parsed above (because of ambiguity)
        self.identifier = identifier
        LeftParenthesis(lexer)
        self.parameters = []
        token = lexer.peek()
        if token.get_type() in Expression.starting_token_types():
            self.parameters.append(Expression(lexer).reduce())
            token = lexer.peek()
            while token.get_type() in Comma.starting_token_types():
                Comma(lexer)
                self.parameters.append(Expression(lexer).reduce())
                token = lexer.peek()
        RightParenthesis(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {LeftParenthesis}

    def get_children(self):
        return [self.identifier] + self.parameters

    def execute(self, environment):
        self.self_evaluate(environment)

    def self_evaluate(self, environment):
        fun_node = environment.get_fun(self.identifier.token.get_value())
        if len(fun_node.parameters.parameters) != len(self.parameters):
            raise ValueError("TODO")
        environment.push_scope()
        fun_node.parameters.execute(environment)
        for param_id, param_val in zip(fun_node.parameters.parameters, self.parameters):
            environment.set_var(param_id.token.get_value(), param_val.self_evaluate(environment))
        fun_node.body.execute(environment)
        environment.pop_scope()
        return 1  # TODO


class TimeInfoAccess(BaseNode, SelfEvaluable):
    def __init__(self, lexer,
                 identifier):  # have to pass identifier as it was already parsed above (because of ambiguity)
        self.identifier = identifier
        Access(lexer)
        self.time_unit = self.choose_and_build_node(lexer, {Years,
                                                            Months,
                                                            Weeks,
                                                            Days,
                                                            Hours,
                                                            Minutes,
                                                            Seconds})

    @classmethod
    def _starting_nodes(cls):
        return {Access}

    def get_children(self):
        return [self.identifier, self.time_unit]

    def self_evaluate(self, environment):
        return self.time_unit.unary_evaluate(self.identifier.token.get_value, environment)
