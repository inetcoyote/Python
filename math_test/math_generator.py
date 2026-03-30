import json
import random
from ftplib import FTP

def generate_math_problems(max_num=20, count=10):
    """
    Генерирует список математических задач на сложение и вычитание.
    :param max_num: максимальное число в задаче
    :param count: количество задач
    :return: список задач в формате JSON
    """
    problems = []

    # Генерация задач на сложение
    for _ in range(count // 2):
        a = random.randint(1, max_num)
        b = random.randint(1, max_num)
        problem = f"{a} + {b}"
        correct_answer = a + b
        problems.append({
            "problem": problem,
            "user_answer": None,
            "correct_answer": correct_answer
        })

    # Генерация задач на вычитание (с положительным результатом)
    for _ in range(count - len(problems)):
        a = random.randint(1, max_num)
        b = random.randint(1, max_num)
        #b = random.randint(1, a)  # чтобы a - b >= 0
        problem = f"{a} - {b}"
        correct_answer = a - b
        problems.append({
            "problem": problem,
            "user_answer": None,
            "correct_answer": correct_answer
        })
    # Перемешиваем задачи, чтобы не было паттернов
    random.shuffle(problems)
    return problems

def upload_to_ftp(file_path, ftp_host, ftp_user, ftp_pass, remote_dir, remote_filename):
    """
    Загружает файл на FTP-сервер.
    :param file_path: локальный путь к файлу
    :param ftp_host: адрес FTP-сервера
    :param ftp_user: логин
    :param ftp_pass: пароль
    :param remote_dir: папка на сервере
    :param remote_filename: имя файла на сервере
    """
    with FTP(ftp_host) as ftp:
        ftp.login(ftp_user, ftp_pass)
        print(f"✅ Подключено к FTP: {ftp_host}")

        # Переход в нужную директорию
        try:
            ftp.cwd(remote_dir)
            print(f"📁 Перешли в папку: {remote_dir}")
        except Exception as e:
            print(f"❌ Ошибка при переходе в папку {remote_dir}: {e}")
            return

        # Загрузка файла
        with open(file_path, 'rb') as file:
            ftp.storbinary(f'STOR {remote_filename}', file)
            print(f"📤 Файл {remote_filename} успешно загружен!")

# === Настройки ===
LOCAL_FILE = 'problems.json'         # временный локальный файл
FTP_HOST = 'your.ftp.server.com'     # замените на реальный хост
FTP_USER = 'your_username'           # замените
FTP_PASS = 'your_password'           # замените
REMOTE_DIR = '/public/problems'      # папка на сервере (должна существовать)
REMOTE_FILENAME = 'problems.json'    # имя файла на сервере
MAX_NUM = 20                         # числа до 20
PROBLEM_COUNT = 10                   # количество задач

# === Генерация и загрузка ===
if __name__ == "__main__":
    # Генерация задач
    problems = generate_math_problems(max_num=MAX_NUM, count=PROBLEM_COUNT)

    # Сохранение в локальный JSON
    with open(LOCAL_FILE, 'w', encoding='utf-8') as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)
    print(f"📝 Сгенерировано {len(problems)} задач и сохранено в {LOCAL_FILE}")

    # Загрузка на FTP
    upload_to_ftp(LOCAL_FILE, FTP_HOST, FTP_USER, FTP_PASS, REMOTE_DIR, REMOTE_FILENAME)