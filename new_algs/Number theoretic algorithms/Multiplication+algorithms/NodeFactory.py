from calculator.Nodes.OperatorNodes import *
from calculator.Nodes.ValueNodes import *

class NodeFactory:
    def __is_realnumber(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def __is_complexnumber(self, s):
        try:
            complex(s)
            return True
        except ValueError:
            return False

    def generate(self, operation):
        if self.__is_realnumber(operation):
            return(RealNode(float(operation)))
        if operation is '+':
            return(AdditionNode())
        elif operation is '-':
            return(SubtractionNode())
        elif operation is '*':
            return(MultiplicationNode())
        elif operation is '/':
            return(DivisionNode())
