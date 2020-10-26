import unittest
from circuit import AdditionGate, MultiplicationGate, ScalarMultGate, Circuit
from gf import FFE

class TestCircuit(unittest.TestCase):

    def test_addition1(self):
        a = FFE(10, 31)
        b = FFE(12, 31)
        g = AdditionGate("test")
        res = g.calculate(a,b)
        self.assertEqual(res, a + b)
        
    def test_addition2(self):
        a = FFE(30, 31)
        b = FFE(12, 31)
        g = AdditionGate("test")
        res = g.calculate(a,b)
        self.assertEqual(res, a + b)
        
    def test_multiplication(self):
        a = FFE(30, 31)
        b = FFE(12, 31)
        g = MultiplicationGate("test")
        res = g.calculate(a,b)
        self.assertEqual(res, a * b)
    
    def test_scalar_mult(self):
        scalar = FFE(3, 7)
        a = FFE(4, 7)
        b = FFE(5, 7)
        g = ScalarMultGate(scalar, "test")
        res = g.calculate(a)
        self.assertEqual(res, scalar * a)
        res = g.calculate(b)
        self.assertEqual(res, scalar * b)
    
    def test_eval_order(self):
        c = Circuit(2)
        f = AdditionGate("F")
        g = AdditionGate("G")
        h = ScalarMultGate(2, "H")
        c.add_gate(h, ["INPUT1"])
        c.add_gate(f, ["H","INPUT0"])
        c.add_gate(g, ["F", "H"], True)
        self.assertEqual(c.eval_order(), ['H', 'F', 'G', 'OUTPUT'])
    
    def test_evaluation(self):
        c = Circuit(2)
        f = AdditionGate("F")
        g = AdditionGate("G")
        h = ScalarMultGate(2, "H")
        c.add_gate(h, ["INPUT1"])
        c.add_gate(f, ["H","INPUT0"])
        c.add_gate(g, ["F", "H"], True)
        input0, input1 = 1, 100
        result = c.evaluate((input0, input1))
        h_res = input1 * 2
        f_res = h_res + input0
        g_res = h_res + f_res
        self.assertEqual(result, g_res)
    

if __name__ == '__main__':
    unittest.main()
