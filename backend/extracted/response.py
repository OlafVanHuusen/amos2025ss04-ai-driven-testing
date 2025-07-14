import sys
from pathlib import Path
sys.path.insert(0, '/code/extracted')  # Add extracted dir to import path
from prompt import *  # Import functions from prompt.py

import unittest

import unittest


class TestBubbleSort(unittest.TestCase):
    def test_sorted_list(self):
        arr = [11, 12, 22, 25, 34, 64, 90]
        bubble_sort(arr)
        self.assertEqual(arr, [11, 12, 22, 25, 34, 64, 90])

    def test_unsorted_list(self):
        arr = [64, 34, 25, 12, 22, 11, 90]
        bubble_sort(arr)
        self.assertEqual(arr, [11, 12, 22, 25, 34, 64, 90])

    def test_empty_list(self):
        arr = []
        bubble_sort(arr)
        self.assertEqual(arr, [])

    def test_single_element_list(self):
        arr = [5]
        bubble_sort(arr)
        self.assertEqual(arr, [5])

    def test_even_length_list(self):
        arr = [5, 3, 8, 6]
        bubble_sort(arr)
        self.assertEqual(arr, [3, 5, 6, 8])

    def test_odd_length_list(self):
        arr = [5, 3, 8, 6, 2]
        bubble_sort(arr)
        self.assertEqual(arr, [2, 3, 5, 6, 8])


if __name__ == "__main__":
    unittest.main()
