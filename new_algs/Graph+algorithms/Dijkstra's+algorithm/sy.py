from enum import Enum
import random

class TokenType(Enum):
	NUMBER		   = 0
	OPERATOR	   = 1
	OPEN_PAREN	   = 2
	CLOSE_PAREN	   = 3

class OperatorType(Enum):
	ADD = 0,
	SUB = 1,
	MUL = 2,
	DIV = 3,

op_strings = ('+', '-', '*', '/')

op_prec = {
	OperatorType.MUL : 3,
	OperatorType.DIV : 3,
	OperatorType.ADD : 2,
	OperatorType.SUB : 2,
	TokenType.OPEN_PAREN: 1,
}

class Token:
	def __init__(self, token_type, value=None, op_type=None):
		self.token_type = token_type
		self.value = value
		self.op_type = op_type
		if self.token_type != TokenType.NUMBER and \
		   value != None:
			print("Token is not of type NUMBER but was given value anyway")
			exit()
		if self.token_type != TokenType.OPERATOR and \
		   op_type != None:
			print("Token is not of type OPERATOR but was given op_type anyway")
			exit()
	def __str__(self):
		if	 self.token_type == TokenType.NUMBER:
			return "{0}: {1}".format(self.token_type, self.value)
		elif self.token_type == TokenType.OPERATOR:
			return "{0}: {1}".format(self.token_type, self.op_type)
		else:
			return str(self.token_type)

def tokenize(string):
	tokens = []
	i = 0
	while True:
		if i >= len(string):
			break
		c = string[i]
		if	 c == '(':
			tokens.append(Token(TokenType.OPEN_PAREN))
		elif c == ')':
			tokens.append(Token(TokenType.CLOSE_PAREN))
		elif c == '+':
			tokens.append(Token(TokenType.OPERATOR, op_type=OperatorType.ADD))
		elif c == '-':
			tokens.append(Token(TokenType.OPERATOR, op_type=OperatorType.SUB))
		elif c == '*':
			tokens.append(Token(TokenType.OPERATOR, op_type=OperatorType.MUL))
		elif c == '/':
			tokens.append(Token(TokenType.OPERATOR, op_type=OperatorType.DIV))
		elif c == '.' or c.isdigit():
			digits = []
			while True:
				if i >= len(string):
					break
				if string[i] == '.' or string[i].isdigit():
					digits.append(string[i])
				else:
					i -= 1
					break
				i += 1
			tokens.append(Token(TokenType.NUMBER, value=float(''.join(digits))))
		i += 1
	return tokens

def shunting_yard(tokens):
	out = []
	stack = []
	for token in tokens:
		if	 token.token_type == TokenType.NUMBER:
			out.append(token.value)
		elif token.token_type == TokenType.OPERATOR:
			if len(stack) == 0 or \
			   op_prec[token.op_type] > op_prec[stack[-1]]:
				stack.append(token.op_type)
			else:
				while len(stack) > 0 and \
					  op_prec[token.op_type] <= op_prec[stack[-1]]:
					out.append(stack.pop())
				stack.append(token.op_type)
		elif token.token_type == TokenType.OPEN_PAREN:
			stack.append(TokenType.OPEN_PAREN)
		elif token.token_type == TokenType.CLOSE_PAREN:
			while stack[-1] != TokenType.OPEN_PAREN:
				out.append(stack.pop())
			stack.pop()
	while len(stack) > 0:
		out.append(stack.pop())
	return out

def rpn_evaluate(rpn):
	stack = []
	for element in rpn:
		if type(element) == OperatorType:
			a = stack.pop()
			b = stack.pop()
			if	 element == OperatorType.ADD:
				stack.append(b + a)
			elif element == OperatorType.SUB:
				stack.append(b - a)
			elif element == OperatorType.MUL:
				stack.append(b * a)
			elif element == OperatorType.DIV:
				stack.append(b / a)
		else:
			stack.append(element)
	return stack[-1]

def random_number():
	return str(round(random.random() * 50, 2))

def generate_test_expression():
	expr_len = random.randrange(2, 8)
	expr = [random_number()]
	paren_level = 0
	for i in range(expr_len):
		opened = False
		expr.append(op_strings[random.randrange(0, 4)])
		if random.randrange(0, 100) < 35:
			expr.append('(')
			paren_level += 1
			opened = True
		expr.append(random_number())
		if random.randrange(0, 100) < 60 \
		   and paren_level > 0 \
		   and not opened:
			expr.append(')')
			paren_level -= 1
	while paren_level > 0:
		expr.append(')')
		paren_level -= 1
	return ' '.join(expr)

def test_alg():
	for i in range(10000):
		expr = generate_test_expression()
		try:
			py_value = eval(expr)
		except ZeroDivisionError:
			continue
		my_value = rpn_evaluate(shunting_yard(tokenize(expr)))
		if py_value != my_value:
			print("Error with expression '{0}':\n  py_value: {1}\n	my_value: {2}" \
				  .format(expr, \
						  py_value, \
						  my_value))
			exit()

def main():
	print("Running tests...")
	test_alg()
	print("Everything looks a-ok")

def interactive():
	while True:
		inp = input('> ')
		if inp.lower() == 'quit' or inp.lower() == 'q':
			break
		val = rpn_evaluate(shunting_yard(tokenize(inp)))
		if val == int(val):
			val = int(val)
		print(val)
	
if __name__ == "__main__":
	main()
	interactive()
