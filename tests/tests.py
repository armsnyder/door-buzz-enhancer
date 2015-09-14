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

    def test_distance(self):
        in_a = [1, 2, 3, 4, 5]
        in_b = [-2, 7, 11, -9]
        expected = 3+5+8+13
        actual_a = door_buzz_enhancer.get_sound_distance(in_a, in_b)
        actual_b = door_buzz_enhancer.get_sound_distance(in_b, in_a)
        self.assertEqual(actual_a, actual_b)
        self.assertEqual(expected, actual_b)
