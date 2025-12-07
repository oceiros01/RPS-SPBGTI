import hashlib  # Модуль для хеширования паролей
import secrets  # Модуль для генерации криптографически безопасных случайных чисел
from typing import Tuple, Optional  # Аннотации типов для лучшей читаемости кода

class AuthManager:
    # Конструктор класса, инициализирует менеджер аутентификации
    def __init__(self, db_manager):
        # Сохраняем ссылку на менеджер базы данных для работы с пользователями
        self.db = db_manager
        # ID текущего аутентифицированного пользователя (None если не аутентифицирован)
        self.current_user = None
        # Имя текущего аутентифицированного пользователя (None если не аутентифицирован)
        self.current_username = None
    
    # Метод для хеширования пароля с использованием соли
    def hash_password(self, password: str) -> str:
        """Хеширование пароля"""
        # Генерируем случайную соль длиной 16 байт (32 символа в hex)
        salt = secrets.token_hex(16)
        # Создаем хеш пароля используя алгоритм PBKDF2-HMAC-SHA256
        # password.encode() - преобразуем пароль в байты
        # salt.encode() - преобразуем соль в байты
        # 100000 - количество итераций для замедления brute-force атак
        # .hex() - преобразуем байты в hex-строку
        # Возвращаем хеш и соль, разделенные двоеточием
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex() + ':' + salt
    
    # Метод для проверки соответствия введенного пароля сохраненному хешу
    def verify_password(self, stored_password: str, provided_password: str) -> bool:
        """Проверка пароля"""
        try:
            # Разделяем сохраненный пароль на хеш и соль по разделителю ':'
            password_hash, salt = stored_password.split(':')
            # Вычисляем хеш введенного пароля с той же солью и сравниваем с сохраненным
            return password_hash == hashlib.pbkdf2_hmac(
                'sha256', provided_password.encode(), salt.encode(), 100000
            ).hex()
        except:
            # Если произошла ошибка (неправильный формат), возвращаем False
            return False
    
    # Метод для регистрации нового пользователя
    def register(self, username: str, password: str) -> Tuple[bool, str]:
        """Регистрация пользователя"""
        # Проверяем минимальную длину имени пользователя
        if len(username) < 3:
            # Возвращаем False и сообщение об ошибке
            return False, "Имя пользователя должно содержать минимум 3 символа"
        # Проверяем минимальную длину пароля
        if len(password) < 6:
            # Возвращаем False и сообщение об ошибке
            return False, "Пароль должен содержать минимум 6 символов"
        
        # Хешируем пароль перед сохранением в базу
        password_hash = self.hash_password(password)
        # Пытаемся зарегистрировать пользователя в базе данных
        success = self.db.register_user(username, password_hash)
        
        # Проверяем результат регистрации
        if success:
            # Если успешно, возвращаем True и сообщение об успехе
            return True, "Регистрация успешна"
        else:
            # Если неуспешно (скорее всего пользователь уже существует), возвращаем False и сообщение
            return False, "Пользователь с таким именем уже существует"
    
    # Метод для аутентификации пользователя
    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """Аутентификация пользователя"""
        try:
            # Получаем хеш пароля из базы данных для указанного пользователя
            cursor = self.db.connection.execute(
                "SELECT id, password_hash FROM users WHERE username = ?",
                (username,)  # Параметризованный запрос для безопасности
            )
            # Получаем первую строку результата
            result = cursor.fetchone()
        
            # Проверяем, найден ли пользователь
            if not result:
                # Если пользователь не найден, возвращаем ошибку
                return False, "Пользователь не найден"
            
            # Проверяем соответствие введенного пароля сохраненному хешу
            if self.verify_password(result['password_hash'], password):
                # Если пароль верный, сохраняем информацию о текущем пользователе
                self.current_user = result['id']  # Сохраняем ID пользователя
                self.current_username = username  # Сохраняем имя пользователя
                # Возвращаем успешный результат
                return True, "Вход выполнен успешно"
            else:
                # Если пароль неверный, возвращаем ошибку
                return False, "Неверный пароль"
        except Exception as e:
            # Если произошла любая другая ошибка, возвращаем сообщение об ошибке
            return False, f"Ошибка авторизации: {str(e)}"
    
    # Метод для выхода пользователя из системы
    def logout(self):
        """Выход пользователя"""
        # Сбрасываем ID текущего пользователя
        self.current_user = None
        # Сбрасываем имя текущего пользователя
        self.current_username = None
    
    # Метод для проверки, аутентифицирован ли текущий пользователь
    def is_authenticated(self) -> bool:
        """Проверка аутентификации"""
        # Возвращает True если current_user не None (пользователь аутентифицирован)
        return self.current_user is not None
    
    # Метод для получения имени текущего аутентифицированного пользователя
    def get_current_username(self) -> str:
        """Получение имени текущего пользователя"""
        # Возвращает имя пользователя или пустую строку если пользователь не аутентифицирован
        return self.current_username or ""