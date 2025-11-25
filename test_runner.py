
import unittest
import sys
import os
import time

def main():
    """Основная функция запуска тестов"""
    # Вывод заголовка тестовой сессии
    print("=" * 80)
    print("ИНТЕГРАЦИОННЫЕ ТЕСТЫ ПРОИЗВОДИТЕЛЬНОСТИ БАЗЫ ДАННЫХ")
    print("=" * 80)
    print("Тесты используют отдельную тестовую базу данных")
    print("=" * 80)
    
    # Добавляем путь к основному проекту для импорта модулей
    # os.path.dirname(__file__) получает директорию текущего файла
    # os.path.join(..., '..') поднимается на один уровень вверх
    # sys.path.append(...) добавляет этот путь в список путей Python
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    
    # Импортируем класс тестов производительности из файла test_database_performance
    from test_database_perfomance import DatabasePerformanceTests
    
    # Создаем загрузчик тестов для управления процессом тестирования
    loader = unittest.TestLoader()
    
    # Определяем порядок выполнения тестов вручную
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
    
    # Создаем test suite (набор тестов) с определенным порядком выполнения
    suite = unittest.TestSuite()
    # Добавляем каждый тест в suite в указанном порядке
    for test_name in test_cases:
        # DatabasePerformanceTests(test_name) создает экземпляр теста
        # suite.addTest() добавляет тест в набор
        suite.addTest(DatabasePerformanceTests(test_name))
    
    # Выводим информацию о запускаемых тестах
    print(f"\nЗапуск {len(test_cases)} интеграционных тестов...")
    print("Тесты выполняются в следующем порядке:")
    # Выводим нумерованный список тестов для наглядности
    for i, test_name in enumerate(test_cases, 1):
        print(f"  {i}. {test_name}")
    
    # Разделитель перед началом выполнения тестов
    print("\n" + "=" * 80)
    
    # Засекаем время начала выполнения всех тестов
    start_time = time.time()
    # Создаем runner для выполнения тестов с повышенной детализацией вывода (verbosity=2)
    runner = unittest.TextTestRunner(verbosity=2)
    # Запускаем все тесты в suite и сохраняем результат
    result = runner.run(suite)
    # Засекаем время окончания выполнения тестов
    end_time = time.time()
    
    # Выводим итоговую статистику выполнения тестов
    print("\n" + "=" * 80)
    print("ИТОГИ ТЕСТИРОВАНИЯ:")
    print("=" * 80)
    # Вычисляем и выводим общее время выполнения всех тестов
    print(f"Общее время выполнения: {end_time - start_time:.2f} секунд")
    # Выводим общее количество запущенных тестов
    print(f"Всего тестов: {result.testsRun}")
    # Вычисляем количество успешных тестов (общее минус проваленные и с ошибками)
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    # Выводим количество проваленных тестов (assert не прошел)
    print(f"Провалено: {len(result.failures)}")
    # Выводим количество тестов с ошибками (исключения во время выполнения)
    print(f"Ошибок: {len(result.errors)}")
    
    # Если есть проваленные тесты, выводим информацию о них
    if result.failures:
        print("\nПРОВАЛЕННЫЕ ТЕСТЫ:")
        # Проходим по всем проваленным тестам
        for test, traceback in result.failures:
            # traceback.splitlines()[-1] получает последнюю строку трассировки (саму ошибку)
            print(f"  - {test}: {traceback.splitlines()[-1]}")
    
    # Если есть тесты с ошибками, выводим информацию о них
    if result.errors:
        print("\nТЕСТЫ С ОШИБКАМИ:")
        # Проходим по всем тестам с ошибками
        for test, traceback in result.errors:
            # Выводим имя теста и последнюю строку ошибки
            print(f"  - {test}: {traceback.splitlines()[-1]}")
    
    # Возвращаем код выхода: 0 если все тесты прошли успешно, 1 если были ошибки
    # result.wasSuccessful() возвращает True если не было failures и errors
    return 0 if result.wasSuccessful() else 1

# Проверка что скрипт запущен напрямую, а не импортирован как модуль
if __name__ == '__main__':
    # Вызываем основную функцию и сохраняем код возврата
    exit_code = main()
    # Завершаем программу с соответствующим кодом выхода
    sys.exit(exit_code)