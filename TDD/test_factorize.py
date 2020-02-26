from TDD.factorize import factorize

import unittest


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exceptions(self):
        test_cases = ['string', 1.5]
        for x in test_cases:
            with self.subTest(x=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        test_cases = [-1, -10, -100]
        for x in test_cases:
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        test_cases = {0: (0, ), 1: (1, )}
        for key, value in test_cases.items():
            with self.subTest(x=key):
                self.assertEqual(factorize(key), value)

    def test_simple_numbers(self):
        test_cases = {3: (3, ), 13: (13, ), 29: (29, )}
        for key, value in test_cases.items():
            with self.subTest(x=key):
                self.assertEqual(factorize(key), value)

    def test_two_simple_multipliers(self):
        test_cases = {6: (2, 3), 26: (2, 13), 121: (11, 11)}
        for key, value in test_cases.items():
            with self.subTest(x=key):
                self.assertEqual(factorize(key), value)

    def test_many_multipliers(self):
        test_cases = {1001: (7, 11, 13), 9699690: (2, 3, 5, 7, 11, 13, 17, 19)}
        for key, value in test_cases.items():
            with self.subTest(x=key):
                self.assertEqual(factorize(key), value)
