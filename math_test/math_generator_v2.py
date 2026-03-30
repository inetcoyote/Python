import json
import random
from ftplib import FTP

def generate_math_problems(max_sum=20, count=10):
    """
    Генерирует математические задачи на сложение и вычитание,
    где сумма в сложении не превышает max_sum, а в вычитании уменьшаемое <= max_sum.
    Задачи перемешаны в случайном порядке.
    :param max_sum: максимальная сумма (для сложения) или уменьшаемое (для вычитания)
    :param count: количество задач
    :return: список задач в формате JSON
    """
    problems = []

    while len(problems) < count:
        # Случайно выбираем тип задачи
        operation = random.choice(['add', 'sub'])

        if operation == 'add':
            # Генерируем a + b, где a + b <= max_sum
            total = random.randint(2, max_sum)  # сумма от 2 до max_sum
            a = random.randint(1, total - 1)
            b = total - a
            problem = f"{a} + {b}"
            correct_answer = total
            problems.append({
                "problem": problem,
                "user_answer": None,
                "correct_answer": correct_answer
            })

        else:  # operation == 'sub'
            # a - b, где a <= max_sum, b <= a
            a = random.randint(2, max_sum)  # уменьшаемое от 2 до max_sum
            b = random.randint(1, a)
            problem = f"{a} - {b}"
            correct_answer = a - b
            problems.append({
                "problem": problem,
                "user_answer": None,
                "correct_answer": correct_answer
            })

    # Перемешиваем задачи
    random.shuffle(problems)
    return problems

def upload_to_ftp(file_path, ftp_host, ftp_user, ftp_pass, remote_dir, remote_filename):
    """
    Загружает файл на FTP-сервер.
    """
    with FTP(ftp_host) as ftp:
        ftp.login(ftp_user, ftp_pass)
        print(f"✅ Подключено к FTP: {ftp_host}")

        try:
            ftp.cwd(remote_dir)
            print(f"📁 Перешли в папку: {remote_dir}")
        except Exception as e:
            print(f"❌ Ошибка при переходе в папку {remote_dir}: {e}")
            return

        with open(file_path, 'rb') as file:
            ftp.storbinary(f'STOR {remote_filename}', file)
            print(f"📤 Файл {remote_filename} успешно загружен!")

# === Настройки ===
LOCAL_FILE = 'problems.json'
FTP_HOST = 'your.ftp.server.com'     # заменить
FTP_USER = 'your_username'           # заменить
FTP_PASS = 'your_password'           # заменить
REMOTE_DIR = '/public/problems'      # заменить
REMOTE_FILENAME = 'problems.json'
MAX_SUM = 20                         # Максимальная сумма (для +) или уменьшаемое (для -)
PROBLEM_COUNT = 10

# === Генерация и загрузка ===
if __name__ == "__main__":
    problems = generate_math_problems(max_sum=MAX_SUM, count=PROBLEM_COUNT)

    # Сохранение в JSON
    with open(LOCAL_FILE, 'w', encoding='utf-8') as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)
    print(f"📝 Сгенерировано {len(problems)} задач с суммой/уменьшаемым до {MAX_SUM}")
    print(f"📄 Файл сохранён: {LOCAL_FILE}")

    # Загрузка на FTP
    upload_to_ftp(LOCAL_FILE, FTP_HOST, FTP_USER, FTP_PASS, REMOTE_DIR, REMOTE_FILENAME)