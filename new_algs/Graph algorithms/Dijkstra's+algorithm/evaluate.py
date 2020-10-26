import sys
from postfix import evaluate_postfix, parse_expression_into_parts
from stack import Stack

PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 0, ')': 0}


def infix_parts_to_postfix(terms):
    raise NotImplementedError("complete me!")


def evaluate_infix(terms):
    return evaluate_postfix(infix_parts_to_postfix(terms))


def evaluate_infix_str(exp):
    return evaluate_infix(parse_expression_into_parts(exp))


if __name__ == "__main__":
    expr = None
    if len(sys.argv) > 1:
        expr = sys.argv[1]
        print "Evaluating %s == %s" % (expr, evaluate_infix_str(expr))
    else:
        print 'Usage: python evaluate.py "<expr>" -- i.e. python evaluate.py 9 - ( 1 + 3 ) * 2'
        print "Spaces are required between every term, even parenthesis."

