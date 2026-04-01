from selection_sort import selection_sort
from additional import display_menu, get_choice, input_array_from_keyboard, display_arrays, generate_random_array, load_array_from_file, offer_file_save


while True:
        display_menu()
        choice = get_choice("Выберите действие (1-4): ", 1, 4)
        
        if choice == 1:
            # Ввод с клавиатуры
            original_arr = input_array_from_keyboard()
        
        elif choice == 2:
            # Генерация случайного массива
            original_arr = generate_random_array()
        
        elif choice == 3:
            # Загрузка из файла
            filename = input("Введите имя файла: ")
            original_arr = load_array_from_file(filename)
            if original_arr is None:
                continue
        
        elif choice == 4:
            # Выход
            print("До свидания!")
            break
        
        # Сортировка массива
        print("\nВыполняется сортировка...")
        sorted_arr = selection_sort(original_arr)
        
        # Вывод результатов
        display_arrays(original_arr, sorted_arr)
        
        #  Предложение сохранить в файл
        offer_file_save(original_arr, sorted_arr)

