import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from ftplib import FTP  # Простой FTP (без шифрования)
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

class MathFTPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Математические примеры")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.problems = []
        self.current_index = 0

        self.setup_ui()
        self.load_problems()

    def setup_ui(self):
        # Заголовок
        self.title_label = tk.Label(self.root, text="Решите примеры:", font=("Arial", 14, "bold"))
        self.title_label.pack(pady=10)

        # Пример
        self.problem_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.problem_label.pack(pady=20)

        # Поле ввода
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

        # Статус и прогресс
        self.status_label = tk.Label(self.root, text="", fg="gray")
        self.status_label.pack(pady=5)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

    def load_problems(self):
        self.set_status("Загрузка с FTP...")
        try:
            with FTP(FTP_HOST) as ftp:
                ftp.login(FTP_USER, FTP_PASS)

                with open(LOCAL_FILE, 'wb') as f:
                    ftp.retrbinary(f'RETR {REMOTE_FILE}', f.write)
                self.set_status("Файл загружен.")

            with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
                self.problems = json.load(f)

            self.update_progress()
            self.show_current_problem()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")
            self.root.quit()

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

            # Проверка ответа (если указан правильный)
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

    def set_status(self, text):
        self.status_label.config(text=text)
        self.root.update_idletasks()

    def on_closing(self):
        if messagebox.askyesno("Выход", "Сохранить ответы на сервере?"):
            self.save_to_ftp()
        self.cleanup()
        self.root.quit()

    def save_to_ftp(self):
        try:
            # Сохраняем изменения локально
            with open(LOCAL_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.problems, f, ensure_ascii=False, indent=2)

            # Загружаем обратно на FTP
            with FTP(FTP_HOST) as ftp:
                ftp.login(FTP_USER, FTP_PASS)
                with open(LOCAL_FILE, 'rb') as f:
                    ftp.storbinary(f'STOR {REMOTE_FILE}', f)
            messagebox.showinfo("Успех", "Ответы сохранены на сервере!")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить:\n{e}")

    def cleanup(self):
        """Удаляет временный файл при выходе"""
        if os.path.exists(LOCAL_FILE):
            try:
                os.remove(LOCAL_FILE)
            except:
                pass  # Игнорируем ошибки

# ================ Запуск приложения ================
if __name__ == "__main__":
    root = tk.Tk()
    app = MathFTPApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()