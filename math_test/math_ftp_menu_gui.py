import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from ftplib import FTP
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

# Соответствие кнопок и файлов на сервере
FILE_MAP = {
    "Сложение": "sum.json",
    "Вычитание": "minus.json",
    "Умножение": "multiply.json",
    "Деление": "divide.json"
}

class MathFTPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Математика")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(padx=20, pady=20)

        self.problems = []
        self.current_index = 0
        self.selected_file = None

        self.main_menu()

    def main_menu(self):
        """Главное меню с выбором типа примеров"""
        self.clear_window()

        tk.Label(self.root, text="Выберите тип примеров:",
                 font=("Arial", 16, "bold"), justify="center").pack(pady=40)

        for title in FILE_MAP.keys():
            btn = tk.Button(self.root, text=title, font=("Arial", 14), width=20, height=2,
                            command=lambda t=title: self.start_problems(t))
            btn.pack(pady=10)

    def start_problems(self, topic):
        """Начать решение примеров по выбранной теме"""
        self.selected_file = FILE_MAP[topic]
        self.load_from_ftp()

    def load_from_ftp(self):
        """Скачивание выбранного файла с FTP"""
        self.show_status_window(f"Загрузка {self.selected_file}...")

        try:
            with FTP(FTP_HOST) as ftp:
                ftp.login(FTP_USER, FTP_PASS)
                with open(LOCAL_FILE, 'wb') as f:
                    ftp.retrbinary(f'RETR {self.selected_file}', f.write)
            self.status_window.destroy()

            with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
                self.problems = json.load(f)

            self.current_index = 0
            self.open_problems_window()

        except Exception as e:
            self.status_window.destroy()
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{self.selected_file}\n\n{e}")
            self.main_menu()

    def show_status_window(self, message):
        """Показывает окно ожидания"""
        self.status_window = tk.Toplevel(self.root)
        self.status_window.title("Подождите")
        self.status_window.geometry("300x100")
        self.status_window.resizable(False, False)
        self.status_window.grab_set()  # Блокировка главного окна

        tk.Label(self.status_window, text=message, font=("Arial", 10), wraplength=250).pack(pady=20)
        self.status_window.transient(self.root)

    def open_problems_window(self):
        """Открывает окно с примерами"""
        self.clear_window()

        self.root.geometry("500x600")

        # Заголовок
        tk.Label(self.root, text=f"Тема: {self.get_topic_name()}",
                 font=("Arial", 14, "bold"), fg="blue").pack(pady=10)

        self.problem_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.problem_label.pack(pady=20)

        self.answer_entry = tk.Entry(self.root, font=("Arial", 14), justify='center')
        self.answer_entry.pack(pady=10, padx=50, fill='x')
        self.answer_entry.bind('<Return>', lambda e: self.save_answer())

        # Кнопки
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        self.prev_btn = tk.Button(btn_frame, text="Назад", width=10, command=self.prev_problem)
        self.prev_btn.grid(row=0, column=0, padx=5)

        self.next_btn = tk.Button(btn_frame, text="Далее", width=10, command=self.next_problem)
        self.next_btn.grid(row=0, column=1, padx=5)

        self.submit_btn = tk.Button(btn_frame, text="Проверить", width=10, command=self.save_answer)
        self.submit_btn.grid(row=0, column=2, padx=5)

        # Статус
        self.status_label = tk.Label(self.root, text="", fg="gray")
        self.status_label.pack(pady=5)

        # Прогресс
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        self.update_navigation()
        self.update_progress()
        self.show_current_problem()

        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def get_topic_name(self):
        for name, fname in FILE_MAP.items():
            if fname == self.selected_file:
                return name
        return "Примеры"

    def show_current_problem(self):
        if not self.problems:
            return

        item = self.problems[self.current_index]
        problem = item.get("problem", "Ошибка")
        user_answer = item.get("user_answer")

        self.problem_label.config(text=f"{problem} = ?")

        if user_answer is not None:
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.insert(0, str(user_answer))
        else:
            self.answer_entry.delete(0, tk.END)

        self.update_navigation()
        self.update_progress()

    def save_answer(self):
        if not self.problems:
            return

        try:
            answer = self.answer_entry.get().strip()
            if not answer:
                messagebox.showwarning("Ввод", "Введите ответ!")
                return

            num_answer = float(answer) if '.' in answer else int(answer)
            item = self.problems[self.current_index]
            item['user_answer'] = num_answer

            # Проверка (если есть правильный ответ)
            correct = item.get("correct_answer")
            if correct is not None:
                is_correct = abs(num_answer - correct) < 1e-6
                msg = "✅ Верно!" if is_correct else f"❌ Неверно. Правильно: {correct}"
                messagebox.showinfo("Результат", msg)

            self.update_progress()
            self.next_problem()

        except ValueError:
            messagebox.showerror("Ошибка", "Введите число!")

    def prev_problem(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_current_problem()

    def next_problem(self):
        if self.current_index < len(self.problems) - 1:
            self.current_index += 1
            self.show_current_problem()

    def update_navigation(self):
        self.prev_btn.config(state='normal' if self.current_index > 0 else 'disabled')
        self.next_btn.config(state='normal' if self.current_index < len(self.problems) - 1 else 'disabled')

    def update_progress(self):
        if not self.problems:
            return
        solved = sum(1 for p in self.problems if p.get("user_answer") is not None)
        total = len(self.problems)
        self.progress['value'] = (solved / total) * 100
        self.status_label.config(text=f"Решено: {solved} из {total}")

    def on_closing(self):
        if messagebox.askyesno("Выход", "Сохранить ответы на сервере?"):
            self.save_to_ftp()
        self.cleanup()
        self.root.quit()

    def save_to_ftp(self):
        """Сохраняет изменения обратно на FTP-сервер"""
        try:
            # Сохраняем текущие данные локально
            with open(LOCAL_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.problems, f, ensure_ascii=False, indent=2)

            # Подключаемся к FTP и загружаем файл
            with FTP(FTP_HOST) as ftp:
                ftp.login(FTP_USER, FTP_PASS)
                with open(LOCAL_FILE, 'rb') as f:
                    ftp.storbinary(f'STOR {self.selected_file}', f)

            messagebox.showinfo("Успех", f"Ответы сохранены:\n{self.selected_file}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

    def cleanup(self):
        """Удаляет временный локальный файл"""
        if os.path.exists(LOCAL_FILE):
            try:
                os.remove(LOCAL_FILE)
            except:
                pass  # Игнорируем ошибки удаления

    def clear_window(self):
        """Очищает все виджеты окна"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_status_window(self, message):
        """Показывает окно ожидания при загрузке"""
        self.status_window = tk.Toplevel(self.root)
        self.status_window.title("Подождите")
        self.status_window.geometry("300x100")
        self.status_window.resizable(False, False)
        self.status_window.grab_set()  # Блокировка главного окна

        tk.Label(self.status_window, text=message, font=("Arial", 10), wraplength=250).pack(pady=20)
        self.status_window.transient(self.root)
        self.root.update_idletasks()

    def get_topic_name(self):
        """Возвращает название темы по имени файла"""
        for name, fname in FILE_MAP.items():
            if fname == self.selected_file:
                return name
        return "Примеры"


# ================ Запуск приложения ================
if __name__ == "__main__":
    root = tk.Tk()
    app = MathFTPApp(root)
    root.mainloop()