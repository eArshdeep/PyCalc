import re
import operator
from enum import Enum
from collections.abc import Callable


class Associativity(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    BOTH = 3


class Operator:
    def __init__(self, name: str, associativity: Associativity, precedence: int, operation: Callable):
        self.name = name
        self.associativity = associativity
        self.precedence = precedence
        self.operation = operation


operators = {
    "+": Operator("+", Associativity.LEFT, 2, operator.add),
    "-": Operator("-", Associativity.LEFT, 2, operator.sub),
    "*": Operator("*", Associativity.LEFT, 3, operator.mul),
    "/": Operator("/", Associativity.LEFT, 3, operator.truediv),
    "^": Operator("^", Associativity.RIGHT, 4, operator.pow)
}

rep_split_expr = "[0-9]+[.]?[0-9]*"
for key in operators.keys():
    rep_split_expr += f"|[\\{key}]"
rep_split_expr += "|[(|)]"


def tokenize(expression):
    tokens = expression.split()

    i = 0
    while i < len(tokens):
        sub_tokens = re.findall(rep_split_expr, tokens[i])
        for x, sub_token in enumerate(sub_tokens):
            if sub_token.isnumeric():
                sub_tokens[x] = int(sub_token)
        tokens[i:i + 1] = sub_tokens
        i += len(sub_tokens)

    return tokens


def infix_to_postfix(tokens):
    """ shunting yard algorithm """
    operator_stack = []
    output = []

    for token in tokens:
        if type(token) == int:
            output.append(token)
        elif token == "(":
            operator_stack.append(token)
        elif token == ")":
            while operator_stack:
                if operator_stack[-1] == "(":
                    break
                output.append(operator_stack.pop())
            if operator_stack:
                operator_stack.pop()
            else:
                raise Exception("ParenthesesMismatch")
        else:
            while (operator_stack and operator_stack[-1] != "(") \
                    and (operators[operator_stack[-1]].precedence > operators[token].precedence or
                         (operators[operator_stack[-1]].precedence == operators[token].precedence and
                          operators[token].associativity == Associativity.LEFT)):
                output.append(operator_stack.pop())
            operator_stack.append(token)

    while operator_stack:
        output.append(operator_stack.pop())

    return output


def postfix_solver(tokens):
    operands = []

    for token in tokens:
        if type(token) == int:
            operands.append(token)
        else:
            if len(operands) < 2:
                raise Exception("BinOp_TooFewOperands")
            operand2 = operands.pop()
            operand1 = operands.pop()
            operands.append(operators[token].operation(operand1, operand2))
    return operands.pop()
