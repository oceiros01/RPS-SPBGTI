import random
import json
import unittest
import sys
import os
from pathlib import Path

def display_menu():  # Отображение главного меню
    print("\n" + "="*50)
    print("          ПРОГРАММА СОРТИРОВКИ МАССИВОВ")
    print("="*50)
    print("1. Ввод массива с клавиатуры")
    print("2. Генерация массива случайных чисел")
    print("3. Загрузка массива из файла")
    print("4. Выход")
    print("="*50)

def get_choice(prompt, min_val, max_val):
    while True:
        try:
            choice = int(input(prompt))
            if min_val <= choice <= max_val:
                return choice
            else:
                print(f"Пожалуйста, введите число от {min_val} до {max_val}")
        except ValueError:
            print("Пожалуйста, введите целое число")

def display_arrays(original_arr, sorted_arr):
    #Отображает исходный и отсортированный массивы
    print("\n" + "-"*50)
    print("РЕЗУЛЬТАТЫ:")
    print("-"*50)
    print(f"Исходный массив:    {original_arr}")
    print(f"Отсортированный массив: {sorted_arr}")



def input_array_from_keyboard():
    print("\n--- Ввод массива с клавиатуры ---")

    while True:
        try:
            n = int(input("Введите количество элементов массива: "))
            if n <= 0:
                print("Количество элементов должно быть положительным числом")
                continue
            break
        except ValueError:
            print("Пожалуйста, введите целое число")
    
    arr = []
    print("Введите элементы массива:")
    for i in range(n):
        while True:
            try:
                element = int(input(f"Элемент {i + 1}: "))
                arr.append(element)
                break
            except ValueError:
                print("Пожалуйста, введите целое число")
    
    return arr

def generate_random_array():
    #Генерация массива случайных чисел

    print("\n--- Генерация массива случайных чисел ---")
    
    while True:
        try:
            n = int(input("Введите количество элементов массива: "))
            if n <= 0:
                print("Количество элементов должно быть положительным числом")
                continue
            
            min_val = int(input("Введите минимальное значение: "))
            max_val = int(input("Введите максимальное значение: "))
            
            if min_val > max_val:
                print("Минимальное значение не может быть больше максимального")
                continue
            
            break
        except ValueError:
            print("Пожалуйста, введите целое число")
    
    arr = [random.randint(min_val, max_val) for _ in range(n)]
    print(f"Сгенерирован массив из {n} элементов")
    
    return arr



def is_system_filename(filename):
    # Проверяет, является ли имя файла системным
    if not filename or not filename.strip():
        return True
    
    filename = filename.strip().lower()
    
    # Системные имена в Windows
    windows_system_names = {
        'con', 'prn', 'aux', 'nul',
        'com1', 'com2', 'com3', 'com4', 'com5', 'com6', 'com7', 'com8', 'com9',
        'lpt1', 'lpt2', 'lpt3', 'lpt4', 'lpt5', 'lpt6', 'lpt7', 'lpt8', 'lpt9'
    }
    
    # Системные имена в Unix/Linux
    unix_system_names = {
        '.', '..', '/', '\\'
    }
    
    # Общие системные имена и расширения
    common_system_names = {
        'desktop.ini', 'thumbs.db', '.ds_store', '.localized',
        'hosts', 'passwd', 'shadow', 'group', 'sudoers'
    }
    
    # Получаем имя файла без пути и расширения
    base_name = os.path.splitext(filename)[0].lower()
    # basename извлекает имя без пути
    
    # Проверяем системные имена
    if (base_name in windows_system_names or
        base_name in unix_system_names or
        filename.lower() in common_system_names or
        any(char in filename for char in ['<', '>', ':', '"', '|', '?', '*'])):
        return True
    
    # Проверяем зарезервированные слова в начале имени
    reserved_prefixes = ['~$', '~', '.~']
    for prefix in reserved_prefixes:
        if filename.startswith(prefix):
            return True
    
    return False


def is_valid_filename(filename):
    # Проверяет валидность имени файла

    if not filename or not filename.strip():
        return False, "Имя файла не может быть пустым"
    
    filename = filename.strip()
    
    # Проверка на системные имена
    if is_system_filename(filename):
        return False, f"Имя файла '{filename}' является системным или зарезервированным"
    
    # Проверка на недопустимые символы
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
    for char in invalid_chars:
        if char in filename:
            return False, f"Имя файла содержит недопустимый символ: '{char}'"
    
    # Проверка длины имени файла
    if len(filename) > 255:
        return False, "Имя файла слишком длинное (максимум 255 символов)"
    
    # Проверка на точки в конце (проблема в Windows)
    if filename.endswith('.') or filename.endswith(' '):
        return False, "Имя файла не может заканчиваться точкой или пробелом"
    
    # Проверка на специальные устройства (Unix/Linux)
    if filename.startswith('/dev/'):
        return False, "Имя файла не может ссылаться на устройства системы"
    
    return True, "Имя файла валидно"

def ensure_txt_extension(filename):
    # Добавляет расширение .txt если его нет
    if not filename.lower().endswith('.txt'):
        return filename + '.txt'
    return filename



def load_array_from_file(filename):
    # Проверяем валидность имени файла
    is_valid, error_message = is_valid_filename(filename)
    if not is_valid:
        print(f"Ошибка: {error_message}")
        return None
    
    filename = ensure_txt_extension(filename)
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Пытаемся найти массив в текстовом файле
        # Ищем строку, содержащую массив в формате [1, 2, 3, 4, 5]
        lines = content.split('\n')
        array_line = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                array_line = line
                break
        
        if not array_line:
            print(f"Ошибка: в файле {filename} не найден массив в формате [1, 2, 3, ...]")
            return None
        
        # Извлекаем массив из строки
        try:
            # Убираем квадратные скобки и разбиваем по запятым
            array_str = array_line[1:-1]  # убираем [ и ]
            if not array_str.strip():  # пустой массив
                return []
            
            elements = array_str.split(',')
            arr = []
            
            for element in elements:
                element = element.strip()
                if element:  # пропускаем пустые элементы
                    # Пробуем преобразовать в int, если не получается - в float
                    try:
                        num = int(element)
                    except ValueError:
                        num = float(element)
                    arr.append(num)
            
            print(f"Массив успешно загружен из текстового файла: {filename}")
            return arr
            
        except ValueError as e:
            print(f"Ошибка: не удалось преобразовать элементы массива в числа: {e}")
            return None
        
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден")
        return None
    except PermissionError:
        print(f"Ошибка: нет прав для чтения файла {filename}")
        return None
    except OSError as e:
        print(f"Ошибка ОС при чтении файла {filename}: {e}")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return None


def save_both_arrays_to_file(original_arr, sorted_arr, filename):
    # Сохраняет оба массива (исходный и отсортированный) в один файл
    # Проверяем валидность имени файла
    is_valid, error_message = is_valid_filename(filename)
    if not is_valid:
        print(f"Ошибка: {error_message}")
        return False
    
    # Обеспечиваем расширение .txt
    filename = ensure_txt_extension(filename)
    
    try:
        # открываем файл для ЗАПИСИ ('w')
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("ИСХОДНЫЙ МАССИВ:\n")
            file.write("-" * 20 + "\n")
            file.write("[" + ", ".join(map(str, original_arr)) + "]\n")
            file.write(f"Количество элементов: {len(original_arr)}\n\n")
            
            file.write("ОТСОРТИРОВАННЫЙ МАССИВ:\n")
            file.write("-" * 25 + "\n")
            file.write("[" + ", ".join(map(str, sorted_arr)) + "]\n")
            file.write(f"Количество элементов: {len(sorted_arr)}\n\n")
            
        print(f"✅ Оба массива успешно сохранены в текстовый файл: {filename}")
        return True
        
    except PermissionError:
        print(f"Ошибка: нет прав для записи в файл {filename}")
        return False
    except OSError as e:
        print(f"Ошибка ОС при сохранении файла {filename}: {e}")
        return False
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return False




def offer_file_save(original_arr, sorted_arr):
    # Предлагает пользователю сохранить массивы в файлы
    while True:
        save_choice = input("\nХотите сохранить массивы в файлы? (y/n): ").lower().strip()
        
        if save_choice == 'y':
            # Зацикливаем до успешного сохранения
            while True:
                filename = input("Введите имя файла для сохранения массивов: ")
                # Обеспечиваем расширение .txt
                filename = ensure_txt_extension(filename)


                # Пытаемся сохранить
                success = save_both_arrays_to_file(original_arr, sorted_arr, filename)
                
                if success:
                    print("Файл успешно сохранен!")
                    return  # Выходим из функции после успешного сохранения
                else:
                    print("Не удалось сохранить файл. Попробуйте снова.\n")
                    
                    while True:
                        retry = input("Хотите попробовать другое имя файла? (y/n): ").lower().strip()
                        
                        if retry == 'y':
                            break  # Выходим во внутренний цикл для новой попытки сохранения
                        elif retry == 'n':
                            print("Сохранение отменено.")
                            return  # Полностью выходим из функции
                        else:
                            print("Пожалуйста, введите 'y' или 'n'")
                    # После break продолжаем внутренний цикл 
        
        elif save_choice == 'n':
            print("Сохранение отменено.")
            break
        else:
            print("Пожалуйста, введите 'y' для да или 'n' для нет.")



