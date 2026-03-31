
import unittest
import sys
import os
import time


def main():
    """Основная функция запуска тестов"""
    print("=" * 80)
    print("ИНТЕГРАЦИОННЫЕ ТЕСТЫ ПРОИЗВОДИТЕЛЬНОСТИ БАЗЫ ДАННЫХ")
    print("=" * 80)
    print("Тесты используют временную базу данных")
    print("=" * 80)
    
    # Добавляем путь к основному проекту
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    
    # Импортируем класс тестов производительности
    from test_database_perfomance import DatabasePerformanceTests
    
    # Определяем порядок выполнения тестов
    test_cases = [
        # Тесты добавления массивов 
        'test_a_insert_100_arrays',      
        'test_a_insert_1000_arrays',     
        'test_a_insert_10000_arrays',    
        
        # Тесты выгрузки и сортировки 
        'test_b_sort_100_arrays_from_100',    
        'test_b_sort_100_arrays_from_1000',   
        'test_b_sort_100_arrays_from_10000',  
        
        # Тесты очистки базы данных 
        'test_c_clear_database_100',     
        'test_c_clear_database_1000',    
        'test_c_clear_database_10000',  
    ]
    
    # Создаем test suite
    suite = unittest.TestSuite()
    for test_name in test_cases:
        suite.addTest(DatabasePerformanceTests(test_name))
    
    print(f"\nЗапуск {len(test_cases)} интеграционных тестов...")
    print("Тесты выполняются в следующем порядке:")
    for i, test_name in enumerate(test_cases, 1):
        print(f"  {i}. {test_name}")
    
    print("\n" + "=" * 80)
    
    # Запускаем тесты
    start_time = time.time()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    end_time = time.time()
    
    # Выводим итоги
    print("\n" + "=" * 80)
    print("ИТОГИ ТЕСТИРОВАНИЯ:")
    print("=" * 80)
    print(f"Общее время выполнения: {end_time - start_time:.2f} секунд")
    print(f"Всего тестов: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    
    if result.failures:
        print("\nПРОВАЛЕННЫЕ ТЕСТЫ:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.splitlines()[-1]}")
    
    if result.errors:
        print("\nТЕСТЫ С ОШИБКАМИ:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.splitlines()[-1]}")
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)

# Проверка что скрипт запущен напрямую, а не импортирован как модуль
if __name__ == '__main__':
    # Вызываем основную функцию и сохраняем код возврата
    exit_code = main()
    # Завершаем программу с соответствующим кодом выхода
    sys.exit(exit_code)