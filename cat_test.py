import requests

# Твой текст для картинки
text = "MyCat"

# Собираем адрес
url = f"https://cataas.com/cat/says/{text}"

print("Отправляем запрос на cataas.com...")

# Делаем запрос
response = requests.get(url)

# Проверяем статус ответа
if response.status_code == 200:
    print("Картинка получена!")
    
    # Сохраняем файл, чтобы ты мог его открыть и посмотреть
    file_name = f"{text}.jpg"
    with open(file_name, "wb") as f:
        f.write(response.content)
    
    print(f"Файл сохранен как {file_name}")
else:
    print("Что-то пошло не так. Код ошибки:", response.status_code)