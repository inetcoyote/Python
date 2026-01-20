import kociemba

class RubiksCube:
    def __init__(self, state=None):
        """
        Инициализация кубика Рубика.
        Если state не задан, создается собранный кубик.
        Формат state: словарь с гранями 'U', 'D', 'F', 'B', 'L', 'R'
        """
        if state is None:
            # Создаем собранный кубик
            self.state = {
                'U': [['W' for _ in range(3)] for _ in range(3)],  # Верх (белый)
                'D': [['Y' for _ in range(3)] for _ in range(3)],  # Низ (желтый)
                'F': [['R' for _ in range(3)] for _ in range(3)],  # Перед (красный)
                'B': [['O' for _ in range(3)] for _ in range(3)],  # Зад (оранжевый)
                'L': [['G' for _ in range(3)] for _ in range(3)],  # Лево (зеленый)
                'R': [['B' for _ in range(3)] for _ in range(3)]   # Право (синий)
            }
        else:
            self.state = state

    def display(self):
        """Отображение состояния кубика."""
        faces = ['U', 'L', 'F', 'R', 'B', 'D']
        names = {'U': 'Верх', 'D': 'Низ', 'F': 'Перед', 'B': 'Зад', 'L': 'Лево', 'R': 'Право'}
        colors = {'W': '⬜', 'Y': '🟨', 'R': '🟥', 'O': '🟧', 'G': '🟩', 'B': '🟦'}

        print("Текущее состояние кубика Рубика:")
        for face in faces:
            print(f"\n{names[face]} ({face}):")
            for row in self.state[face]:
                print(" ".join(colors[c] for c in row))

    def is_solved(self):
        """Проверка, собран ли кубик."""
        for face in self.state.values():
            color = face[0][0]
            for row in face:
                for cell in row:
                    if cell != color:
                        return False
        return True

    def to_kociemba_string(self):
        """
        Преобразование состояния кубика в строку в формате,
        понятном для библиотеки kociemba (UDFBLR).

        Порядок: U(9), R(9), F(9), D(9), L(9), B(9)
        Каждая грань читается слева направо, сверху вниз.
        """
        face_order = ['U', 'R', 'F', 'D', 'L', 'B']
        color_map = {
            'W': 'U',  # White -> Up
            'Y': 'D',  # Yellow -> Down
            'R': 'F',  # Red -> Front
            'O': 'B',  # Orange -> Back
            'G': 'L',  # Green -> Left
            'B': 'R'   # Blue -> Right
        }

        sticker_string = ""
        for face in face_order:
            for row in self.state[face]:
                for cell in row:
                    sticker_string += color_map[cell]

        return sticker_string

    @classmethod
    def from_kociemba_solution(cls, kociemba_state):
        """
        Создание кубика из строки в формате kociemba.
        kociemba_state: строка из 54 символов (UDFBLR)
        """
        # Проверка длины
        if len(kociemba_state) != 54:
            raise ValueError("Строка состояния должна содержать 54 символа")

        # Обратное отображение
        color_map = {'U': 'W', 'D': 'Y', 'F': 'R', 'B': 'O', 'L': 'G', 'R': 'B'}

        state = {}
        faces = ['U', 'R', 'F', 'D', 'L', 'B']
        idx = 0

        for face in faces:
            grid = [[0]*3 for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    color = kociemba_state[idx]
                    grid[i][j] = color_map[color]
                    idx += 1
            # Переназначаем в правильный порядок (потому что R и B поменяны местами в порядке)
            if face == 'R':
                state['R'] = grid
            elif face == 'B':
                state['B'] = grid
            else:
                state[face] = grid

        return cls(state)

def solve_rubiks_cube_kociemba(cube):
    """
    Решение кубика Рубика с использованием библиотеки kociemba.
    Возвращает строку с последовательностью ходов.
    """
    try:
        kociemba_string = cube.to_kociemba_string()
        solution = kociemba.solve(kociemba_string)
        return solution
    except Exception as e:
        return f"Ошибка при решении: {e}"

# Пример использования
if __name__ == "__main__":
    # Создаем собранный кубик
    cube = RubiksCube()

    # Применяем несколько ходов, чтобы "разобрать" кубик
    cube.R()
    cube.U()
    cube.R_prime()
    cube.F()
    cube.U()

    print("Кубик после перемешивания:")
    cube.display()

    # Получаем решение через kociemba
    print("\nИщем решение с помощью алгоритма Коцембы...")
    solution = solve_rubiks_cube_kociemba(cube)

    if "Ошибка" not in solution:
        print(f"\n✅ Решение найдено: {solution}")

        # Можно также вывести количество ходов
        moves = solution.split()
        print(f"Количество ходов: {len(moves)}")
    else:
        print(solution)