import csv
import re
import os
from datetime import datetime

# === 0. Декоратор ===
def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = (
                f"{timestamp} - Вызов функции {old_function.__name__}\n"
                f"  Аргументы: {signature}\n"
                f"  Результат: {result}\n"
            )
            with open(path, "a", encoding="utf-8") as log_file:
                log_file.write(log_message)
            return result
        return new_function
    return __logger

# === 1. Читаем файл ===
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# === 2. Очистка и разбиение ФИО для ВСЕХ строк ===
for i in range(1, len(contacts_list)):
    contact = contacts_list[i]
    # Объединяем первые 3 поля и разбиваем на части
    full_name = " ".join([contact[j].strip() for j in range(3) if contact[j]])
    parts = [p for p in full_name.split() if p]  # убираем пустые

    # Заполняем поля: максимум 3 части
    for j in range(3):
        contact[j] = parts[j] if j < len(parts) else ""

# === 3. Форматирование телефонов ===
phone_pattern = r'(?:\+7|8)[\s\-\(]*(\d{3})[\s\-\)]*(\d{3})[\s\-]*(\d{2})[\s\-]*(\d{2})(?:\s*(?:[\(\s]?(?:доб\.?|ext\.?|x)\.?\s*)?(\d{2,6}))?'
pattern = re.compile(phone_pattern, re.IGNORECASE)


@logger('log_10.log')
def replace_phone(match):
    code = match.group(1)
    num3 = match.group(2)
    num2_1 = match.group(3)
    num2_2 = match.group(4)
    ext = match.group(5)
    formatted = f"+7({code}){num3}-{num2_1}-{num2_2}"
    if ext:
        formatted += f" доб.{ext}"
    return formatted

for i in range(1, len(contacts_list)):
    phone = contacts_list[i][5]
    if phone and phone.strip():
        cleaned_phone = pattern.sub(replace_phone, phone)
        contacts_list[i][5] = cleaned_phone

# === 4. Объединение дубликатов по (фамилия, имя) с использованием unique_fio ===

# Собираем unique_fio из ОЧИЩЕННЫХ данных
fio = []
seen = set()
unique_fio = []

for contact in contacts_list[1:]:
    lastname = contact[0].strip()
    firstname = contact[1].strip()
    surname = contact[2].strip()
    key = (lastname, firstname)

    if key not in seen:
        seen.add(key)
        # Сохраняем только ФИО — остальное соберём позже
        unique_fio.append([lastname, firstname, surname])

# Создаём словарь для объединения
merged = {}
for fio_entry in unique_fio:
    key = (fio_entry[0], fio_entry[1])
    merged[key] = [""] * 7
    merged[key][0] = fio_entry[0]
    merged[key][1] = fio_entry[1]
    merged[key][2] = fio_entry[2]

# Заполняем данными из всех строк
for contact in contacts_list[1:]:
    lastname = contact[0].strip()
    firstname = contact[1].strip()
    key = (lastname, firstname)

    if key in merged:
        target = merged[key]
        for i in range(3, 7):  # organization, position, phone, email
            value = contact[i].strip() if contact[i] else ""
            if value and not target[i]:
                target[i] = value

# === 5. Собираем итоговый список в порядке unique_fio ===
contacts_list_updated = [contacts_list[0]]  # заголовок
for fio_entry in unique_fio:
    key = (fio_entry[0], fio_entry[1])
    if key in merged:
        contacts_list_updated.append(merged[key])

# === 6. Сохраняем в файл ===
with open("../phonebook.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(contacts_list_updated)

print("✅ Готово! Файл 'phonebook.csv' успешно сохранён.")