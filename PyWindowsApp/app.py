import tkinter as tk
from tkinter import messagebox

def combine_texts():
    text1 = entry1.get().strip()
    text2 = entry2.get().strip()
    
    # Объединяем с пробелом, если оба не пустые
    combined = f"{text1} {text2}".strip()
    
    if not combined:
        messagebox.showwarning("Предупреждение", "Оба поля пусты!")
        entry3.delete(0, tk.END)
        entry3.insert(0, "")
    else:
        # Выводим в третье поле
        entry3.delete(0, tk.END)
        entry3.insert(0, combined)
        # Выводим во всплывающее окно
        messagebox.showinfo("Результат", f"Объединённый текст:\n{combined}")

def center_window(window, width, height):
    """Центрирует окно на экране"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Создаём главное окно
root = tk.Tk()
root.title("Объединение текста")

# Устанавливаем размер и центрируем
window_width = 500
window_height = 200
center_window(root, window_width, window_height)

# Метка
tk.Label(root, text="Введите текст в поля:").pack(pady=10)

# Рамка для двух полей рядом
frame = tk.Frame(root)
frame.pack(pady=5)

# Первое поле
tk.Label(frame, text="Поле 1:").grid(row=0, column=0, padx=5)
entry1 = tk.Entry(frame, width=20)
entry1.grid(row=0, column=1, padx=5)

# Второе поле
tk.Label(frame, text="Поле 2:").grid(row=0, column=2, padx=5)
entry2 = tk.Entry(frame, width=20)
entry2.grid(row=0, column=3, padx=5)

# Третье поле (результат)
tk.Label(root, text="Результат:").pack(pady=(15, 5))
entry3 = tk.Entry(root, width=50)
entry3.pack(pady=5)

# Кнопка
button = tk.Button(root, text="Объединить", command=combine_texts)
button.pack(pady=10)

# Запуск главного цикла
root.mainloop()