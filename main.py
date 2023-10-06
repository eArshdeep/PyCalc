import src.lib as asp

expression = "(0-1)+1"
print("Input:", expression)

tokens = asp.tokenize(expression)
print("Token Input:", tokens)

rpn = asp.infix_to_postfix(tokens)
print("Polish Representation:", rpn)

result = asp.postfix_solver(rpn)
print("Result:", result)
