
def selection_sort(unsorted_arr):
    sorted_arr = unsorted_arr.copy()
    N = len(sorted_arr)  # число элементов в списке

    for i in range(N-1): # Внешний цикл
        min_value = sorted_arr[i] # Предполагаем, что текущий элемент - минимальный
        index_min_value = i # индекс минимального значения
        for j in range(i+1, N): # Внутренний цикл - ищем настоящий минимум
            if min_value > sorted_arr[j]:  
                min_value = sorted_arr[j]
                index_min_value = j # Нашли элемент еще меньше
        
        if  index_min_value != i: # Меняем местами найденный минимум с текущей позицией
            temp = sorted_arr[i]
            sorted_arr[i] = sorted_arr[index_min_value]
            sorted_arr[index_min_value] = temp
    return sorted_arr

def is_sorted(arr):
    # Проверяет, отсортирован ли массив

    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True