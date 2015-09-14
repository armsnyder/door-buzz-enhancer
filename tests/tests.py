__author__ = 'Adam Snyder'

import unittest
import door_buzz_enhancer


class Test(unittest.TestCase):
    def test_get_sound(self):
        milliseconds = 100
        actual, _ = door_buzz_enhancer.get_sound(milliseconds)
        found_non_zero = False
        for bit in actual:
            if bit != 0:
                found_non_zero = True
                break
        self.assertTrue(found_non_zero)
