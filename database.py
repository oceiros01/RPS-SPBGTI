import sqlite3
import json
from datetime import datetime
import os
from typing import List, Dict, Any, Optional

class DatabaseManager:
    def __init__(self, test_mode=False):
        # Определяем путь к базе данных в зависимости от режима
        if test_mode:
            self.db_path = "sorting_test.db"
        else:
            self.db_path = "sorting_app.db"
        
        # Инициализируем соединение
        self.connection = None
        # Подключаемся к базе данных
        self.connect()
        # Инициализируем структуру базы данных
        self.init_database()
    
    def connect(self):
        """Установка соединения с базой данных SQLite"""
        try:
            # Создаем соединение с SQLite базой данных
            self.connection = sqlite3.connect(self.db_path)
            # Устанавливаем фабрику строк для удобства работы
            self.connection.row_factory = sqlite3.Row
            print(f"Успешное подключение к базе данных: {self.db_path}")
        except Exception as e:
            # Выводим сообщение об ошибке и пробрасываем исключение
            print(f"Ошибка подключения к базе данных: {e}")
            raise
    
    def init_database(self):
        """Инициализация таблиц в базе данных"""
        try:
            # Используем контекстный менеджер для автоматического коммита
            with self.connection:
                # Создаем таблицу пользователей если она не существует
                self.connection.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Создаем таблицу массивов если она не существует
                self.connection.execute("""
                    CREATE TABLE IF NOT EXISTS arrays (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER REFERENCES users(id),
                        original_array TEXT NOT NULL,
                        sorted_array TEXT,
                        is_sorted BOOLEAN DEFAULT FALSE,
                        array_size INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            print("Таблицы базы данных успешно инициализированы")
        except Exception as e:
            print(f"Ошибка инициализации базы данных: {e}")
            raise
    
    def register_user(self, username: str, password_hash: str) -> bool:
        """Регистрация нового пользователя"""
        try:
            # Используем контекстный менеджер для автоматического коммита
            with self.connection:
                # Вставляем нового пользователя в таблицу
                self.connection.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash)
                )
            print(f"Пользователь {username} успешно зарегистрирован")
            return True
        except sqlite3.IntegrityError:
            # Ошибка возникает если пользователь с таким именем уже существует
            print(f"Пользователь с именем {username} уже существует")
            return False
        except Exception as e:
            print(f"Ошибка регистрации пользователя: {e}")
            return False
    
    def authenticate_user(self, username: str, password_hash: str) -> Optional[int]:
        """Аутентификация пользователя"""
        try:
            # Выполняем запрос для поиска пользователя
            cursor = self.connection.execute(
                "SELECT id FROM users WHERE username = ? AND password_hash = ?",
                (username, password_hash)
            )
            # Получаем результат запроса
            result = cursor.fetchone()
            # Возвращаем ID пользователя если найден, иначе None
            return result['id'] if result else None
        except Exception as e:
            print(f"Ошибка аутентификации: {e}")
            return None
    
    def save_array(self, user_id: int, original_array: List[int], sorted_array: List[int] = None) -> int:
        """Сохранение массива в базу данных"""
        try:
            # Используем контекстный менеджер для автоматического коммита
            with self.connection:
                # Вставляем массив в таблицу arrays
                cursor = self.connection.execute("""
                    INSERT INTO arrays (user_id, original_array, sorted_array, is_sorted, array_size)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    user_id, 
                    json.dumps(original_array),  # Сериализуем массив в JSON
                    json.dumps(sorted_array) if sorted_array else None,  # Сериализуем отсортированный массив или NULL
                    sorted_array is not None,  # Флаг указывающий есть ли отсортированная версия
                    len(original_array)  # Сохраняем размер массива
                ))
                # Возвращаем ID созданной записи
                return cursor.lastrowid
        except Exception as e:
            print(f"Ошибка сохранения массива: {e}")
            return -1
    
    def get_user_arrays(self, user_id: int) -> List[Dict[str, Any]]:
        """Получение массивов пользователя"""
        try:
            # Выполняем запрос для получения массивов пользователя
            cursor = self.connection.execute("""
                SELECT id, original_array, sorted_array, is_sorted, array_size, created_at
                FROM arrays 
                WHERE user_id = ? 
                ORDER BY created_at DESC
            """, (user_id,))
            
            # Создаем список для результатов
            results = []
            # Обрабатываем каждую строку результата
            for row in cursor.fetchall():
                # Преобразуем строку в словарь
                result = dict(row)
                # Десериализуем JSON обратно в список Python
                result['original_array'] = json.loads(result['original_array'])
                # Если есть отсортированный массив, тоже десериализуем
                if result['sorted_array']:
                    result['sorted_array'] = json.loads(result['sorted_array'])
                # Добавляем результат в список
                results.append(result)
            
            return results
        except Exception as e:
            print(f"Ошибка получения массивов пользователя: {e}")
            return []
    
    def get_random_arrays(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Получение случайных массивов для тестов"""
        try:
            # Выполняем запрос для получения случайных массивов
            cursor = self.connection.execute("""
                SELECT id, original_array, sorted_array, is_sorted, array_size
                FROM arrays 
                ORDER BY RANDOM()
                LIMIT ?
            """, (limit,))
            
            # Создаем список для результатов
            results = []
            # Обрабатываем каждую строку результата
            for row in cursor.fetchall():
                # Преобразуем строку в словарь
                result = dict(row)
                # Десериализуем JSON обратно в список Python
                result['original_array'] = json.loads(result['original_array'])
                # Если есть отсортированный массив, тоже десериализуем
                if result['sorted_array']:
                    result['sorted_array'] = json.loads(result['sorted_array'])
                # Добавляем результат в список
                results.append(result)
            
            return results
        except Exception as e:
            print(f"Ошибка получения случайных массивов: {e}")
            return []
    
    def clear_database(self):
        """Очистка базы данных (для тестов)"""
        try:
            # Используем контекстный менеджер для автоматического коммита
            with self.connection:
                # Удаляем все записи из таблицы массивов
                self.connection.execute("DELETE FROM arrays")
                # Удаляем все записи из таблицы пользователей
                self.connection.execute("DELETE FROM users")
                # Сбрасываем счетчики автоинкремента
                self.connection.execute("DELETE FROM sqlite_sequence WHERE name IN ('arrays', 'users')")
            print("База данных успешно очищена")
        except Exception as e:
            print(f"Ошибка очистки базы данных: {e}")
    
    def get_array_count(self) -> int:
        """Получение количества массивов в базе"""
        try:
            # Выполняем запрос для подсчета массивов
            cursor = self.connection.execute("SELECT COUNT(*) FROM arrays")
            # Возвращаем количество массивов
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Ошибка получения количества массивов: {e}")
            return 0
    
    def close(self):
        """Закрытие соединения с базой данных"""
        # Проверяем что соединение существует
        if self.connection:
            # Закрываем соединение
            self.connection.close()
            print("Соединение с базой данных закрыто")