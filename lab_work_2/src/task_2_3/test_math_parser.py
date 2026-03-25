import unittest

from math_parser.math_parser import MathParser


class TestMathParser(unittest.TestCase):

    def test_empty_expression(self):
        mp = MathParser(value=' ')
        with self.assertRaises(ValueError) as context:
            mp.construct()
        self.assertIn('Empty expression', str(context.exception))

    def test_single_number(self):
        mp = MathParser("42")
        mp.construct()
        self.assertEqual(mp.calculate(), 42)

    def test_single_variable(self):
        mp = MathParser("a")
        mp.construct()
        mp.assign_values(a=10)
        self.assertEqual(mp.calculate(), 10)

    def test_addition(self):
        mp = MathParser("3+5")
        mp.construct()
        self.assertEqual(mp.calculate(), 8)

    def test_subtraction(self):
        mp = MathParser("10-4")
        mp.construct()
        self.assertEqual(mp.calculate(), 6)

    def test_multiplication(self):
        mp = MathParser("7*8")
        mp.construct()
        self.assertEqual(mp.calculate(), 56)

    def test_division_float(self):
        mp = MathParser("10/3")
        mp.construct()
        res = mp.calculate()
        self.assertAlmostEqual(res, 10/3, places=6)
        self.assertIsInstance(res, float)

    def test_division_negative_float(self):
        mp = MathParser("-10/3")
        mp.construct()
        res = mp.calculate()
        self.assertAlmostEqual(res, -10/3, places=6)
        self.assertIsInstance(res, float)

    def test_division_with_integer_result(self):
        mp = MathParser("12/4")
        mp.construct()
        res = mp.calculate()
        self.assertEqual(res, 3.0)
        self.assertIsInstance(res, float)

    def test_operator_precedence(self):
        mp = MathParser("2+3*4")
        mp.construct()
        self.assertEqual(mp.calculate(), 14)

    def test_parentheses(self):
        mp = MathParser("(2+3)*4")
        mp.construct()
        self.assertEqual(mp.calculate(), 20)

    def test_nested_parentheses(self):
        mp = MathParser("(1+(2+3))*4")
        mp.construct()
        self.assertEqual(mp.calculate(), 24)

    def test_multiple_operators(self):
        mp = MathParser("10-2*3+4/2")
        mp.construct()
        # 2*3=6, 4/2=2, 10-6+2=6
        self.assertEqual(mp.calculate(), 6)       

    def test_single_variable_assignment(self):
        mp = MathParser("x")
        mp.construct()
        mp.assign_values(x=7)
        self.assertEqual(mp.calculate(), 7)

    def test_multiple_variables(self):
        mp = MathParser("a+b*c")
        mp.construct()
        mp.assign_values(a=2, b=3, c=4)
        self.assertEqual(mp.calculate(), 2+3*4)

    def test_assign_unknown_variable(self):
        mp = MathParser(value='1')
        mp.construct()
        with self.assertRaises(ValueError) as context:
            mp.assign_values(**{'a': 1})
        self.assertIn('Unknown variable', str(context.exception))
        
    def test_assign_missing_variable(self):
        mp = MathParser(value='a+b')
        mp.construct()
        mp.assign_values(**{'a': 1})
        with self.assertRaises(ValueError) as context:
            mp.calculate()
        self.assertIn('Missing values for variables', str(context.exception))

    def test_unary_minus_number(self):
        mp = MathParser("-1")
        mp.construct()
        self.assertEqual(mp.calculate(), -1)

    def test_unary_minus_variable(self):
        mp = MathParser("-a")
        mp.construct()
        mp.assign_values(a=5)
        self.assertEqual(mp.calculate(), -5)

    def test_unary_minus_expression(self):
        mp = MathParser("-(2+3)")
        mp.construct()
        self.assertEqual(mp.calculate(), -5)

    def test_unary_minus_with_other_ops(self):
        mp = MathParser("2*(-3)")
        mp.construct()
        self.assertEqual(mp.calculate(), -6)

    def test_double_unary_minus(self):
        mp = MathParser("-(-5)")
        mp.construct()
        self.assertEqual(mp.calculate(), 5)

    def test_unary_plus_ignored(self):
        mp = MathParser("+7")
        mp.construct()
        self.assertEqual(mp.calculate(), 7)

    def test_spaces(self):
        mp = MathParser("  2  +  3  *  4  ")
        mp.construct()
        self.assertEqual(mp.calculate(), 14)

    def test_invalid_character(self):
        mp = MathParser("2+$")
        with self.assertRaises(ValueError):
            mp.construct()

    def test_missing_parenthesis(self):
        mp = MathParser("(2+3")
        with self.assertRaises(ValueError):
            mp.construct()

    def test_repeated_calculation(self):
        mp = MathParser("2*3")
        mp.construct()
        self.assertEqual(mp.calculate(), 6)
        self.assertEqual(mp.calculate(), 6)  # второй раз

    def test_recalculate_with_new_variables(self):
        mp = MathParser("a+b")
        mp.construct()
        mp.assign_values(a=2, b=3)
        self.assertEqual(mp.calculate(), 5)
        mp.assign_values(a=10, b=1)  # меняем значения
        self.assertEqual(mp.calculate(), 11)


if __name__ == '__main__':
    unittest.main(verbosity=3)