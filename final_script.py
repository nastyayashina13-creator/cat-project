import requests
import json
import os


print("--- Программа резервного копирования котов ---")
TEXT = input("Введите текст для картинки: ")
YANDEX_TOKEN = input("Введите токен Яндекс.Диска: ")


GROUP_NAME = "AIE-TRF-8" 


print("\nСкачиваем картинку...")
cat_url = f"https://cataas.com/cat/says/{TEXT}"
cat_response = requests.get(cat_url)
cat_response.raise_for_status()
image_data = cat_response.content
file_name = f"{TEXT}.jpg"
file_size = len(image_data)
print(f"Картинка скачана. Размер: {file_size} байт")


headers = {"Authorization": f"OAuth {YANDEX_TOKEN}"}
folder_path = f"/{GROUP_NAME}"

print(f"Создаем папку '{GROUP_NAME}'...")
create_folder_response = requests.put(
    "https://cloud-api.yandex.net/v1/disk/resources",
    headers=headers,
    params={"path": folder_path}
)
if create_folder_response.status_code == 201:
    print("Папка создана.")
elif create_folder_response.status_code == 409:
    print("Папка уже существует, используем её.")
else:
    print("Ошибка при создании папки:", create_folder_response.status_code)


print("Загружаем файл на Яндекс.Диск...")
upload_url_response = requests.get(
    "https://cloud-api.yandex.net/v1/disk/resources/upload",
    headers=headers,
    params={"path": f"{folder_path}/{file_name}", "overwrite": "true"}
)
upload_url_response.raise_for_status()
upload_url = upload_url_response.json()["href"]

upload_response = requests.put(upload_url, data=image_data)
upload_response.raise_for_status()
print(f"Файл '{file_name}' загружен в папку '{GROUP_NAME}'.")


print("Сохраняем информацию в json-файл...")
result = {
    "file_name": file_name,
    "size": file_size
}
with open("result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print("Готово! Информация сохранена в result.json")