from TDD.factorize import factorize

import unittest


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exceptions(self):
        test_cases = ['string', 1.5]
        for i in range(len(test_cases)):
            with self.subTest(x=i):
                self.assertRaises(TypeError, factorize, test_cases[i])

    def test_negative(self):
        test_cases = [-1, -10, -100]
        for i in range(len(test_cases)):
            with self.subTest(x=i):
                self.assertRaises(ValueError, factorize, test_cases[i])

    def test_zero_and_one_cases(self):
        test_cases = {0: (0, ), 1: (1, )}
        for i, item in enumerate(test_cases.items()):
            with self.subTest(x=i):
                key = item[0]
                self.assertEqual(factorize(key), item[1])

    def test_simple_numbers(self):
        test_cases = {3: (3, ), 13: (13, ), 29: (29, )}
        for i, item in enumerate(test_cases.items()):
            with self.subTest(x=i):
                key = item[0]
                self.assertEqual(factorize(key), item[1])

    def test_two_simple_multipliers(self):
        test_cases = {6: (2, 3), 26: (2, 13), 121: (11, 11)}
        for i, item in enumerate(test_cases.items()):
            with self.subTest(x=i):
                key = item[0]
                self.assertEqual(factorize(key), item[1])

    def test_many_multipliers(self):
        test_cases = {1001: (7, 11, 13), 9699690: (2, 3, 5, 7, 11, 13, 17, 19)}
        for i, item in enumerate(test_cases.items()):
            with self.subTest(x=i):
                key = item[0]
                self.assertEqual(factorize(key), item[1])
