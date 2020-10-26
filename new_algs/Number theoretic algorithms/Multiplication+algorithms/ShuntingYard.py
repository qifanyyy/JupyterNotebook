from Stack import OperatorStack, OutputStack

# According to wikipedia description
# https://en.wikipedia.org/wiki/Shunting-yard_algorithm

class ShuntingYard:
    isLeftAssociative = {}
    isLeftAssociative['+'] = True
    isLeftAssociative['-'] = True
    isLeftAssociative['*'] = True
    isLeftAssociative['/'] = True
    isLeftAssociative['exp'] = True
    isLeftAssociative['('] = False
    isLeftAssociative[')'] = False


    def __init__(self, operations):
        self.precedence = {'+': 1, '-': 1, '/': 2, '*': 2,'exp': 3, '(': 0,')': 0 }

        self.operations = operations

        self.evaluate()


    def evaluate(self):
        self.__algorithmShuntingYard()

    def __is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def __isOperator(self, stack, operators):
        if len(stack) == 0:
            return(False)
        return(stack[-1] in operators)

    def __algorithmShuntingYard(self):
        operatorSet = '\+\-\*\/'
        outputStack = OutputStack()
        operatorStack = OperatorStack(operatorSet)

        i = 0
        while i < len(self.operations):
            token = self.operations[i]
            if self.__is_number(token):
                outputStack.push(token)

            """	if the token is an operator, then:"""
            if token in operatorSet:
                """
                while there is an operator at the top of the operator stack with
                greater than or equal to precedence and the operator is left associative:
                    pop operators from the operator stack, onto the output queue.
                """
                while self.__isOperator(operatorStack, operatorSet) and \
                    self.precedence[operatorStack[-1]] >= self.precedence[token] and \
                    self.isLeftAssociative[operatorStack[-1]]:
                        outputStack.push(operatorStack.pop())
                """push the read operator onto the operator stack."""
                operatorStack.append(token)
            if token in '(':
                operatorStack.append(token)
            if token in ')':
                while operatorStack and not operatorStack[len(operatorStack) - 1] in '(':
                    outputStack.append(operatorStack.pop())
                operatorStack.pop()
            i+= 1
        if i == len(self.operations):
            while operatorStack:
                outputStack.append(operatorStack.pop())
        self.stack = outputStack
        return(self.stack)
