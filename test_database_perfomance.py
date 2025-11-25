import unittest
import time
import random
import sys
import os

# Добавляем путь к основному проекту для импорта модулей
# os.path.dirname(__file__) - получаем директорию текущего файла
# os.path.join(..., '..') - поднимаемся на уровень выше
# sys.path.append(...) - добавляем путь в список путей для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Импорт классов и функций из основного приложения
from app.database import DatabaseManager
from app.sorting import selection_sort, generate_random_array

class DatabasePerformanceTests(unittest.TestCase):
    """
    Интеграционные тесты производительности базы данных
    Тесты используют отдельную тестовую базу данных
    """
    
    @classmethod
    def setUpClass(cls):
        """Настройка перед всеми тестами"""
        # Устанавливаем имя тестовой базы данных
        cls.test_db_name = "performance_test.db"
        # Удаляем старую тестовую базу если существует
        if os.path.exists(cls.test_db_name):
            os.remove(cls.test_db_name)
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        # Создаем отдельную базу данных для тестов в тестовом режиме
        self.db = DatabaseManager(test_mode=True)
        # Очищаем базу данных перед началом теста
        self.db.clear_database()
    
    def tearDown(self):
        """Очистка после каждого теста"""
        # Закрываем соединение с базой данных если оно существует
        if self.db.connection:
            self.db.connection.close()
    
    def test_a_insert_100_arrays(self):
        """
        Тест добавления 100 массивов в базу данных
        Требование: вывод флага успешного/неуспешного выполнения и время работы
        """
        # Вывод заголовка теста для наглядности
        print("\n" + "="*60)
        print("ТЕСТ A: ДОБАВЛЕНИЕ 100 МАССИВОВ")
        print("="*60)
        
        # Вызов вспомогательного метода для выполнения теста вставки
        success, execution_time, details = self._perform_insert_test(100)
        
        # Вывод результатов теста
        print(f"Флаг выполнения: {'УСПЕХ' if success else 'НЕУДАЧА'}")
        print(f"Время работы: {execution_time:.4f} секунд")
        print(f"Детали: {details}")
        
        # Проверка что тест прошел успешно
        self.assertTrue(success, "Тест добавления 100 массивов не прошел")
    
    def test_a_insert_1000_arrays(self):
        """
        Тест добавления 1000 массивов в базу данных
        """
        print("\n" + "="*60)
        print("ТЕСТ A: ДОБАВЛЕНИЕ 1000 МАССИВОВ")
        print("="*60)
        
        success, execution_time, details = self._perform_insert_test(1000)
        
        print(f"Флаг выполнения: {'УСПЕХ' if success else 'НЕУДАЧА'}")
        print(f"Время работы: {execution_time:.4f} секунд")
        print(f"Детали: {details}")
        
        self.assertTrue(success, "Тест добавления 1000 массивов не прошел")
    
    def test_a_insert_10000_arrays(self):
        """
        Тест добавления 10000 массивов в базу данных
        """
        print("\n" + "="*60)
        print("ТЕСТ A: ДОБАВЛЕНИЕ 10000 МАССИВОВ")
        print("="*60)
        
        success, execution_time, details = self._perform_insert_test(10000)
        
        print(f"Флаг выполнения: {'УСПЕХ' if success else 'НЕУДАЧА'}")
        print(f"Время работы: {execution_time:.4f} секунд")
        print(f"Детали: {details}")
        
        self.assertTrue(success, "Тест добавления 10000 массивов не прошел")
    
    def _perform_insert_test(self, count):
        """Вспомогательный метод для тестирования вставки массивов"""
        try:
            # Засекаем время начала выполнения теста
            start_time = time.time()
            
            # Создаем тестового пользователя для работы с базой данных
            self.db.register_user("perf_test_user", "test_hash")
            # Аутентифицируем пользователя и получаем его ID
            user_id = self.db.authenticate_user("perf_test_user", "test_hash")
            
            # Проверяем что пользователь успешно создан
            if not user_id:
                return False, 0, "Не удалось создать тестового пользователя"
            
            # Счетчик успешно обработанных массивов
            arrays_processed = 0
            # Цикл для создания и сохранения указанного количества массивов
            for i in range(count):
                # Генерируем случайный размер массива от 10 до 1000 элементов
                size = random.randint(10, 1000)
                # Генерируем случайный массив с числами от -10000 до 10000
                array = generate_random_array(size, -10000, 10000)
                # Сортируем сгенерированный массив
                sorted_array = selection_sort(array)
                
                # Сохраняем массив в базу данных
                array_id = self.db.save_array(user_id, array, sorted_array)
                # Если сохранение прошло успешно (ID > 0), увеличиваем счетчик
                if array_id > 0:
                    arrays_processed += 1
            
            # Засекаем время окончания выполнения теста
            end_time = time.time()
            # Вычисляем общее время выполнения
            execution_time = end_time - start_time
            
            # Проверяем результат - сколько массивов действительно сохранено в БД
            actual_count = self.db.get_array_count()
            # Успех теста - если сохранено столько массивов, сколько планировалось
            success = actual_count == count
            
            # Формируем детализированное сообщение о результатах
            details = f"Ожидалось: {count}, Сохранено: {arrays_processed}, В базе: {actual_count}"
            
            # Возвращаем результаты теста
            return success, execution_time, details
            
        except Exception as e:
            # В случае ошибки вычисляем время выполнения если start_time был определен
            execution_time = time.time() - start_time if 'start_time' in locals() else 0
            # Возвращаем информацию об ошибке
            return False, execution_time, f"Ошибка: {str(e)}"
    
    def test_b_sort_100_arrays_from_100(self):
        """
        Тест выгрузки и сортировки 100 массивов из базы на 100 записей
        Требование: вывод флага, общего времени и среднего времени на массив
        """
        print("\n" + "="*60)
        print("ТЕСТ B: ВЫГРУЗКА И СОРТИРОВКА 100 МАССИВОВ ИЗ БАЗЫ НА 100")
        print("="*60)
        
        success, total_time, avg_time, details = self._perform_sort_test(100, 100)
        
        print(f"Флаг выполнения: {'УСПЕХ' if success else 'НЕУДАЧА'}")
        print(f"Общее время работы: {total_time:.4f} секунд")
        print(f"Среднее время на массив: {avg_time:.6f} секунд")
        print(f"Детали: {details}")
        
        self.assertTrue(success, "Тест сортировки из базы на 100 не прошел")
    
    def test_b_sort_100_arrays_from_1000(self):
        """
        Тест выгрузки и сортировки 100 массивов из базы на 1000 записей
        """
        print("\n" + "="*60)
        print("ТЕСТ B: ВЫГРУЗКА И СОРТИРОВКА 100 МАССИВОВ ИЗ БАЗЫ НА 1000")
        print("="*60)
        
        success, total_time, avg_time, details = self._perform_sort_test(100, 1000)
        
        print(f"Флаг выполнения: {'УСПЕХ' if success else 'НЕУДАЧА'}")
        print(f"Общее время работы: {total_time:.4f} секунд")
        print(f"Среднее время на массив: {avg_time:.6f} секунд")
        print(f"Детали: {details}")
        
        self.assertTrue(success, "Тест сортировки из базы на 1000 не прошел")
    
    def test_b_sort_100_arrays_from_10000(self):
        """
        Тест выгрузки и сортировки 100 массивов из базы на 10000 записей
        """
        print("\n" + "="*60)
        print("ТЕСТ B: ВЫГРУЗКА И СОРТИРОВКА 100 МАССИВОВ ИЗ БАЗЫ НА 10000")
        print("="*60)
        
        success, total_time, avg_time, details = self._perform_sort_test(100, 10000)
        
        print(f"Флаг выполнения: {'УСПЕХ' if success else 'НЕУДАЧА'}")
        print(f"Общее время работы: {total_time:.4f} секунд")
        print(f"Среднее время на массив: {avg_time:.6f} секунд")
        print(f"Детали: {details}")
        
        self.assertTrue(success, "Тест сортировки из базы на 10000 не прошел")
    
    def _perform_sort_test(self, sort_count, db_size):
        """Вспомогательный метод для тестирования выгрузки и сортировки"""
        try:
            # Подготавливаем базу данных - создаем пользователя
            self.db.register_user("sort_test_user", "test_hash")
            user_id = self.db.authenticate_user("sort_test_user", "test_hash")
            
            if not user_id:
                return False, 0, 0, "Не удалось создать тестового пользователя"
            
            # Заполняем базу данных случайными массивами до указанного размера
            print(f"Заполнение базы {db_size} записями...")
            for i in range(db_size):
                # Генерируем массив случайного размера
                size = random.randint(10, 500)
                # Создаем случайный массив
                array = generate_random_array(size, -5000, 5000)
                # Сохраняем массив в базу
                self.db.save_array(user_id, array)
                # Выводим прогресс каждые 1000 записей
                if i % 1000 == 0 and i > 0:
                    print(f"  Добавлено {i} массивов...")
            
            # Проверяем, что база заполнена корректно
            actual_db_size = self.db.get_array_count()
            if actual_db_size != db_size:
                return False, 0, 0, f"База заполнена некорректно: {actual_db_size} вместо {db_size}"
            
            # Выполняем тест сортировки - засекаем общее время
            start_time = time.time()
            total_sort_time = 0  # Общее время только на сортировку
            arrays_processed = 0  # Счетчик обработанных массивов
            
            # Получаем случайные массивы из базы для сортировки
            arrays = self.db.get_random_arrays(sort_count)
            arrays_processed = len(arrays)
            
            # Сортируем каждый массив и замеряем время
            for i, array_data in enumerate(arrays):
                array = array_data['original_array']
                
                # Замеряем время сортировки одного массива
                sort_start = time.time()
                sorted_array = selection_sort(array)
                sort_end = time.time()
                
                # Суммируем время сортировки
                total_sort_time += (sort_end - sort_start)
                
                # Проверяем корректность сортировки
                # all() проверяет что все элементы отсортированы по возрастанию
                is_correctly_sorted = all(
                    sorted_array[i] <= sorted_array[i+1] 
                    for i in range(len(sorted_array)-1)
                )
                
                # Если массив отсортирован некорректно - возвращаем ошибку
                if not is_correctly_sorted:
                    return False, 0, 0, f"Массив {i} отсортирован некорректно"
            
            # Вычисляем общее время выполнения теста
            end_time = time.time()
            total_time = end_time - start_time
            # Вычисляем среднее время сортировки одного массива
            avg_time_per_array = total_sort_time / arrays_processed if arrays_processed > 0 else 0
            
            # Формируем детализированное сообщение
            details = f"Обработано массивов: {arrays_processed}, Общее время сортировки: {total_sort_time:.4f} сек"
            
            return True, total_time, avg_time_per_array, details
            
        except Exception as e:
            # В случае ошибки вычисляем общее время если start_time был определен
            total_time = time.time() - start_time if 'start_time' in locals() else 0
            return False, total_time, 0, f"Ошибка: {str(e)}"
    
    def test_c_clear_database_100(self):
        """
        Тест очистки базы данных с 100 записями
        Требование: вывод флага успешного/неуспешного выполнения и время работы
        """
        print("\n" + "="*60)
        print("ТЕСТ C: ОЧИСТКА БАЗЫ ДАННЫХ С 100 ЗАПИСЯМИ")
        print("="*60)
        
        success, execution_time, details = self._perform_clear_test(100)
        
        print(f"Флаг выполнения: {'УСПЕХ' if success else 'НЕУДАЧА'}")
        print(f"Время работы: {execution_time:.10f} секунд")
        print(f"Детали: {details}")
        
        self.assertTrue(success, "Тест очистки базы на 100 не прошел")
    
    def test_c_clear_database_1000(self):
        """
        Тест очистки базы данных с 1000 записями
        """
        print("\n" + "="*60)
        print("ТЕСТ C: ОЧИСТКА БАЗЫ ДАННЫХ С 1000 ЗАПИСЯМИ")
        print("="*60)
        
        success, execution_time, details = self._perform_clear_test(1000)
        
        print(f"Флаг выполнения: {'УСПЕХ' if success else 'НЕУДАЧА'}")
        print(f"Время работы: {execution_time:.10f} секунд")
        print(f"Детали: {details}")
        
        self.assertTrue(success, "Тест очистки базы на 1000 не прошел")
    
    def test_c_clear_database_10000(self):
        """
        Тест очистки базы данных с 10000 записями
        """
        print("\n" + "="*60)
        print("ТЕСТ C: ОЧИСТКА БАЗЫ ДАННЫХ С 10000 ЗАПИСЯМИ")
        print("="*60)
        
        success, execution_time, details = self._perform_clear_test(10000)
        
        print(f"Флаг выполнения: {'УСПЕХ' if success else 'НЕУДАЧА'}")
        print(f"Время работы: {execution_time:.10f} секунд")
        print(f"Детали: {details}")
        
        self.assertTrue(success, "Тест очистки базы на 10000 не прошел")
    
    def _perform_clear_test(self, initial_count):
        """Вспомогательный метод для тестирования очистки базы данных"""
        try:
            # Заполняем базу данных - создаем пользователя
            self.db.register_user("clear_test_user", "test_hash")
            user_id = self.db.authenticate_user("clear_test_user", "test_hash")
            
            if not user_id:
                return False, 0, "Не удалось создать тестового пользователя"
            
            # Заполняем базу указанным количеством записей
            print(f"Заполнение базы {initial_count} записями...")
            for i in range(initial_count):
                size = random.randint(10, 100)
                array = generate_random_array(size, -1000, 1000)
                self.db.save_array(user_id, array)
                # Выводим прогресс каждые 1000 записей
                if i % 1000 == 0 and i > 0:
                    print(f"  Добавлено {i} массивов...")
            
            # Проверяем, что база заполнена корректно
            initial_db_count = self.db.get_array_count()
            if initial_db_count != initial_count:
                return False, 0, f"База заполнена некорректно: {initial_db_count} вместо {initial_count}"
            
            # Очищаем базу и замеряем время
            start_time = time.time()
            self.db.clear_database()  # Выполняем очистку базы
            end_time = time.time()
            
            # Вычисляем время выполнения очистки
            execution_time = end_time - start_time
            
            # Проверяем, что база действительно пуста
            final_db_count = self.db.get_array_count()
            success = final_db_count == 0
            
            # Формируем детализированное сообщение
            details = f"Записей до очистки: {initial_db_count}, после очистки: {final_db_count}"
            
            return success, execution_time, details
            
        except Exception as e:
            # В случае ошибки вычисляем время выполнения если start_time был определен
            execution_time = time.time() - start_time if 'start_time' in locals() else 0
            return False, execution_time, f"Ошибка: {str(e)}"

# Проверка что скрипт запущен напрямую (а не импортирован как модуль)
if __name__ == '__main__':
    # Запуск всех тестов в классе
    unittest.main()                                                     