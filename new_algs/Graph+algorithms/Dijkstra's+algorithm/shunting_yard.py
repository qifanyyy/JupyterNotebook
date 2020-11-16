from stack_queue import Stack, Queue
import operator


class Operator:

    """A mathematical operator or function (e.g., "+", "max")."""

    def __init__(self, symbol, precedence, arity=None, associativity=None, actual_function=None):

        """
        :parameter symbol: a non alphabetical character. Should be unique among Operators (and Functions).
        :parameter precedence: positive integer representing operator evaluation precedence.
        :parameter arity: number of parameters the operator takes.
        :parameter associativity: should be "left" or "right". Denotes the associativity type of the operator.
        :parameter actual_function: python function with <arity> parameters used to evaluate expressions.
        """

        self.symbol = symbol
        self.precedence = precedence
        self.arity = arity
        self.associativity = associativity
        self.actual_function = actual_function

    def __eq__(self, other):

        """:parameter other: Operator or string."""

        return self.symbol == other.symbol if type(other) == Operator else self.symbol == other

    def __ge__(self, other):

        """Compares operators arities."""

        return self.precedence >= other.precedence

    def __str__(self):

        return self.symbol


class ShuntingYard:

    def __init__(self, operators=(), load_basic=True):

        """
        :parameter operators: dictionary of operators with their symbols as keys.
        :parameter load_basic: boolean indicating whether to load basic functions and operators.
        """

        self.operators = {op.symbol: op for op in operators}

        if load_basic:
            self._load_basic()

    def parse(self, expression):

        """
        Converts an infix mathematical expression into a postfix one using the Shunting Yard Algorithm.
        :parameter expression: string representing a mathematical infix expression.
        :returns: a queue with the tokens ordered in Reverse Polish Notation (postfix notation).
        """

        input_tokens = self._tokenize(expression)
        output_tokens = Queue()
        operator_stack = Stack()

        while input_tokens:
            token = input_tokens.pull()
            if self._is_number(token):  # If the token is a number
                output_tokens.push(token)
            if token in self.operators:  # If the token is an operator
                next_op = operator_stack.view_next()
                while next_op in self.operators and self.operators[next_op] >= self.operators[token] and \
                        self.operators[token].associativity == "left":
                    output_tokens.push(operator_stack.pull())
                    next_op = operator_stack.view_next()
                operator_stack.push(token)
            if token is '(':
                operator_stack.push(token)
            if token is ')' or token is ',':
                while operator_stack.view_next() and operator_stack.view_next() is not '(':
                    output_tokens.push(operator_stack.pull())
                if token is ')':
                    operator_stack.pull()  # Pull the left bracket
        while operator_stack:
            output_tokens.push(operator_stack.pull())

        return output_tokens

    def evaluate(self, postfix_tokens):

        """
        Evaluates a postfix expression and returns its value.
        :parameter postfix_tokens: queue, as returned by the parse function of this class
        """

        result_stack = Stack()
        operation_stack = Stack()

        while postfix_tokens:
            token = postfix_tokens.pull()
            if token in self.operators:
                op = self.operators[token]
                for operand in range(op.arity):
                    operation_stack.push(result_stack.pull())
                result_stack.push(op.actual_function(*(float(operation_stack.pull()) for operand in range(op.arity))))

            else:
                result_stack.push(token)

        return result_stack.pull()

    def _load_basic(self):

        """Loads basic operators and functions for the algorithm to recognize in expressions."""

        basic_ops = (Operator('+', 2, 2, "left", operator.add),
                     Operator('-', 2, 2, "left", operator.sub),
                     Operator('*', 3, 2, "left", operator.mul),
                     Operator('/', 3, 2, "left", operator.truediv),
                     Operator('^', 4, 2, "right", operator.pow),
                     Operator('max', 5, 2, actual_function=max),
                     Operator('min', 5, 2, actual_function=min))
        self.operators.update({op.symbol: op for op in basic_ops})

    @staticmethod
    def _tokenize(expression):

        """
        Parses an expression into tokens for the Shunting Yard Algorithm. Behaves indefinitely for ill written and non
        infix expressions.
        :parameter expression: string containing an infix mathematical expression.
        :returns: a queue with the tokens.
        """

        expression = ''.join(expression.split())  # remove whitespace, probably inefficient
        tokens = Queue()  # Input tokens for the Shunting Yard

        token_index = 0
        char_index = 0
        # Each loop of this while loop processes one token
        while char_index < len(expression):
            token_start_char = expression[token_index]  # The first character of the token

            if token_start_char.isdigit():  # If the token is a number
                while char_index < len(expression) and \
                        (expression[char_index].isdigit() or
                         expression[char_index] is '.'):
                    char_index += 1
            elif token_start_char.isalpha():  # If the token is a function (no numbers are allowed for functions)
                while char_index < len(expression) and expression[char_index].isalpha():
                    char_index += 1
            else:  # If the character is a single character operator
                char_index += 1

            tokens.push(expression[token_index: char_index])  # Add the found token to the queue

            token_index = char_index
        return tokens

    @staticmethod
    def _is_number(string):

        """Helper method for the algorithm (parse function)."""

        try:
            float(string)
        except ValueError:
            return False
        else:
            return True
