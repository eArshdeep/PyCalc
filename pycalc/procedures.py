from pycalc.definitions import *
import re


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


def handle_neg(tokens):
    """" convert minus operator in tokens that should be unary negative """
    for i, token in enumerate(tokens):
        if token == '-':
            if i == 0:
                tokens[i] = 'NEG'
            elif type(tokens[i - 1]) == str and tokens[i - 1] != ")":
                tokens[i] = 'NEG'
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
            curOp = operators[token]
            stkOp = operators[operator_stack[-1]] if operator_stack else None
            while (operator_stack and operator_stack[-1] != "(") and \
                    (stkOp.precedence > curOp.precedence or
                     (stkOp.precedence == curOp.precedence and
                      curOp.associativity == Associativity.LEFT)):
                output.append(operator_stack.pop())
                stkOp = operators[operator_stack[-1]] if operator_stack else None
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
            if operators[token].arity == Arity.BINARY:
                if len(operands) < 2:
                    raise Exception("BinOp_TooFewOperands")
                operand2 = operands.pop()
                operand1 = operands.pop()
                operands.append(operators[token].operation(operand1, operand2))
            else:
                if not operands:
                    raise Exception("UnaryOp_TooFewOperands")
                operands.append(operators[token].operation(operands.pop()))
    return operands.pop()


def evaluate(expression, verbose=False):
    tokens = tokenize(expression)
    negatedTokens = handle_neg(tokens)
    rpn = infix_to_postfix(negatedTokens)
    result = postfix_solver(rpn)

    if verbose:
        x = "{: >15}"
        print(x.format("Expression:"), expression)
        print(x.format("Initial Tokens:"), tokens)
        print(x.format("Final Tokens:"), negatedTokens)
        print(x.format("Postfix:"), rpn)
        print(x.format("Result :"), result)

    return result
