import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from typing import List, Dict, Any
from .sorting import ArrayManager, generate_random_array
from .auth import AuthManager

# __init__ - это специальный метод в Python, который автоматически 
# вызывается при создании нового объекта класса, настраивает начальное состояние класса.
# self - ссылка на сам объект, через него устанавливаем атрибуты объекта, объекты доступны
# внутри класса

class SortingApp:
    def __init__(self, root, db_manager, auth_manager, array_manager):
        self.root = root
        self.db = db_manager
        self.auth = auth_manager
        self.array_manager = array_manager
        
        self.setup_ui()
        self.show_login_frame()
    
    def setup_ui(self):
        """метод инициализации пользовательского интерфейса"""
        self.root.title("Программа сортировки массивов")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Стили
        # Создаем объект для управления стилями ttk-виджетов
        # ttk (themed tkinter) - современные стилизованные виджеты
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        
        # Основные фреймы
        # Создаем контейнер(фрейм) из родительского контейнера
        self.login_frame = ttk.Frame(self.root)
        self.main_frame = ttk.Frame(self.root)
        
        self.setup_login_frame() # фрейм для авторизации 
        self.setup_main_frame() # фрейм для справки, истории, сортировки
    
    def setup_login_frame(self):
        """Настройка фрейма авторизации"""
        
        # ссылка на фрейм авторизации
        frame = self.login_frame
        
        # Заголовок
        header = ttk.Label(frame, text="АВТОРИЗАЦИЯ", style='Header.TLabel')
        header.pack(pady=20)
        
        # Поля ввода
        # создаем отдельный фрем для логина и пароля
        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Логин:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.login_entry = ttk.Entry(input_frame, width=20)
        self.login_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Пароль:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.password_entry = ttk.Entry(input_frame, width=20, show='*')
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Кнопки
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        
        # при нажатии вызываются методы login и show_register
        ttk.Button(button_frame, text="Войти", command=self.login).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Регистрация", command=self.show_register).pack(side='left', padx=5)
        
        # Статус (сообщения об ошибках)
        self.login_status = ttk.Label(frame, text="", foreground='red')
        self.login_status.pack(pady=5)
    
    def setup_main_frame(self):
        """Настройка основного фрейма"""
        # Верхняя панель
        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(top_frame, text="Программа сортировки массивов", style='Header.TLabel').pack(side='left')
        ttk.Button(top_frame, text="Выйти", command=self.logout).pack(side='right')
        
        # Панель пользователя
        user_frame = ttk.Frame(self.main_frame)
        user_frame.pack(fill='x', padx=10, pady=5)
        
        self.user_label = ttk.Label(user_frame, text="")
        self.user_label.pack(side='left')
        
        # Notebook(контейнер) для вкладок
        # fill='x' растягивает на всю ширину
        # fill='both', expand=True  растягивает на всё доступное пространство
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.setup_input_tab()
        self.setup_history_tab()
        self.setup_help_tab()
    
    def setup_input_tab(self):
        """Вкладка ввода и сортировки"""
        input_tab = ttk.Frame(self.notebook)
        self.notebook.add(input_tab, text="Сортировка")
        
        # Выбор способа ввода
        method_frame = ttk.LabelFrame(input_tab, text="Способ ввода")
        method_frame.pack(fill='x', padx=5, pady=5)
        
        self.input_method = tk.StringVar(value="keyboard")
        ttk.Radiobutton(method_frame, text="Ввод с клавиатуры", 
                       variable=self.input_method, value="keyboard").pack(anchor='w')
        ttk.Radiobutton(method_frame, text="Генерация случайного массива", 
                       variable=self.input_method, value="random").pack(anchor='w')
        
        # Параметры ввода
        self.input_frame = ttk.Frame(input_tab)
        self.input_frame.pack(fill='x', padx=5, pady=5)
        
        self.setup_keyboard_input()
        self.setup_random_input()
        
        # Кнопки действий
        action_frame = ttk.Frame(input_tab)
        action_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(action_frame, text="Сортировать", command=self.sort_array).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Очистить", command=self.clear_input).pack(side='left', padx=5)
        
        # Результаты
        result_frame = ttk.LabelFrame(input_tab, text="Результаты")
        result_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=10, width=80)
        self.result_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Привязка событий
        self.input_method.trace('w', self.on_input_method_change)
    
    def setup_keyboard_input(self):
        """Настройка ввода с клавиатуры"""
        self.keyboard_frame = ttk.Frame(self.input_frame)
        
        ttk.Label(self.keyboard_frame, text="Введите массив (через запятую):").pack(anchor='w')
        self.array_entry = ttk.Entry(self.keyboard_frame, width=50)
        self.array_entry.pack(fill='x', pady=5)
        
        ttk.Label(self.keyboard_frame, text="Пример: 5, 2, 8, 1, 9").pack(anchor='w')
    
    def setup_random_input(self):
        """Настройка генерации случайного массива"""
        self.random_frame = ttk.Frame(self.input_frame)
        
        param_frame = ttk.Frame(self.random_frame)
        param_frame.pack(fill='x', pady=5)
        
        ttk.Label(param_frame, text="Размер:").grid(row=0, column=0, padx=5, sticky='e')
        self.size_entry = ttk.Entry(param_frame, width=10)
        self.size_entry.grid(row=0, column=1, padx=5)
        self.size_entry.insert(0, "10")
        
        ttk.Label(param_frame, text="Мин:").grid(row=0, column=2, padx=5, sticky='e')
        self.min_entry = ttk.Entry(param_frame, width=10)
        self.min_entry.grid(row=0, column=3, padx=5)
        self.min_entry.insert(0, "-100")
        
        ttk.Label(param_frame, text="Макс:").grid(row=0, column=4, padx=5, sticky='e')
        self.max_entry = ttk.Entry(param_frame, width=10)
        self.max_entry.grid(row=0, column=5, padx=5)
        self.max_entry.insert(0, "100")
    
    def setup_history_tab(self):
        """Вкладка истории"""
        history_tab = ttk.Frame(self.notebook)
        self.notebook.add(history_tab, text="История")
        
        # Панель управления
        control_frame = ttk.Frame(history_tab)
        control_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(control_frame, text="Обновить", command=self.load_history).pack(side='left', padx=5)
        
        # Таблица истории
        columns = ('id', 'size', 'is_sorted', 'created_at')
        self.history_tree = ttk.Treeview(history_tab, columns=columns, show='headings')
        
        self.history_tree.heading('id', text='ID')
        self.history_tree.heading('size', text='Размер')
        self.history_tree.heading('is_sorted', text='Отсортирован')
        self.history_tree.heading('created_at', text='Дата создания')
        
        self.history_tree.column('id', width=50)
        self.history_tree.column('size', width=80)
        self.history_tree.column('is_sorted', width=100)
        self.history_tree.column('created_at', width=150)
        
        scrollbar = ttk.Scrollbar(history_tab, orient='vertical', command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Детали
        detail_frame = ttk.LabelFrame(history_tab, text="Детали массива")
        detail_frame.pack(fill='x', padx=5, pady=5)
        
        self.detail_text = scrolledtext.ScrolledText(detail_frame, height=8, width=80)
        self.detail_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.history_tree.bind('<<TreeviewSelect>>', self.on_history_select)
    
    def setup_help_tab(self):
        """Вкладка справки"""
        help_tab = ttk.Frame(self.notebook)
        self.notebook.add(help_tab, text="Справка")
        
        help_text = """
        РУКОВОДСТВО ПОЛЬЗОВАТЕЛЯ

        1. АВТОРИЗАЦИЯ
           - Для использования программы необходимо зарегистрироваться или войти
           - Логин должен содержать минимум 3 символа
           - Пароль должен содержать минимум 6 символов

        2. СОРТИРОВКА МАССИВОВ
           - Выберите способ ввода: с клавиатуры или генерация случайного массива
           - Для ввода с клавиатуры: введите числа через запятую
           - Для генерации: укажите размер массива и диапазон значений
           - Нажмите "Сортировать" для выполнения сортировки

        3. ИСТОРИЯ
           - Просматривайте ранее сохраненные массивы
           - Нажмите на запись для просмотра деталей
           - Используйте "Обновить" для обновления списка

        4. СОХРАНЕНИЕ
           - Массивы автоматически сохраняются в базу данных
           - Сохраняются как исходные, так и отсортированные массивы

        Алгоритм: сортировка выбором
        Сложность: O(n²)
        """
        
        help_widget = scrolledtext.ScrolledText(help_tab, wrap='word')
        help_widget.insert('1.0', help_text)
        help_widget.config(state='disabled')
        help_widget.pack(fill='both', expand=True, padx=10, pady=10)
    
    def on_input_method_change(self, *args):
        """Обработка изменения способа ввода"""
        for widget in self.input_frame.winfo_children():
            widget.pack_forget()
        
        if self.input_method.get() == "keyboard":
            self.keyboard_frame.pack(fill='x', pady=5)
        else:
            self.random_frame.pack(fill='x', pady=5)
    
    def show_login_frame(self):
        """Показать фрейм авторизации"""
        self.main_frame.pack_forget()
        self.login_frame.pack(fill='both', expand=True)
    
    def show_main_frame(self):
        """Показать основной фрейм"""
        self.login_frame.pack_forget()
        self.main_frame.pack(fill='both', expand=True)
        self.load_history()
    
    def login(self):
        """Вход пользователя"""
        username = self.login_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            self.login_status.config(text="Заполните все поля")
            return
        
        success, message = self.auth.login(username, password)
        
        if success:
            self.user_label.config(text=f"Пользователь: {username}")
            self.show_main_frame()
            self.login_status.config(text="")
            self.login_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
        else:
            self.login_status.config(text=message)
    
    def show_register(self):
        """Показать диалог регистрации"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Регистрация")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Регистрация", style='Header.TLabel').pack(pady=10)
        
        ttk.Label(dialog, text="Логин:").pack()
        username_entry = ttk.Entry(dialog, width=20)
        username_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Пароль:").pack()
        password_entry = ttk.Entry(dialog, width=20, show='*')
        password_entry.pack(pady=5)
        
        status_label = ttk.Label(dialog, text="", foreground='red')
        status_label.pack(pady=5)
        
        def register():
            username = username_entry.get().strip()
            password = password_entry.get()
            
            success, message = self.auth.register(username, password)
            
            if success:
                messagebox.showinfo("Успех", message)
                dialog.destroy()
            else:
                status_label.config(text=message)
        
        ttk.Button(dialog, text="Зарегистрироваться", command=register).pack(pady=10)
    
    def logout(self):
        """Выход пользователя"""
        self.auth.logout()
        self.show_login_frame()
    
    def parse_array_input(self, text: str) -> List[int]:
        """Парсинг ввода массива"""
        try:
            return [int(x.strip()) for x in text.split(',') if x.strip()]
        except ValueError:
            raise ValueError("Некорректный формат массива")
    
    def sort_array(self):
        """Сортировка массива"""
        try:
            if self.input_method.get() == "keyboard":
                array_text = self.array_entry.get()
                array = self.parse_array_input(array_text)
            else:
                size = int(self.size_entry.get())
                min_val = int(self.min_entry.get())
                max_val = int(self.max_entry.get())
                array = generate_random_array(size, min_val, max_val)
            
            if not array:
                messagebox.showerror("Ошибка", "Массив не может быть пустым")
                return
            
            result = self.array_manager.process_array(array, True, True)
            
            if result["success"]:
                self.display_result(result)
            else:
                messagebox.showerror("Ошибка", result["message"])
                
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    
    def display_result(self, result: Dict[str, Any]):
        """Отображение результатов сортировки"""
        output = f"""РЕЗУЛЬТАТЫ СОРТИРОВКИ:
        {'-' * 50}

        Исходный массив:
        {result['original_array']}

        Отсортированный массив:
        {result['sorted_array']}

        Время сортировки: {result['sorting_time']:.6f} секунд
        Размер массива: {len(result['original_array'])} элементов

        Статус сохранения: Успешно сохранено в базу данных
        """
                
        self.result_text.delete('1.0', 'end')
        self.result_text.insert('1.0', output)
    
    def clear_input(self):
        """Очистка полей ввода"""
        self.array_entry.delete(0, 'end')
        self.result_text.delete('1.0', 'end')
    
    def load_history(self):
        """Загрузка истории массивов пользователя"""
        try:
            # Получаем историю массивов из менеджера
            history = self.array_manager.get_user_history()
            
            # Очистка таблицы истории
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            
            # Заполнение таблицы данными
            for item in history:
                # Просто используем строковое представление даты
                # SQLite возвращает дату как строку, так что оставляем как есть
                date_str = str(item['created_at'])
                
                # Вставляем данные в таблицу
                self.history_tree.insert('', 'end', values=(
                    item['id'],  # ID массива
                    item['array_size'],  # Размер массива
                    'Да' if item['is_sorted'] else 'Нет',  # Статус сортировки
                    date_str  # Дата как строка
                ))
        except Exception as e:
            print(f"Ошибка загрузки истории: {e}")
            # Показываем сообщение об ошибке пользователю
            messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {e}")
    
    def on_history_select(self, event):
        """Обработка выбора элемента в истории"""
        try:
            # Получаем выбранные элементы
            selection = self.history_tree.selection()
            if not selection:
                return  # Если ничего не выбрано - выход
            
            # Получаем ID выбранного элемента
            item_id = self.history_tree.item(selection[0])['values'][0]
            # Получаем всю историю пользователя
            history = self.array_manager.get_user_history()
            
            # Ищем выбранный элемент в истории
            selected_item = next((item for item in history if item['id'] == item_id), None)
            if not selected_item:
                return  # Если элемент не найден - выход
            
            # Просто используем строковое представление даты
            date_str = str(selected_item['created_at'])
            
            # Формируем текст с деталями массива
            detail_text = f"""ДЕТАЛИ МАССИВА (ID: {selected_item['id']})
            {'-' * 40}

            Размер: {selected_item['array_size']} элементов
            Отсортирован: {'Да' if selected_item['is_sorted'] else 'Нет'}
            Дата создания: {date_str}

            Исходный массив:
            {selected_item['original_array']}

            """
            
            # Добавляем информацию об отсортированном массиве если он есть
            if selected_item['sorted_array']:
                detail_text += f"""Отсортированный массив:
                                {selected_item['sorted_array']}
                                """
            
            # Очищаем поле деталей и вставляем новую информацию
            self.detail_text.delete('1.0', 'end')
            self.detail_text.insert('1.0', detail_text)
        except Exception as e:
            print(f"Ошибка отображения деталей: {e}")
            # Показываем сообщение об ошибке пользователю
            messagebox.showerror("Ошибка", f"Не удалось отобразить детали: {e}")