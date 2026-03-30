import json
import os
from ftplib import FTP
import getpass
from decouple import config


# Настройки FTP
#FTP_HOST = "your.ftp.server.com"
FTP_HOST = config('FTP_HOST', default='')
#FTP_USER = "username"
FTP_USER = config('FTP_USER', default='')
#FTP_PASS = "password"
FTP_PASS = config('FTP_PASS', default='')
REMOTE_FILE = "math_test/math_test.json"  # Путь к файлу на сервере
LOCAL_FILE = "math_test_local.json"  # Локальная копия

# Пример структуры JSON на сервере:
# [
#   {"problem": "2 + 3", "user_answer": null, "correct_answer": 5},
#   {"problem": "10 - 4", "user_answer": null, "correct_answer": 6}
# ]

def download_from_ftp():
    """Скачивает файл с FTP"""
    try:
        with FTP(FTP_HOST) as ftp:
            ftp.login(FTP_USER, FTP_PASS)
            with open(LOCAL_FILE, 'wb') as f:
                ftp.retrbinary(f'RETR {REMOTE_FILE}', f.write)
            print(f"[✓] Файл '{REMOTE_FILE}' успешно загружен.")
    except Exception as e:
        print(f"[✗] Ошибка при загрузке: {e}")
        exit()

def upload_to_ftp():
    """Загружает файл обратно на FTP"""
    try:
        with FTP(FTP_HOST) as ftp:
            ftp.login(FTP_USER, FTP_PASS)
            with open(LOCAL_FILE, 'rb') as f:
                ftp.storbinary(f'STOR {REMOTE_FILE}', f)
            print(f"[✓] Ответы сохранены на сервере.")
    except Exception as e:
        print(f"[✗] Ошибка при выгрузке: {e}")

def solve_problems():
    """Загружает примеры и предлагает решить"""
    if not os.path.exists(LOCAL_FILE):
        print(f"[✗] Локальный файл {LOCAL_FILE} не найден.")
        exit()

    with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
        try:
            problems = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[✗] Ошибка чтения JSON: {e}")
            exit()

    print("\nРешите следующие математические примеры:\n")

    for i, item in enumerate(problems):
        problem = item.get("problem", "")
        user_answer = item.get("user_answer")
        if user_answer is not None:
            print(f"Пример {i+1}: {problem} = {user_answer} (уже решён)")
            continue

        while True:
            try:
                answer = input(f"{i+1}. {problem} = ")
                item["user_answer"] = float(answer) if '.' in answer else int(answer)
                break
            except ValueError:
                print("❌ Пожалуйста, введите число.")
                continue

    # Сохраняем изменения локально
    with open(LOCAL_FILE, 'w', encoding='utf-8') as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)

    print("\n✅ Все примеры решены!")

def main():
    print("📥 Скачивание заданий с FTP...")
    download_from_ftp()

    solve_problems()

    save = input("\n📤 Сохранить ответы на сервере? (y/n): ").strip().lower()
    if save in ('y', 'yes', 'д', 'да'):
        upload_to_ftp()
    else:
        print("❌ Ответы не были сохранены на сервере.")

    # Опционально: удалить локальный файл
    # os.remove(LOCAL_FILE)

if __name__ == "__main__":
    main()