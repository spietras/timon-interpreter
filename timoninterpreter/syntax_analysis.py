"""

Syntax analysis module

"""

from abc import ABC, abstractmethod

from timoninterpreter import tokens


class BaseNode(ABC):
    """
    Node base class
    """

    def __init__(self):
        self.children = []

    def _add_child(self, node):
        self.children.append(node)

    @classmethod
    def starting_token_types(cls):
        """
        Get token types that this rule can start with

        Returns:
            List of token types
        """
        return {t for n in cls._starting_nodes() for t in n.starting_token_types()}

    @classmethod
    @abstractmethod
    def _starting_nodes(cls):
        pass


class SwitchNode(BaseNode, ABC):
    def __init__(self, lexer):
        super().__init__()
        token = lexer.peek()

        for node in self._starting_nodes():
            if token.type in node.starting_token_types():
                self._add_child(node(lexer))
                return

        raise ValueError  # TODO: error


class LeafNode(BaseNode, ABC):
    def __init__(self, lexer):
        super().__init__()
        self.token = lexer.peek()
        if self.token.type != self.token_type():
            raise ValueError  # TODO: error
        lexer.get()

    @classmethod
    @abstractmethod
    def token_type(cls):
        pass

    @classmethod
    def starting_token_types(cls):
        return {cls.token_type()}

    @classmethod
    def _starting_nodes(cls):
        return None


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
        super().__init__()
        token = lexer.peek()
        while token.type != tokens.TokenType.END:
            if token.type in NonNestableStatement.starting_token_types():
                self._add_child(NonNestableStatement(lexer))
            elif token.type in NestableStatement.starting_token_types():
                self._add_child(NestableStatement(lexer))
            else:
                raise ValueError  # TODO: error

            token = lexer.peek()

    @classmethod
    def _starting_nodes(cls):
        return {NonNestableStatement, NestableStatement}

    def execute(self, environment):
        pass


class NonNestableStatement(BaseNode, Executable):
    def __init__(self, lexer):
        super().__init__()
        self._add_child(FunctionDefinitionStatement(lexer))
        Semicolon(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {FunctionDefinitionStatement}

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
        super().__init__()
        identifier = Identifier(lexer)
        token = lexer.peek()
        if token.type in FunctionCall.starting_token_types():
            self._add_child(FunctionCall(lexer, identifier))
        elif token.type in VariableAssignmentStatement.starting_token_types():
            self._add_child(VariableAssignmentStatement(lexer, identifier))
        else:
            raise ValueError  # TODO: error

    @classmethod
    def _starting_nodes(cls):
        return {Identifier}

    def execute(self, environment):
        pass


class VariableAssignmentStatement(BaseNode, Executable):
    def __init__(self, lexer, identifier):
        super().__init__()
        self._add_child(identifier)
        Assign(lexer)
        self._add_child(MathExpression(lexer))

    @classmethod
    def _starting_nodes(cls):
        return {Assign}

    def execute(self, environment):
        pass


class FunctionDefinitionStatement(BaseNode, Executable):
    def __init__(self, lexer):
        super().__init__()
        FunKeyword(lexer)
        self._add_child(Identifier(lexer))
        self._add_child(ParametersDeclaration(lexer))
        self._add_child(Body(lexer))

    @classmethod
    def _starting_nodes(cls):
        return {FunKeyword}

    def execute(self, environment):
        pass


class VariableDefinitionStatement(BaseNode, Executable):
    def __init__(self, lexer):
        super().__init__()
        VarKeyword(lexer)
        self._add_child(Identifier(lexer))
        token = lexer.peek()
        if token.type in VariableAssignmentStatement.starting_token_types():
            self._add_child(VariableAssignmentStatement(lexer, self.children[0]))

    @classmethod
    def _starting_nodes(cls):
        return {VarKeyword}

    def execute(self, environment):
        pass


class IfStatement(BaseNode, Executable):
    def __init__(self, lexer):
        super().__init__()
        IfKeyword(lexer)
        self._add_child(LogicExpression(lexer))
        self._add_child(Body(lexer))
        token = lexer.peek()
        if token.type in ElseKeyword.starting_token_types():
            ElseKeyword(lexer)
            self._add_child(Body(lexer))

    @classmethod
    def _starting_nodes(cls):
        return {IfKeyword}

    def execute(self, environment):
        pass


class FromStatement(BaseNode, Executable):
    def __init__(self, lexer):
        super().__init__()
        FromKeyword(lexer)
        self._add_child(FromRange(lexer))
        self._add_child(FromStep(lexer))
        self._add_child(FromIterator(lexer))
        self._add_child(Body(lexer))

    @classmethod
    def _starting_nodes(cls):
        return {FromKeyword}

    def execute(self, environment):
        pass


class PrintStatement(BaseNode, Executable):
    def __init__(self, lexer):
        super().__init__()
        PrintKeyword(lexer)
        self._add_child(MathExpression(lexer))

    @classmethod
    def _starting_nodes(cls):
        return {PrintKeyword}

    def execute(self, environment):
        pass


class ReturnStatement(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        ReturnKeyword(lexer)
        self._add_child(MathExpression(lexer))

    @classmethod
    def _starting_nodes(cls):
        return {ReturnKeyword}

    def evaluate(self, environment):
        pass


class ParametersDeclaration(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        LeftParenthesis(lexer)
        token = lexer.peek()
        if token.type in Identifier.starting_token_types():
            self._add_child(Identifier(lexer))
            token = lexer.peek()
            while token.type in Comma.starting_token_types():
                Comma(lexer)
                self._add_child(Identifier(lexer))
                token = lexer.peek()
        RightParenthesis(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {LeftParenthesis}

    def evaluate(self, environment):
        pass


class Body(BaseNode, Executable):
    def __init__(self, lexer):
        super().__init__()
        LeftBracket(lexer)
        token = lexer.peek()
        while token.type in NestableStatement.starting_token_types():
            self._add_child(NestableStatement(lexer))
            token = lexer.peek()
        RightBracket(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {LeftBracket}

    def execute(self, environment):
        pass


class FromRange(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        self._add_child(MathExpression(lexer))
        ToKeyword(lexer)
        self._add_child(MathExpression(lexer))

    @classmethod
    def _starting_nodes(cls):
        return {MathExpression}

    def evaluate(self, environment):
        pass


class FromStep(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        ByKeyword(lexer)
        self._add_child(TimeUnit(lexer))

    @classmethod
    def _starting_nodes(cls):
        return {ByKeyword}

    def evaluate(self, environment):
        pass


class FromIterator(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        AsKeyword(lexer)
        self._add_child(Identifier(lexer))

    @classmethod
    def _starting_nodes(cls):
        return {AsKeyword}

    def evaluate(self, environment):
        pass


class MathExpression(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        self._add_child(MultiplicativeMathExpression(lexer))
        token = lexer.peek()
        while token.type in AdditiveOperator.starting_token_types():
            self._add_child(AdditiveOperator(lexer))
            self._add_child(MultiplicativeMathExpression(lexer))
            token = lexer.peek()

    @classmethod
    def _starting_nodes(cls):
        return {MultiplicativeMathExpression}

    def evaluate(self, environment):
        pass


class MultiplicativeMathExpression(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        self._add_child(MathTerm(lexer))
        token = lexer.peek()
        while token.type in MultiplicativeOperator.starting_token_types():
            self._add_child(MultiplicativeOperator(lexer))
            self._add_child(MathTerm(lexer))
            token = lexer.peek()

    @classmethod
    def _starting_nodes(cls):
        return {MathTerm}

    def evaluate(self, environment):
        pass


class MathTerm(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        token = lexer.peek()
        if token.type in MathNegationOperator.starting_token_types():
            self._add_child(MathNegationOperator(lexer))
        token = lexer.peek()
        if token.type in Value.starting_token_types():
            self._add_child(Value(lexer))
        elif token.type in ParenthesisedMathExpression.starting_token_types():
            self._add_child(ParenthesisedMathExpression(lexer))
        else:
            raise ValueError  # TODO: error

    @classmethod
    def _starting_nodes(cls):
        return {MathNegationOperator, Value, ParenthesisedMathExpression}

    def evaluate(self, environment):
        pass


class ParenthesisedMathExpression(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        LeftParenthesis(lexer)
        self._add_child(MathExpression(lexer))
        RightParenthesis(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {LeftParenthesis}

    def evaluate(self, environment):
        pass


class LogicExpression(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        self._add_child(LogicAndExpression(lexer))
        token = lexer.peek()
        while token.type in OrOperator.starting_token_types():
            self._add_child(OrOperator(lexer))
            self._add_child(LogicAndExpression(lexer))
            token = lexer.peek()

    @classmethod
    def _starting_nodes(cls):
        return {LogicAndExpression}

    def evaluate(self, environment):
        pass


class LogicAndExpression(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        self._add_child(LogicEqualityExpression(lexer))
        token = lexer.peek()
        while token.type in AndOperator.starting_token_types():
            self._add_child(AndOperator(lexer))
            self._add_child(LogicEqualityExpression(lexer))
            token = lexer.peek()

    @classmethod
    def _starting_nodes(cls):
        return {LogicEqualityExpression}

    def evaluate(self, environment):
        pass


class LogicEqualityExpression(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        self._add_child(LogicRelationalExpression(lexer))
        token = lexer.peek()
        if token.type in EqualityOperator.starting_token_types():
            self._add_child(EqualityOperator(lexer))
            self._add_child(LogicRelationalExpression(lexer))

    @classmethod
    def _starting_nodes(cls):
        return {LogicRelationalExpression}

    def evaluate(self, environment):
        pass


class LogicRelationalExpression(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        self._add_child(LogicTerm(lexer))
        token = lexer.peek()
        if token.type in RelationOperator.starting_token_types():
            self._add_child(RelationOperator(lexer))
            self._add_child(LogicTerm(lexer))

    @classmethod
    def _starting_nodes(cls):
        return {LogicTerm}

    def evaluate(self, environment):
        pass


class LogicTerm(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        token = lexer.peek()
        if token.type in LogicNegationOperator.starting_token_types():
            self._add_child(LogicNegationOperator(lexer))
        token = lexer.peek()
        if token.type in MathExpression.starting_token_types():
            self._add_child(MathExpression(lexer))
        elif token.type in ParenthesisedLogicExpression.starting_token_types():
            self._add_child(ParenthesisedLogicExpression(lexer))
        else:
            raise ValueError  # TODO: error

    @classmethod
    def _starting_nodes(cls):
        return {LogicNegationOperator, MathExpression, ParenthesisedLogicExpression}

    def evaluate(self, environment):
        pass


class ParenthesisedLogicExpression(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        LeftParenthesis(lexer)
        self._add_child(LogicExpression(lexer))
        RightParenthesis(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {LeftParenthesis}

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
        super().__init__()
        identifier = Identifier(lexer)
        token = lexer.peek()
        if token.type in FunctionCall.starting_token_types():
            self._add_child(FunctionCall(lexer, identifier))
        elif token.type in TimeInfoAccess.starting_token_types():
            self._add_child(TimeInfoAccess(lexer, identifier))
        else:
            self._add_child(identifier)

    @classmethod
    def _starting_nodes(cls):
        return {Identifier}

    def evaluate(self, environment):
        pass


class FunctionCall(BaseNode, SelfEvaluable):
    def __init__(self, lexer, identifier):
        super().__init__()
        self._add_child(identifier)
        self._add_child(ParametersCall(lexer))

    @classmethod
    def _starting_nodes(cls):
        return {ParametersCall}

    def evaluate(self, environment):
        pass


class ParametersCall(BaseNode, SelfEvaluable):
    def __init__(self, lexer):
        super().__init__()
        LeftParenthesis(lexer)
        token = lexer.peek()
        if token.type in MathExpression.starting_token_types():
            self._add_child(MathExpression(lexer))
            token = lexer.peek()
            while token.type in Comma.starting_token_types():
                Comma(lexer)
                self._add_child(MathExpression(lexer))
                token = lexer.peek()
        RightParenthesis(lexer)

    @classmethod
    def _starting_nodes(cls):
        return {LeftParenthesis}

    def evaluate(self, environment):
        pass


class TimeInfoAccess(BaseNode, SelfEvaluable):
    def __init__(self, lexer, identifier):
        super().__init__()
        self._add_child(identifier)
        Access(lexer)
        self._add_child(TimeUnit(lexer))

    @classmethod
    def _starting_nodes(cls):
        return {Access}

    def evaluate(self, environment):
        pass
