import unittest

from calculator.Formular.Formular import *

from calculator.Nodes.Node import Node
from calculator.Nodes.ValueNodes import *
from calculator.Nodes.OperatorNodes import *
from calculator.Nodes.NodeFactory import NodeFactory
from calculator.Nodes.ExpressionTree import ExpressionTree

from calculator.ShuntingYard.ShuntingYard import ShuntingYard
from calculator.ShuntingYard.Stack import Stack

from Calculator import Calculator


class TestFormular(unittest.TestCase):
    def testFormular(self):
        formular = Formular("5 + 3")
        self.assertEqual(formular.operations, list('5+3'))

class TestShuntingYard(unittest.TestCase):
    def testStack(self):
        st1 = Stack()
        st1.push('5')
        st1.pop()

    def testShuntingYardCall(self):
        sh = ShuntingYard(list('5+3'))
        sh.evaluate()
        self.assertEqual(sh.stack, list('53+'))

    def testShuntingYardAddition(self):
        formular = Formular("5 + 3")
        sh = ShuntingYard(formular.operations)
        sh.evaluate()
        self.assertEqual(sh.stack, list('53+'))

    def testShuntingYardSubtraction(self):
        formular = Formular("8 - 3")
        sh = ShuntingYard(formular.operations)
        sh.evaluate()
        self.assertEqual(sh.stack, list('83-'))

    def testShuntingYardMultiplication(self):
        formular = Formular("5 * 4")
        sh = ShuntingYard(formular.operations)
        sh.evaluate()
        self.assertEqual(sh.stack, list('54*'))

    def testShuntingYardDivision(self):
        formular = Formular("8 / 3")
        sh = ShuntingYard(formular.operations)
        sh.evaluate()
        self.assertEqual(sh.stack, list('83/'))

    def testShuntingYardMultiAddition(self):
        formular = Formular("5 + 3 + 8")
        sh = ShuntingYard(formular.operations)
        sh.evaluate()
        self.assertEqual(sh.stack, list('53+8+'))

    def testShuntingYardAdditionMultiplication(self):
        formular = Formular("5 + 3 * 8")
        sh = ShuntingYard(formular.operations)
        sh.evaluate()
        self.assertEqual(sh.stack, list('538*+'))

    def testShuntingYardParanthesis(self):
        formular = Formular("(5 + 3) * 8")
        sh = ShuntingYard(formular.operations)
        sh.evaluate()
        self.assertEqual(sh.stack,list('53+8*'))

    def testShuntingYardAllOperations(self):
        math = "1 + 2 - 3 * 4 / (5 + (6 - 7)) "
        formular = Formular(math)
        sh = ShuntingYard(formular.operations)
        sh.evaluate()

        self.assertEqual(sh.stack, list('12+34*567-+/-'))

class TestCalculatorNodes(unittest.TestCase):
    def testValueNode(self):
        int1 = 5
        v1 = RealNode(int1)
        self.assertEqual(v1.evaluate(), int1)

    def testAddition(self):
        nodeOp = AdditionNode()
        nodeOp.l=RealNode(5)
        nodeOp.r=RealNode(3)
        self.assertEqual(nodeOp.evaluate(),5+3)

    def testSubtraction(self):
        nodeOp = SubtractionNode()
        nodeOp.l=RealNode(5)
        nodeOp.r=RealNode(3)
        self.assertEqual(nodeOp.evaluate(),5-3)

    def testMultiplication(self):
        nodeOp = MultiplicationNode()
        nodeOp.l=RealNode(5)
        nodeOp.r=RealNode(3)
        self.assertEqual(nodeOp.evaluate(),5*3.0)

    def testDivision(self):
        nodeOp = DivisionNode()
        nodeOp.l=RealNode(5)
        nodeOp.r=RealNode(3)
        self.assertEqual(nodeOp.evaluate(),5/3.0)

class TestNodeFactory(unittest.TestCase):
    def testRealNodeInteger(self):
        nodeFactory = NodeFactory()
        operation = 5
        node1 = nodeFactory.generate(operation)
        node2 = RealNode(float(operation))
        self.assertEqual(node1.evaluate(), node2.evaluate())

    def testRealNodeFloat(self):
        nodeFactory = NodeFactory()
        operation = 5.03
        node1 = nodeFactory.generate(operation)
        node2 = RealNode(float(operation))
        self.assertEqual(node1.evaluate(), node2.evaluate())

    def testRealNodeString(self):
        nodeFactory = NodeFactory()
        operation = '5'
        node1 = nodeFactory.generate(operation)
        node2 = RealNode(float(operation))
        self.assertEqual(node1.evaluate(), node2.evaluate())

    def testOperator(self):
        nodeFactory = NodeFactory()
        operation = '+'
        node1 = nodeFactory.generate(operation)
        node2 = AdditionNode()
        self.assertEqual(str(node1), str(node2))

    def testOperators(self):
        nodeFactory = NodeFactory()
        operations='+-*/'
        nodeList = []
        for op in list(operations):
            nodeList.append(nodeFactory.generate(op))
        rep1 = ''.join([str(x) for x in nodeList])
        self.assertEqual(rep1, operations)

class TestRandom(unittest.TestCase):
    def testType1(self):
        nf = NodeFactory()
        node = nf.generate(5)
        self.assertTrue(issubclass(node.__class__, ValueNode))
        self.assertTrue(issubclass(node.__class__, Node))


    def testType2(self):
        node = ValueNode()
        self.assertTrue(issubclass(node.__class__, ValueNode))
        self.assertTrue(issubclass(node.__class__, Node))


    def testType3(self):
        node = RealNode(5)
        self.assertTrue(issubclass(node.__class__, ValueNode))
        self.assertTrue(issubclass(node.__class__, Node))

class TestExpressionTree(unittest.TestCase):
    def testCreate(self):
        tree = ExpressionTree()
        self.assertTrue(tree)

    def testEvaluate(self):
        formular = Formular('5+3')
        ops = formular.stack
        tree = ExpressionTree()
        tree.create_expression_tree_from_postfix(ops)
        self.assertEqual(tree.evaluate(),8)

    def testEvaluate2(self):
        formular = Formular('5+3 * 4')
        ops = formular.stack
        tree = ExpressionTree()
        tree.create_expression_tree_from_postfix(ops)
        self.assertEqual(tree.evaluate(),17.0)

class TestCalculator(unittest.TestCase):
    def testCalculatorAddition(self):
        math = '5+3'
        self.assertEqual(Calculator(math).result(), 5+3)

    def testCalculatorSubtraction(self):
        math = '7-4'
        self.assertEqual(Calculator(math).result(), 7-4)

    def testCalculatorMultiplication(self):
        math = '5*8'
        self.assertEqual(Calculator(math).result(), 5*8)

    def testCalculatorDivision(self):
        math = '5/3.0'
        self.assertEqual(Calculator(math).result(), 5/3.0)

    def testCalculatorParanthesis(self):
        math = '(2+3)*8'
        self.assertEqual(Calculator(math).result(), (2+3)*8)


if __name__ == '__main__':
    unittest.main()
