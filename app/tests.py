from django.test import TestCase
from .calc import add, sub


class CalcTests(TestCase):
    def test_add_numbers(self):
        """This test the add method"""

        self.assertEqual(add(2, 3), 5)

    def test_substract_numbers(self):
        """This test the substraction of numbers"""

        self.assertEqual(sub(5, 6), 1)
