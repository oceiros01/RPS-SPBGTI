import random
import time
from typing import List, Tuple, Dict, Any

def selection_sort(unsorted_arr: List[int]) -> List[int]:
    """Сортировка выбором"""
    if not unsorted_arr:
        return []
        
    sorted_arr = unsorted_arr.copy()
    N = len(sorted_arr)

    for i in range(N-1):
        min_value = sorted_arr[i]
        index_min_value = i
        for j in range(i+1, N):
            if min_value > sorted_arr[j]:
                min_value = sorted_arr[j]
                index_min_value = j
        
        if index_min_value != i:
            sorted_arr[i], sorted_arr[index_min_value] = sorted_arr[index_min_value], sorted_arr[i]
    
    return sorted_arr

def is_sorted(arr: List[int]) -> bool:
    """Проверка отсортирован ли массив"""
    if not arr:
        return True
        
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True

def generate_random_array(size: int, min_val: int = -1000, max_val: int = 1000) -> List[int]:
    """Генерация случайного массива"""
    if size <= 0:
        return []
    return [random.randint(min_val, max_val) for _ in range(size)]

def measure_sorting_time(array: List[int]) -> Tuple[List[int], float]:
    """Измерение времени сортировки"""
    if not array:
        return [], 0.0
        
    start_time = time.time()
    sorted_array = selection_sort(array)
    end_time = time.time()
    
    return sorted_array, end_time - start_time

class ArrayManager:
    def __init__(self, db_manager, auth_manager):
        self.db = db_manager
        self.auth = auth_manager
    
    def process_array(self, array: List[int], save_original: bool = True, save_sorted: bool = True) -> Dict[str, Any]:
        """Обработка массива с сортировкой и сохранением"""
        if not self.auth.is_authenticated():
            return {"success": False, "message": "Требуется авторизация"}
        
        result = {
            "original_array": array,
            "sorted_array": None,
            "sorting_time": 0,
            "saved_arrays": []
        }
        
        # Сортировка
        if array:
            sorted_array, sorting_time = measure_sorting_time(array)
            result["sorted_array"] = sorted_array
            result["sorting_time"] = sorting_time
            
            # Сохранение в базу
            if save_original and save_sorted:
                array_id = self.db.save_array(self.auth.current_user, array, sorted_array)
                if array_id != -1:
                    result["saved_arrays"].append({"id": array_id, "type": "both"})
            elif save_original:
                array_id = self.db.save_array(self.auth.current_user, array)
                if array_id != -1:
                    result["saved_arrays"].append({"id": array_id, "type": "original"})
            elif save_sorted:
                array_id = self.db.save_array(self.auth.current_user, [], sorted_array)
                if array_id != -1:
                    result["saved_arrays"].append({"id": array_id, "type": "sorted"})
        
        result["success"] = True
        return result
    
    def get_user_history(self) -> List[Dict[str, Any]]:
        """Получение истории массивов пользователя"""
        if not self.auth.is_authenticated():
            return []
        
        return self.db.get_user_arrays(self.auth.current_user)