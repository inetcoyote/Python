import json
import random
from ftplib import FTP

def generate_math_problems(max_result=20, count=10):
    """
    Генерирует УНИКАЛЬНЫЕ задачи на умножение и деление.
    Каждый пример встречается только один раз.
    """
    examples = set()

    # Собираем все возможные примеры в виде уникальных строк
    # Умножение: a × b (результат <= max_result)
    for a in range(1, max_result + 1):
        for b in range(1, max_result + 1):
            product = a * b
            if product <= max_result:
                problem_str = f"{a} × {b}"
                examples.add((problem_str, product))

    # Деление: a ÷ b (a делится на b, a <= max_result)
    for a in range(1, max_result + 1):
        for b in range(1, a + 1):
            if a % b == 0:
                problem_str = f"{a} ÷ {b}"
                quotient = a // b
                examples.add((problem_str, quotient))

    # Преобразуем в список и перемешиваем
    examples_list = list(examples)  # Уникальность уже обеспечена множеством
    random.shuffle(examples_list)

    # Берём не больше, чем есть
    if len(examples_list) < count:
        print(f"⚠️ Внимание: найдено только {len(examples_list)} уникальных примеров. Выбираем все.")
        count = len(examples_list)

    # Выбираем первые 'count' уникальных примеров
    problems = []
    for problem_str, answer in examples_list[:count]:
        problems.append({
            "problem": problem_str,
            "user_answer": None,
            "correct_answer": answer
        })

    # Перемешиваем окончательный список
    random.shuffle(problems)
    return problems

def upload_to_ftp(file_path, ftp_host, ftp_user, ftp_pass, remote_dir, remote_filename):
    """Загружает файл на FTP-сервер."""
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
LOCAL_FILE = 'multiplication_division_unique.json'
FTP_HOST = 'your.ftp.server.com'
FTP_USER = 'your_username'
FTP_PASS = 'your_password'
REMOTE_DIR = '/public/problems'
REMOTE_FILENAME = 'problems_md.json'
MAX_RESULT = 20
PROBLEM_COUNT = 20

# === Генерация и загрузка ===
if __name__ == "__main__":
    try:
        problems = generate_math_problems(max_result=MAX_RESULT, count=PROBLEM_COUNT)

        # Сохранение в JSON
        with open(LOCAL_FILE, 'w', encoding='utf-8') as f:
            json.dump(problems, f, ensure_ascii=False, indent=2)
        print(f"📝 Сгенерировано {len(problems)} УНИКАЛЬНЫХ задач (× и ÷) с результатом/делимым до {MAX_RESULT}")
        print(f"📄 Файл сохранён: {LOCAL_FILE}")

        # Загрузка на FTP
        upload_to_ftp(LOCAL_FILE, FTP_HOST, FTP_USER, FTP_PASS, REMOTE_DIR, REMOTE_FILENAME)

    except Exception as e:
        print(f"❌ Ошибка: {e}")