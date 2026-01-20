import tkinter as tk
from tkinter import messagebox, LabelFrame
import kociemba

class RubiksCubeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Решатель кубика Рубика 3x3")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        # Цвета для граней
        self.colors = {
            'W': '#FFFFFF',  # Белый
            'Y': '#FFFF00',  # Желтый
            'R': '#FF0000',  # Красный
            'O': '#FFA500',  # Оранжевый
            'G': '#00FF00',  # Зеленый
            'B': '#0000FF',  # Синий
        }
        self.color_names = {
            'W': 'Белый (U)',
            'Y': 'Желтый (D)',
            'R': 'Красный (F)',
            'O': 'Оранжевый (B)',
            'G': 'Зеленый (L)',
            'B': 'Синий (R)'
        }

        # Текущий выбранный цвет
        self.selected_color = 'W'

        # Состояние кубика: 6 граней 3x3
        self.cube_state = {
            'U': [['W' for _ in range(3)] for _ in range(3)],
            'D': [['Y' for _ in range(3)] for _ in range(3)],
            'F': [['R' for _ in range(3)] for _ in range(3)],
            'B': [['O' for _ in range(3)] for _ in range(3)],
            'L': [['G' for _ in range(3)] for _ in range(3)],
            'R': [['B' for _ in range(3)] for _ in range(3)]
        }

        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        title = tk.Label(self.root, text="Решатель кубика Рубика 3x3", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        # Выбор цвета
        color_frame = tk.Frame(self.root)
        color_frame.pack(pady=10)

        tk.Label(color_frame, text="Выберите цвет: ", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        for color_key, color_hex in self.colors.items():
            btn = tk.Button(
                color_frame,
                bg=color_hex,
                width=3,
                height=1,
                command=lambda c=color_key: self.set_color(c)
            )
            btn.pack(side=tk.LEFT, padx=5)
            # Подсказка
            tk.Label(color_frame, text=self.color_names[color_key].split()[0], font=("Arial", 8)).pack(side=tk.LEFT)

        # Отображение граней
        faces_frame = tk.Frame(self.root)
        faces_frame.pack(pady=10)

        # Расположение граней: U, L F R B, D
        self.face_frames = {}

        # Верхняя грань (U)
        self.face_frames['U'] = self.create_face(faces_frame, 'Верх (U)', 0, 1)

        # Средний ряд: L, F, R, B
        self.face_frames['L'] = self.create_face(faces_frame, 'Лево (L)', 1, 0)
        self.face_frames['F'] = self.create_face(faces_frame, 'Перед (F)', 1, 1)
        self.face_frames['R'] = self.create_face(faces_frame, 'Право (R)', 1, 2)
        self.face_frames['B'] = self.create_face(faces_frame, 'Зад (B)', 1, 3)

        # Нижняя грань (D)
        self.face_frames['D'] = self.create_face(faces_frame, 'Низ (D)', 2, 1)

        # Кнопки управления
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Собрать по умолчанию", font=("Arial", 12), command=self.load_solved).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Решить кубик", font=("Arial", 12), bg="lightgreen", command=self.solve_cube).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Очистить всё", font=("Arial", 12), command=self.clear_all).pack(side=tk.LEFT, padx=5)

        # Результат
        result_frame = LabelFrame(self.root, text="Решение", font=("Arial", 12))
        result_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.solution_text = tk.Text(result_frame, height=8, font=("Courier", 11), state="disabled")
        self.solution_text.pack(padx=10, pady=10, fill="both", expand=True)

    def create_face(self, parent, name, row, col):
        frame = LabelFrame(parent, text=name, font=("Arial", 10))
        frame.grid(row=row, column=col, padx=10, pady=10)

        buttons = []
        face_key = name[0]  # U, D, F, B, L, R

        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = tk.Button(
                    frame,
                    bg=self.colors[self.cube_state[face_key][i][j]],
                    width=4,
                    height=2,
                    command=lambda f=face_key, x=i, y=j: self.set_tile(f, x, y)
                )
                btn.grid(row=i, column=j, padx=1, pady=1)
                row_buttons.append(btn)
            buttons.append(row_buttons)
        return buttons

    def set_color(self, color):
        self.selected_color = color
        messagebox.showinfo("Цвет выбран", f"Выбран цвет: {self.color_names[color]}")

    def set_tile(self, face, x, y):
        self.cube_state[face][x][y] = self.selected_color
        self.face_frames[face][x][y].config(bg=self.colors[self.selected_color])

    def load_solved(self):
        """Загрузка собранного кубика"""
        self.cube_state = {
            'U': [['W' for _ in range(3)] for _ in range(3)],
            'D': [['Y' for _ in range(3)] for _ in range(3)],
            'F': [['R' for _ in range(3)] for _ in range(3)],
            'B': [['O' for _ in range(3)] for _ in range(3)],
            'L': [['G' for _ in range(3)] for _ in range(3)],
            'R': [['B' for _ in range(3)] for _ in range(3)]
        }
        self.update_display()

    def clear_all(self):
        """Очистка всех граней (можно заполнить вручную)"""
        for face in self.cube_state:
            for i in range(3):
                for j in range(3):
                    self.cube_state[face][i][j] = 'W'  # По умолчанию белый
        self.update_display()

    def update_display(self):
        """Обновление отображения всех кнопок"""
        for face in self.cube_state:
            for i in range(3):
                for j in range(3):
                    color = self.cube_state[face][i][j]
                    self.face_frames[face][i][j].config(bg=self.colors[color])

def to_kociemba_string(self):
    """
    Преобразование в строку для kociemba:
    Порядок: U, R, F, D, L, B — по 9 элементов
    Каждая грань читается слева направо, сверху вниз.
    """
    face_order = ['U', 'R', 'F', 'D', 'L', 'B']
    color_map = {
        'W': 'U',  # White  -> Up
        'Y': 'D',  # Yellow -> Down
        'R': 'F',  # Red    -> Front
        'O': 'B',  # Orange -> Back
        'G': 'L',  # Green  -> Left
        'B': 'R'   # Blue   -> Right
    }

    sticker_string = ""
    for face in face_order:
        for i in range(3):
            for j in range(3):
                sticker_string += color_map[self.cube_state[face][i][j]]

    return sticker_string

def validate_cube(self):
    """
    Проверка корректности состояния кубика:
    - По 9 наклеек каждого цвета
    - Корректная компоновка (упрощённая проверка)
    """
    count = {'W': 0, 'Y': 0, 'R': 0, 'O': 0, 'G': 0, 'B': 0}

    for face in self.cube_state.values():
        for row in face:
            for cell in row:
                if cell in count:
                    count[cell] += 1

    # Проверяем, что по 9 наклеек каждого цвета
    for color, cnt in count.items():
        if cnt != 9:
            return False, f"Цвет {self.color_names[color].split()[0]} встречается {cnt} раз вместо 9"

    return True, "Корректно"

def solve_cube(self):
    """Решение кубика"""
    # Проверка корректности
    is_valid, message = self.validate_cube()
    if not is_valid:
        messagebox.showerror("Ошибка ввода", message)
        return

    # Преобразуем в строку для kociemba
    try:
        kociemba_str = self.to_kociemba_string()
        solution = kociemba.solve(kociemba_str)

        # Отображение результата
        self.solution_text.config(state="normal")
        self.solution_text.delete(1.0, tk.END)
        self.solution_text.insert(tk.END, f"Найдено решение:\n\n{solution}\n\n")
        moves = solution.split()
        self.solution_text.insert(tk.END, f"Количество ходов: {len(moves)}\n")
        self.solution_text.insert(tk.END, "\nНотация:\n")
        self.solution_text.insert(tk.END, "U (вверх), D (вниз), F (вперёд), B (назад), L (лево), R (право)\n")
        self.solution_text.insert(tk.END, "' — против часовой, 2 — двойной ход")
        self.solution_text.config(state="disabled")

    except Exception as e:
        self.solution_text.config(state="normal")
        self.solution_text.delete(1.0, tk.END)
        self.solution_text.insert(tk.END, f"Ошибка при решении:\n\n{str(e)}\n\n")
        self.solution_text.insert(tk.END, "Возможно, неверная компоновка кубика.\n")
        self.solution_text.insert(tk.END, "Убедитесь, что каждая грань имеет по 9 одинаковых цветов.")
        self.solution_text.config(state="disabled")
        messagebox.showerror("Ошибка", f"Не удалось найти решение: {e}")

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = RubiksCubeGUI(root)
    root.mainloop()