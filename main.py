# Импорт модуля tkinter для создания графического интерфейса
import tkinter as tk
from database import DatabaseManager
from auth import AuthManager
from sorting import ArrayManager
from gui import SortingApp

def main():
    try:
        # Инициализация менеджера базы данных в основном режиме (не тестовом)
        db_manager = DatabaseManager(test_mode=False)
        
        # Создание менеджера аутентификации, передаем ему менеджер базы данных
        auth_manager = AuthManager(db_manager)
        
        # Создание менеджера массивов, передаем ему менеджер БД и менеджер аутентификации
        array_manager = ArrayManager(db_manager, auth_manager)
        
        # Корневое окно tkinter
        root = tk.Tk()
        
        # Создание экземпляра основного приложения, передаем все менеджеры
        app = SortingApp(root, db_manager, auth_manager, array_manager)
        
        # Запуск главного цикла обработки событий Tkinter
        # Программа будет работать пока не будет закрыто окно
        root.mainloop()
        
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
        input("Нажмите Enter для выхода...")

# Проверка, запущен ли скрипт напрямую (а не импортирован как модуль)
if __name__ == "__main__":
    # Если скрипт запущен напрямую, вызываем основную функциюё
    main()