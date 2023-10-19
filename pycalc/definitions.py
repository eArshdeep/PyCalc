import operator
from enum import Enum
from collections.abc import Callable


class Associativity(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    BOTH = 3


class Arity:
    NONE = 0
    UNARY = 1
    BINARY = 2


def nop():
    """ no operation """
    return


def neg(a):
    """ return negative of `a` """
    return -a


class Operator:
    def __init__(self, name: str, associativity: Associativity, precedence: int,
                 operation: Callable, arity=Arity.BINARY):
        self.name = name
        self.associativity = associativity
        self.precedence = precedence
        self.operation = operation
        self.arity = arity


operators = {
    "+": Operator("+", Associativity.LEFT, 1, operator.add),
    "-": Operator("-", Associativity.LEFT, 1, operator.sub),
    "*": Operator("*", Associativity.LEFT, 2, operator.mul),
    "/": Operator("/", Associativity.LEFT, 2, operator.truediv),
    "^": Operator("^", Associativity.RIGHT, 3, operator.pow),
    "(": Operator("(", Associativity.NONE, 0, nop, arity=Arity.NONE),
    ")": Operator(")", Associativity.NONE, 0, nop, arity=Arity.NONE),
    "NEG": Operator("NEG", Associativity.RIGHT, 2, neg, arity=Arity.UNARY)
}

rep_split_expr = "\\d+\\.?\\d*|[+|\\-|\\*|\\/|\\(|\\)|\\^]"
""" Extract numbers and operators from string. Ignores whitespace. """
rep_is_float = "\\d+\\.\\d*"
""" Check if string is valid float. """


def isnumeric(a: any) -> bool:
    """ Return truthy indicating `a` is an integer or float """
    t = type(a)
    return t == int or t == float
