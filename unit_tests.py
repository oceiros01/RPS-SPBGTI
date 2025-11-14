import unittest
import os
import json
import random
from selection_sort import selection_sort, is_sorted

class TestSelectionSort(unittest.TestCase):
    """Тесты для функции сортировки пузырьком"""
    
    def test_empty_array(self):
        """Тест сортировки пустого массива"""
        arr = []
        result = selection_sort(arr)
        self.assertEqual(result, [])
        self.assertTrue(is_sorted(result))
    
    def test_single_element(self):
        """Тест сортировки массива с одним элементом"""
        arr = [5]
        result = selection_sort(arr)
        self.assertEqual(result, [5])
        self.assertTrue(is_sorted(result))
    
    def test_sorted_array(self):
        """Тест сортировки уже отсортированного массива"""
        arr = [1, 2, 3, 4, 5]
        result = selection_sort(arr)
        self.assertEqual(result, [1, 2, 3, 4, 5])
        self.assertTrue(is_sorted(result))
    
    def test_reverse_sorted_array(self):
        """Тест сортировки массива, отсортированного в обратном порядке"""
        arr = [5, 4, 3, 2, 1]
        result = selection_sort(arr)
        self.assertEqual(result, [1, 2, 3, 4, 5])
        self.assertTrue(is_sorted(result))
    
    def test_random_array(self):
        """Тест сортировки случайного массива"""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        result = selection_sort(arr)
        expected = [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
        self.assertEqual(result, expected)
        self.assertTrue(is_sorted(result))
    
    def test_negative_numbers(self):
        """Тест сортировки массива с отрицательными числами"""
        arr = [-3, -1, -4, -2, 0, 2, 1, -5]
        result = selection_sort(arr)
        expected = [-5, -4, -3, -2, -1, 0, 1, 2]
        self.assertEqual(result, expected)
        self.assertTrue(is_sorted(result))
    
    def test_duplicate_elements(self):
        """Тест сортировки массива с повторяющимися элементами"""
        arr = [5, 2, 5, 1, 2, 5, 1]
        result = selection_sort(arr)
        expected = [1, 1, 2, 2, 5, 5, 5]
        self.assertEqual(result, expected)
        self.assertTrue(is_sorted(result))
    
    def test_large_random_array(self):
        """Тест сортировки большого случайного массива"""
        arr = [random.randint(-1000, 1000) for _ in range(1000)]
        result = selection_sort(arr)
        self.assertTrue(is_sorted(result))
        # Проверяем, что отсортированный массив содержит те же элементы
        self.assertEqual(sorted(arr), result)
    
    def test_original_array_not_modified(self):
        """Тест, что исходный массив не изменяется"""
        arr = [5, 3, 8, 1, 2]
        original_arr = arr.copy()
        result = selection_sort(arr)
        self.assertEqual(arr, original_arr)  # Исходный массив не изменился
        self.assertNotEqual(arr, result)     # Результат отличается от исходного

