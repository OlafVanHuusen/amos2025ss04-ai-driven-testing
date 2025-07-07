import sys
from pathlib import Path
sys.path.insert(0, '/code/extracted')  # Add extracted dir to import path
from prompt import *  # Import functions from prompt.py

import unittest
from mylib import calculate_result


class CalculateResultTest(unittest.TestCase):
    def test_addition(self):
        a = 10
        b = 20
        op = ("+",)  # '+' is the default operator
        expected = 30
        actual = calculate_result(a, b, op[0])
        self.assertEqual(expected, actual)

    def test_subtraction(self):
        a = 10
        b = 20
        op = ("-",)  # '-' is the default operator
        expected = 8
        actual = calculate_result(a, b, op[0])
        self.assertEqual(expected, actual)

    def test_multiplication(self):
        a = 10
        b = 20
        op = ("*",)  # "* " is the default operator
        expected = 30
        actual = calculate_result(a, b, op[0])
        self.assertEqual(expected, actual)

    def test_division(self):
        a = 10
        b = 20
        op = ("/",)  # "/" is the default operator
        expected = 5
        actual = calculate_result(a, b, op[0])
        self.assertEqual(expected, actual)

    def test_negative_division(self):
        a = -10
        b = 20
        op = ("/",)  # "/" is the default operator
        expected = 5
        actual = calculate_result(a, b, op[0])
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
