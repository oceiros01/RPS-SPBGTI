import unittest
import time
import random
import sys
import os
import tempfile
import json

# Добавляем путь к основному проекту для импорта модулей
# os.path.dirname(__file__) - получаем директорию текущего файла
# os.path.join(..., '..') - поднимаемся на уровень выше
# sys.path.append(...) - добавляем путь в список путей для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Импорт классов и функций из основного приложения
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database import DatabaseManager
from sorting import selection_sort, generate_random_array

class DatabasePerformanceTests(unittest.TestCase):
    """
    Интеграционные тесты производительности базы данных
    Тесты используют одну тестовую базу данных для всех тестов
    """
    
    @classmethod
    def setUpClass(cls):
        """Настройка перед всеми тестами - СОЗДАЕМ БАЗУ ОДИН РАЗ"""
        # Создаем временный файл для тестовой базы данных
        cls.temp_db_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        cls.temp_db_file.close()
        cls.test_db_path = cls.temp_db_file.name
        
        # СОЗДАЕМ БАЗУ ДАННЫХ ОДИН РАЗ ДЛЯ ВСЕХ ТЕСТОВ
        try:
            cls.db = DatabaseManager(test_mode=True, test_db_path=cls.test_db_path)
        except TypeError:
            # Если конструктор не поддерживает test_db_path
            cls.db = DatabaseManager(test_mode=True)
            cls.db.db_path = cls.test_db_path
            if cls.db.connection:
                cls.db.connection.close()
            cls.db.connect()
    
    @classmethod
    def tearDownClass(cls):
        """Очистка после всех тестов - УДАЛЯЕМ ФАЙЛ ОДИН РАЗ"""
        # Закрываем соединение
        if hasattr(cls, 'db') and cls.db.connection:
            cls.db.connection.close()
        
        # Удаляем временный файл
        try:
            os.unlink(cls.test_db_path)
        except:
            pass
    
    def setUp(self):
        """Настройка перед каждым тестом - ОЧИЩАЕМ СУЩЕСТВУЮЩУЮ БАЗУ"""
        # НЕ создаем новую базу! Используем существующую
        
        # Очищаем данные из таблиц
        self.db.clear_database()
        
        # Пересоздаем структуру таблиц (если нужно)
        if hasattr(self.db, 'create_tables'):
            self.db.create_tables()
        elif hasattr(self.db, 'init_database'):
            self.db.init_database()
        
        # Регистрируем тестового пользователя
        # Обрабатываем разные варианты API
        result = self.db.register_user("test_user", "test_password")
        
        if isinstance(result, tuple) and len(result) == 2:
            # register_user возвращает (success, message)
            success, message = result
        else:
            # register_user возвращает просто bool
            success = result
        
        # Получаем ID пользователя
        self.user_id = self.db.authenticate_user("test_user", "test_password")
        self.assertIsNotNone(self.user_id, "Не удалось создать тестового пользователя")
    
    def tearDown(self):
        """Очистка после каждого теста - только очищаем данные"""
        # НЕ закрываем соединение! Оно нужно для других тестов
        # Просто очищаем данные
        self.db.clear_database()
        
    def test_a_insert_100_arrays(self):
        """
        Тест добавления 100 массивов в базу данных
        """
        print("\n" + "="*60)
        print("ТЕСТ A: ДОБАВЛЕНИЕ 100 МАССИВОВ")
        print("="*60)
        
        success, execution_time, details = self._perform_insert_test(100)
        
        print(f"Флаг выполнения: {'УСПЕХ' if success else 'НЕУДАЧА'}")
        print(f"Время работы: {execution_time:.4f} секунд")
        print(f"Детали: {details}")
        
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
            start_time = time.time()
            arrays_processed = 0
            
            # Цикл для создания и сохранения указанного количества массивов
            for i in range(count):
                size = random.randint(10, 1000)
                array = generate_random_array(size, -10000, 10000)
                sorted_array = selection_sort(array)
                
                # Сохраняем массив в базу данных
                array_id = self.db.save_array(self.user_id, array, sorted_array)
                if array_id > 0:
                    arrays_processed += 1
                
                # Выводим прогресс для больших тестов
                if count >= 1000 and i % 1000 == 0 and i > 0:
                    print(f"  Добавлено {i} массивов...")
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Проверяем результат
            actual_count = self.db.get_array_count()
            success = actual_count == count
            
            details = f"Ожидалось: {count}, Сохранено: {arrays_processed}, В базе: {actual_count}"
            
            return success, execution_time, details
            
        except Exception as e:
            execution_time = time.time() - start_time if 'start_time' in locals() else 0
            return False, execution_time, f"Ошибка: {str(e)}"
    
    def test_b_sort_100_arrays_from_100(self):
        """
        Тест выгрузки и сортировки 100 массивов из базы на 100 записей
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
            # Заполняем базу данных случайными массивами до указанного размера
            print(f"Заполнение базы {db_size} записями...")
            for i in range(db_size):
                size = random.randint(10, 500)
                array = generate_random_array(size, -5000, 5000)
                self.db.save_array(self.user_id, array)
                
                if db_size >= 1000 and i % 1000 == 0 and i > 0:
                    print(f"  Добавлено {i} массивов...")
            
            # Проверяем, что база заполнена корректно
            actual_db_size = self.db.get_array_count()
            if actual_db_size != db_size:
                return False, 0, 0, f"База заполнена некорректно: {actual_db_size} вместо {db_size}"
            
            # Выполняем тест сортировки
            start_time = time.time()
            total_sort_time = 0
            arrays_processed = 0
            
            # Получаем случайные массивы из базы для сортировки
            arrays = self._get_random_arrays_from_db(sort_count)
            arrays_processed = len(arrays)
            
            # Сортируем каждый массив и замеряем время
            for i, array in enumerate(arrays):
                # Замеряем время сортировки одного массива
                sort_start = time.time()
                sorted_array = selection_sort(array)
                sort_end = time.time()
                
                total_sort_time += (sort_end - sort_start)
                
                # Проверяем корректность сортировки
                is_correctly_sorted = all(
                    sorted_array[i] <= sorted_array[i+1] 
                    for i in range(len(sorted_array)-1)
                )
                
                if not is_correctly_sorted:
                    return False, 0, 0, f"Массив {i} отсортирован некорректно"
            
            end_time = time.time()
            total_time = end_time - start_time
            avg_time_per_array = total_sort_time / arrays_processed if arrays_processed > 0 else 0
            
            details = f"Обработано массивов: {arrays_processed}, Общее время сортировки: {total_sort_time:.4f} сек"
            
            return True, total_time, avg_time_per_array, details
            
        except Exception as e:
            total_time = time.time() - start_time if 'start_time' in locals() else 0
            return False, total_time, 0, f"Ошибка: {str(e)}"
    
    def _get_random_arrays_from_db(self, count):
        """Получение случайных массивов из базы данных"""
        try:
            cursor = self.db.connection.execute(
                "SELECT original_array FROM arrays ORDER BY RANDOM() LIMIT ?",
                (count,)
            )
            results = cursor.fetchall()
            
            # Преобразуем JSON строки обратно в массивы
            arrays = []
            for row in results:
                try:
                    array = json.loads(row[0])
                    arrays.append(array)
                except:
                    pass
            
            return arrays
        except Exception as e:
            print(f"Ошибка получения массивов из базы: {e}")
            return []
    
    def test_c_clear_database_100(self):
        """
        Тест очистки базы данных с 100 записями
        """
        print("\n" + "="*60)
        print("ТЕСТ C: ОЧИСТКА БАЗЫ ДАННЫХ С 100 ЗАПИСЯМИ")
        print("="*60)
        
        success, execution_time, details = self._perform_clear_test(100)
        
        print(f"Флаг выполнения: {'УСПЕХ' if success else 'НЕУДАЧА'}")
        print(f"Время работы: {execution_time:.6f} секунд")
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
        print(f"Время работы: {execution_time:.6f} секунд")
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
        print(f"Время работы: {execution_time:.6f} секунд")
        print(f"Детали: {details}")
        
        self.assertTrue(success, "Тест очистки базы на 10000 не прошел")
    
    def _perform_clear_test(self, initial_count):
        """Вспомогательный метод для тестирования очистки базы данных"""
        try:
            # Заполняем базу данных указанным количеством записей
            print(f"Заполнение базы {initial_count} записями...")
            for i in range(initial_count):
                size = random.randint(10, 100)
                array = generate_random_array(size, -1000, 1000)
                self.db.save_array(self.user_id, array)
                
                if initial_count >= 1000 and i % 1000 == 0 and i > 0:
                    print(f"  Добавлено {i} массивов...")
            
            # Проверяем, что база заполнена корректно
            initial_db_count = self.db.get_array_count()
            if initial_db_count != initial_count:
                return False, 0, f"База заполнена некорректно: {initial_db_count} вместо {initial_count}"
            
            # Очищаем базу и замеряем время
            start_time = time.time()
            self.db.clear_database()
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            # Проверяем, что база действительно пуста
            final_db_count = self.db.get_array_count()
            success = final_db_count == 0
            
            details = f"Записей до очистки: {initial_db_count}, после очистки: {final_db_count}"
            
            return success, execution_time, details
            
        except Exception as e:
            execution_time = time.time() - start_time if 'start_time' in locals() else 0
            return False, execution_time, f"Ошибка: {str(e)}"


# Проверка что скрипт запущен напрямую (а не импортирован как модуль)
if __name__ == '__main__':
    # Запуск всех тестов в классе
    unittest.main()                                                     