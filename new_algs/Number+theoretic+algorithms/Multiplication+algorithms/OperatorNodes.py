from Node import Node

class OperatorNode(Node):
    def __init__(self):
        self.l = None
        self.r = None

    def isOperator(self):
        return(True)

    def evaluate(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def __str__(self):
        raise NotImplementedError("Subclass must implement abstract method")


class AdditionNode(OperatorNode):
    def evaluate(self):
        return(self.l.evaluate() + self.r.evaluate())
    def __str__(self):
        return('+')

class SubtractionNode(OperatorNode):
    def evaluate(self):
        return(self.l.evaluate() - self.r.evaluate())
    def __str__(self):
        return('-')

class MultiplicationNode(OperatorNode):
    def evaluate(self):
        return(self.l.evaluate() * self.r.evaluate())
    def __str__(self):
        return('*')

class DivisionNode(OperatorNode):
    def evaluate(self):
        return(self.l.evaluate() / self.r.evaluate())
    def __str__(self):
        return('/')
