import requests

# --- НАСТРОЙКИ ---
# ВАЖНО: Замени на название своей группы (как в Нетологии)
GROUP_NAME = "AIE-TRF-8"

# Вставь сюда свой токен (в кавычках)
YANDEX_TOKEN = "ТВОЙ_ТОКЕН"

# Текст, который был на картинке
TEXT = "MyCat"

# --- 1. Загружаем картинку с cataas.com в память ---
print("Скачиваем картинку с cataas.com...")
cat_url = f"https://cataas.com/cat/says/{TEXT}"
cat_response = requests.get(cat_url)
cat_response.raise_for_status()
image_data = cat_response.content
file_name = f"{TEXT}.jpg"
print(f"Картинка скачана. Размер: {len(image_data)} байт")

# --- 2. Создаем папку на Яндекс.Диске ---
headers = {"Authorization": f"OAuth {YANDEX_TOKEN}"}
folder_path = f"/{GROUP_NAME}"

print(f"Создаем папку '{GROUP_NAME}' на Яндекс.Диске...")
# Метод PUT создает папку. Если папка уже есть, вернется ошибка 409, но это не страшно.
create_folder_response = requests.put(
    "https://cloud-api.yandex.net/v1/disk/resources",
    headers=headers,
    params={"path": folder_path}
)

if create_folder_response.status_code == 201:
    print("Папка успешно создана.")
elif create_folder_response.status_code == 409:
    print("Папка уже существует. Будем использовать её.")
else:
    print("Ошибка при создании папки:", create_folder_response.status_code, create_folder_response.text)

# --- 3. Получаем ссылку для загрузки файла ---
print("Получаем ссылку для загрузки файла...")
upload_url_response = requests.get(
    "https://cloud-api.yandex.net/v1/disk/resources/upload",
    headers=headers,
    params={"path": f"{folder_path}/{file_name}", "overwrite": "true"}
)
upload_url_response.raise_for_status()
upload_url = upload_url_response.json()["href"]

# --- 4. Загружаем файл ---
print("Загружаем файл на Яндекс.Диск...")
upload_response = requests.put(upload_url, data=image_data)
upload_response.raise_for_status()

print(f"Готово! Файл '{file_name}' загружен в папку '{GROUP_NAME}' на Яндекс.Диске.")