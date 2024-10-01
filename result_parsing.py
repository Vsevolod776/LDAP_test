import pandas as pd

# Указываем путь к текстовому файлу
file_path = "/Users/vsevolodovcinnikov/Desktop/result_add.txt"

# Считываем данные из файла
data = []
real, user_time, sys, log = None, None, None, None

# Считывание файла с обработкой пустых строк и корректной проверкой
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()  # Удаляем пробелы и символы новой строки
        if not line:  # Пропускаем пустые строки
            continue

        # Проверяем каждую строку и разделяем по табуляции
        parts = line.split('\t')  # Разделяем строку по символу табуляции
        print(f"Обработка строки: {line}, Части: {parts}")  # Отладочный вывод

        if len(parts) < 2 and not "is done!" in line:  # Если строка не содержит табуляцию или не является логом, переходим к следующей
            continue

        if parts[0] == "real":
            real = parts[1] if len(parts) > 1 else None  # Извлекаем значение времени "real"
            print(f"Извлечено real: {real}")
        elif parts[0] == "user":
            user_time = parts[1] if len(parts) > 1 else None  # Извлекаем значение времени "user"
            print(f"Извлечено user_time: {user_time}")
        elif parts[0] == "sys":
            sys = parts[1] if len(parts) > 1 else None  # Извлекаем значение времени "sys"
            print(f"Извлечено sys: {sys}")
        elif "is done!" in line:  # Проверяем наличие "is done!" в строке
            log = line  # Извлекаем лог сообщение
            print(f"Извлечен лог: {log}")
            # Проверяем, чтобы все значения (real, user, sys) были определены перед добавлением в таблицу
            if real and user_time and sys:
                data.append([real, user_time, sys, log])  # Добавляем строку данных
                print(f"Добавлена строка данных: {[real, user_time, sys, log]}")
                real, user_time, sys, log = None, None, None, None  # Сбрасываем значения для следующей группы
            else:
                print("Пропуск строки, так как отсутствуют значения real, user_time или sys.")

print(f"Считано строк данных: {len(data)}")
if not data:
    print("Ошибка: данные не были извлечены из файла. Проверьте формат файла.")

# Создание DataFrame с данными
df = pd.DataFrame(data, columns=["Real", "User Time", "Sys", "Log"])

# Проверка содержания DataFrame
print("Содержимое DataFrame:")
print(df.head())  # Отображаем первые несколько строк

# Указываем путь для сохранения Excel файла
output_excel_path = "/Users/vsevolodovcinnikov/Desktop/parsing_result_add.xlsx"

# Сохраняем DataFrame в Excel
df.to_excel(output_excel_path, index=False)
print(f"Данные успешно сохранены в {output_excel_path}")
