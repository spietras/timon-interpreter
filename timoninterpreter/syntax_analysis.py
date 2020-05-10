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
    def make_error(token, expected_tokens, lexer):
        raise SyntacticError(token,
                             "Expected one of {} but got {}".format(expected_tokens, token.get_type()))


class SwitchNode(BaseNode, ABC):
    """
    Node type for nodes with multiple possible child types
    """

    def __init__(self, lexer):
        token = lexer.peek()

        for node in self._starting_nodes():
            if token.get_type() in node.starting_token_types():
                self.child = node(lexer)
                return

        self.make_error(token, self.starting_token_types(), lexer)

    def get_children(self):
        return [self.child]


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


class BinaryEvaluable(ABC):
    @abstractmethod
    def evaluate(self, lhs, rhs, environment):
        pass


class UnaryEvaluable(ABC):
    @abstractmethod
    def evaluate(self, rhs, environment):
        pass


class SelfEvaluable(ABC):
    @abstractmethod
    def evaluate(self, environment):
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

    def evaluate(self, environment):
        pass


class Program(BaseNode, Executable):
    def __init__(self, lexer):
        self.statements = []
        token = lexer.peek()
        while token.get_type() != tokens.TokenType.END:
            if token.get_type() in NonNestableStatement.starting_token_types():
                self.statements.append(NonNestableStatement(lexer))
            elif token.get_type() in NestableStatement.starting_token_types():
                self.statements.append(NestableStatement(lexer))
            else:
                self.make_error(token, self.starting_token_types(), lexer)

            token = lexer.peek()

    @classmethod
    def _starting_nodes(cls):
        return {NonNestableStatement, NestableStatement}

    def get_children(self):
        return self.statements

    def execute(self, environment):
        pass


class NonNestableStatement(BaseNode, Executable):
    def __init__(self, lexer):
        self.statement = FunctionDefinitionStatement(lexer)
        Semicolon(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {FunctionDefinitionStatement}

    def get_children(self):
        return [self.statement]

    def execute(self, environment):
        pass


class NestableStatement(SwitchNode, Executable):
    def __init__(self, lexer):
        super().__init__(lexer)
        Semicolon(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {IdentifierFirstStatement,
                VariableDefinitionStatement,
                IfStatement, FromStatement,
                PrintStatement,
                ReturnStatement}

    def execute(self, environment):
        pass


class IdentifierFirstStatement(BaseNode, Executable):
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

    @classmethod
    def _starting_nodes(cls):
        return {Identifier}

    def get_children(self):
        return [self.statement]

    def execute(self, environment):
        pass


class VariableAssignmentStatement(BaseNode, Executable):
    def __init__(self, lexer,
                 identifier):  # have to pass identifier as it was already parsed above (because of ambiguity)
        self.identifier = identifier
        Assign(lexer)
        self.expression = Expression(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {Assign}

    def get_children(self):
        return [self.identifier, self.expression]

    def execute(self, environment):
        pass


class FunctionDefinitionStatement(BaseNode, Executable):
    def __init__(self, lexer):
        FunKeyword(lexer)
        self.identifier = Identifier(lexer)
        self.parameters = ParametersDeclaration(lexer)
        self.body = Body(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {FunKeyword}

    def get_children(self):
        return [self.identifier, self.parameters, self.body]

    def execute(self, environment):
        pass


class VariableDefinitionStatement(BaseNode, Executable):
    def __init__(self, lexer):
        VarKeyword(lexer)
        self.identifier = Identifier(lexer)
        self.assignment = None
        token = lexer.peek()
        if token.get_type() in VariableAssignmentStatement.starting_token_types():
            self.assignment = VariableAssignmentStatement(lexer, self.identifier)

    @classmethod
    def _starting_nodes(cls):
        return {VarKeyword}

    def get_children(self):
        if self.assignment is None:
            return [self.identifier]

        return [self.identifier, self.assignment]

    def execute(self, environment):
        pass


class IfStatement(BaseNode, Executable):
    def __init__(self, lexer):
        IfKeyword(lexer)
        self.expression = Expression(lexer)
        self.body = Body(lexer)
        self.else_body = None
        token = lexer.peek()
        if token.get_type() in ElseKeyword.starting_token_types():
            ElseKeyword(lexer)
            self.else_body = Body(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {IfKeyword}

    def get_children(self):
        if self.else_body is None:
            return [self.expression, self.body]

        return [self.expression, self.body, self.else_body]

    def execute(self, environment):
        pass


class FromStatement(BaseNode, Executable):
    def __init__(self, lexer):
        FromKeyword(lexer)
        self.range = FromRange(lexer)
        self.step = FromStep(lexer)
        self.iterator = FromIterator(lexer)
        self.body = Body(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {FromKeyword}

    def get_children(self):
        return [self.range, self.step, self.iterator, self.body]

    def execute(self, environment):
        pass


class PrintStatement(BaseNode, Executable):
    def __init__(self, lexer):
        PrintKeyword(lexer)
        self.expression = Expression(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {PrintKeyword}

    def get_children(self):
        return [self.expression]

    def execute(self, environment):
        pass


class ReturnStatement(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        ReturnKeyword(lexer)
        self.expression = None
        token = lexer.peek()
        if token.get_type() in Expression.starting_token_types():
            self.expression = Expression(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {ReturnKeyword}

    def get_children(self):
        if self.expression is None:
            return []

        return [self.expression]

    def evaluate(self, environment):
        pass


class ParametersDeclaration(BaseNode, SelfEvaluable):
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

    def evaluate(self, environment):
        pass


class Body(BaseNode, Executable):
    def __init__(self, lexer):
        LeftBracket(lexer)
        self.statements = []
        token = lexer.peek()
        while token.get_type() in NestableStatement.starting_token_types():
            self.statements.append(NestableStatement(lexer))
            token = lexer.peek()
        RightBracket(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {LeftBracket}

    def get_children(self):
        return self.statements

    def execute(self, environment):
        pass


class FromRange(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        self.start = Expression(lexer)
        ToKeyword(lexer)
        self.end = Expression(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {Expression}

    def get_children(self):
        return [self.start, self.end]

    def evaluate(self, environment):
        pass


class FromStep(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        ByKeyword(lexer)
        self.time_unit = TimeUnit(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {ByKeyword}

    def get_children(self):
        return [self.time_unit]

    def evaluate(self, environment):
        pass


class FromIterator(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        AsKeyword(lexer)
        self.identifier = Identifier(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {AsKeyword}

    def get_children(self):
        return [self.identifier]

    def evaluate(self, environment):
        pass


class Expression(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        self.first_expression = LogicAndExpression(lexer)
        self.operations = []
        token = lexer.peek()
        while token.get_type() in OrOperator.starting_token_types():
            self.operations.append((OrOperator(lexer), LogicAndExpression(lexer)))
            token = lexer.peek()

    @classmethod
    def _starting_nodes(cls):
        return {LogicAndExpression}

    def get_children(self):
        return [self.first_expression] + [x for operation in self.operations for x in operation]

    def evaluate(self, environment):
        pass


class LogicAndExpression(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        self.first_expression = LogicEqualityExpression(lexer)
        self.operations = []
        token = lexer.peek()
        while token.get_type() in AndOperator.starting_token_types():
            self.operations.append((AndOperator(lexer), LogicEqualityExpression(lexer)))
            token = lexer.peek()

    @classmethod
    def _starting_nodes(cls):
        return {LogicEqualityExpression}

    def get_children(self):
        return [self.first_expression] + [x for operation in self.operations for x in operation]

    def evaluate(self, environment):
        pass


class LogicEqualityExpression(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        self.first_expression = LogicRelationalExpression(lexer)
        self.operator = None
        token = lexer.peek()
        if token.get_type() in EqualityOperator.starting_token_types():
            self.operator = EqualityOperator(lexer)
            self.second_expression = LogicRelationalExpression(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {LogicRelationalExpression}

    def get_children(self):
        if self.operator is None:
            return [self.first_expression]

        return [self.first_expression, self.operator, self.second_expression]

    def evaluate(self, environment):
        pass


class LogicRelationalExpression(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        self.first_expression = LogicTerm(lexer)
        self.operator = None
        token = lexer.peek()
        if token.get_type() in RelationOperator.starting_token_types():
            self.operator = RelationOperator(lexer)
            self.second_expression = LogicTerm(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {LogicTerm}

    def get_children(self):
        if self.operator is None:
            return [self.first_expression]

        return [self.first_expression, self.operator, self.second_expression]

    def evaluate(self, environment):
        pass


class LogicTerm(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        self.negation = None
        token = lexer.peek()
        if token.get_type() in LogicNegationOperator.starting_token_types():
            self.negation = LogicNegationOperator(lexer)
        self.expression = MathExpression(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {LogicNegationOperator, MathExpression}

    def get_children(self):
        if self.negation is None:
            return [self.expression]

        return [self.negation, self.expression]

    def evaluate(self, environment):
        pass


class MathExpression(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        self.first_expression = MultiplicativeMathExpression(lexer)
        self.operations = []
        token = lexer.peek()
        while token.get_type() in AdditiveOperator.starting_token_types():
            self.operations.append((AdditiveOperator(lexer), MultiplicativeMathExpression(lexer)))
            token = lexer.peek()

    @classmethod
    def _starting_nodes(cls):
        return {MultiplicativeMathExpression}

    def get_children(self):
        return [self.first_expression] + [x for operation in self.operations for x in operation]

    def evaluate(self, environment):
        pass


class MultiplicativeMathExpression(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        self.first_expression = MathTerm(lexer)
        self.operations = []
        token = lexer.peek()
        while token.get_type() in MultiplicativeOperator.starting_token_types():
            self.operations.append((MultiplicativeOperator(lexer), MathTerm(lexer)))
            token = lexer.peek()

    @classmethod
    def _starting_nodes(cls):
        return {MathTerm}

    def get_children(self):
        return [self.first_expression] + [x for operation in self.operations for x in operation]

    def evaluate(self, environment):
        pass


class MathTerm(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        self.negation = None
        token = lexer.peek()
        if token.get_type() in MathNegationOperator.starting_token_types():
            self.negation = MathNegationOperator(lexer)
        token = lexer.peek()
        if token.get_type() in Value.starting_token_types():
            self.term = Value(lexer)
        elif token.get_type() in ParenthesisedExpression.starting_token_types():
            self.term = ParenthesisedExpression(lexer)
        else:
            self.make_error(token, self.starting_token_types(), lexer)

    @classmethod
    def _starting_nodes(cls):
        return {MathNegationOperator, Value, ParenthesisedExpression}

    def get_children(self):
        if self.negation is None:
            return [self.term]

        return [self.negation, self.term]

    def evaluate(self, environment):
        pass


class ParenthesisedExpression(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        LeftParenthesis(lexer)
        self.expression = Expression(lexer)
        RightParenthesis(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {LeftParenthesis}

    def get_children(self):
        return [self.expression]

    def evaluate(self, environment):
        pass


class AdditiveOperator(SwitchNode, BinaryEvaluable):
    @classmethod
    def _starting_nodes(cls):
        return {PlusOperator, MinusOperator}

    def evaluate(self, lhs, rhs, environment):
        pass


class PlusOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.PLUS

    def evaluate(self, lhs, rhs, environment):
        pass


class MinusOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.MINUS

    def evaluate(self, lhs, rhs, environment):
        pass


class MultiplicativeOperator(SwitchNode, BinaryEvaluable):
    @classmethod
    def _starting_nodes(cls):
        return {MultiplyOperator, DivisionOperator}

    def evaluate(self, lhs, rhs, environment):
        pass


class MultiplyOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.MULTIPLICATION

    def evaluate(self, lhs, rhs, environment):
        pass


class DivisionOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.DIVISION

    def evaluate(self, lhs, rhs, environment):
        pass


class OrOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.LOGICAL_OR

    def evaluate(self, lhs, rhs, environment):
        pass


class AndOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.LOGICAL_AND

    def evaluate(self, lhs, rhs, environment):
        pass


class EqualityOperator(SwitchNode, BinaryEvaluable):
    @classmethod
    def _starting_nodes(cls):
        return {EqualOperator, NotEqualOperator}

    def evaluate(self, lhs, rhs, environment):
        pass


class EqualOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.EQUALS

    def evaluate(self, lhs, rhs, environment):
        pass


class NotEqualOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.NOT_EQUALS

    def evaluate(self, lhs, rhs, environment):
        pass


class RelationOperator(SwitchNode, BinaryEvaluable):
    @classmethod
    def _starting_nodes(cls):
        return {GreaterOperator, GreaterOrEqualOperator, LessOperator, LessOrEqualOperator}

    def evaluate(self, lhs, rhs, environment):
        pass


class GreaterOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.GREATER

    def evaluate(self, lhs, rhs, environment):
        pass


class GreaterOrEqualOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.GREATER_OR_EQUAL

    def evaluate(self, lhs, rhs, environment):
        pass


class LessOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.LESS

    def evaluate(self, lhs, rhs, environment):
        pass


class LessOrEqualOperator(LeafNode, BinaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.LESS_OR_EQUAL

    def evaluate(self, lhs, rhs, environment):
        pass


class MathNegationOperator(LeafNode, UnaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.MINUS

    def evaluate(self, rhs, environment):
        pass


class LogicNegationOperator(LeafNode, UnaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.NOT

    def evaluate(self, rhs, environment):
        pass


class TimeUnit(SwitchNode, UnaryEvaluable):
    @classmethod
    def _starting_nodes(cls):
        return {Years, Months, Weeks, Days, Hours, Minutes, Seconds}

    def evaluate(self, rhs, environment):
        pass


class Years(LeafNode, UnaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.YEARS

    def evaluate(self, rhs, environment):
        pass


class Months(LeafNode, UnaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.MONTHS

    def evaluate(self, rhs, environment):
        pass


class Weeks(LeafNode, UnaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.WEEKS

    def evaluate(self, rhs, environment):
        pass


class Days(LeafNode, UnaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.DAYS

    def evaluate(self, rhs, environment):
        pass


class Hours(LeafNode, UnaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.HOURS

    def evaluate(self, rhs, environment):
        pass


class Minutes(LeafNode, UnaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.MINUTES

    def evaluate(self, rhs, environment):
        pass


class Seconds(LeafNode, UnaryEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.SECONDS

    def evaluate(self, rhs, environment):
        pass


class Value(SwitchNode, SelfEvaluable):
    @classmethod
    def _starting_nodes(cls):
        return {Literal, IdentifierFirstValue}

    def evaluate(self, environment):
        pass


class Literal(SwitchNode, SelfEvaluable):
    @classmethod
    def _starting_nodes(cls):
        return {NumberLiteral, StringLiteral, DateLiteral, TimeLiteral, DateTimeLiteral, TimedeltaLiteral}

    def evaluate(self, environment):
        pass


class NumberLiteral(LeafNode, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.NUMBER_LITERAL

    def evaluate(self, environment):
        pass


class StringLiteral(LeafNode, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.STRING_LITERAL

    def evaluate(self, environment):
        pass


class DateLiteral(LeafNode, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.DATE_LITERAL

    def evaluate(self, environment):
        pass


class TimeLiteral(LeafNode, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.TIME_LITERAL

    def evaluate(self, environment):
        pass


class DateTimeLiteral(LeafNode, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.DATETIME_LITERAL

    def evaluate(self, environment):
        pass


class TimedeltaLiteral(LeafNode, SelfEvaluable):
    @classmethod
    def token_type(cls):
        return tokens.TokenType.TIMEDELTA_LITERAL

    def evaluate(self, environment):
        pass


class IdentifierFirstValue(BaseNode, SelfEvaluable):
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

    def evaluate(self, environment):
        pass


class FunctionCall(BaseNode, SelfEvaluable):
    def __init__(self, lexer,
                 identifier):  # have to pass identifier as it was already parsed above (because of ambiguity)
        self.identifier = identifier
        self.parameters = ParametersCall(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {ParametersCall}

    def get_children(self):
        return [self.identifier, self.parameters]

    def evaluate(self, environment):
        pass


class ParametersCall(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        LeftParenthesis(lexer)
        self.parameters = []
        token = lexer.peek()
        if token.get_type() in Expression.starting_token_types():
            self.parameters.append(Expression(lexer))
            token = lexer.peek()
            while token.get_type() in Comma.starting_token_types():
                Comma(lexer)
                self.parameters.append(Expression(lexer))
                token = lexer.peek()
        RightParenthesis(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {LeftParenthesis}

    def get_children(self):
        return self.parameters

    def evaluate(self, environment):
        pass


class TimeInfoAccess(BaseNode, SelfEvaluable):
    def __init__(self, lexer,
                 identifier):  # have to pass identifier as it was already parsed above (because of ambiguity)
        self.identifier = identifier
        Access(lexer)
        self.time_unit = TimeUnit(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {Access}

    def get_children(self):
        return [self.identifier, self.time_unit]

    def evaluate(self, environment):
        pass
