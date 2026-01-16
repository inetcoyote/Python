from collections import deque
import copy

class RubiksCube:
    def __init__(self, state=None):
        """
        Инициализация кубика Рубика.
        Если state не задан, создается собранный кубик.
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

    def copy(self):
        """Создание копии кубика."""
        return RubiksCube(copy.deepcopy(self.state))

    def rotate_face_clockwise(self, face):
        """Поворот грани по часовой стрелке."""
        # Поворачиваем саму грань
        old_face = [row[:] for row in self.state[face]]
        for i in range(3):
            for j in range(3):
                self.state[face][j][2-i] = old_face[i][j]

    def rotate_face_counterclockwise(self, face):
        """Поворот грани против часовой стрелки."""
        for _ in range(3):
            self.rotate_face_clockwise(face)

    # Методы для поворота граней
    def U(self):  # Поворот верхней грани по часовой
        self.rotate_face_clockwise('U')
        temp = [self.state['F'][0][i] for i in range(3)]
        for i in range(3):
            self.state['F'][0][i] = self.state['R'][0][i]
            self.state['R'][0][i] = self.state['B'][0][i]
            self.state['B'][0][i] = self.state['L'][0][i]
            self.state['L'][0][i] = temp[i]

    def U_prime(self):  # Поворот верхней грани против часовой
        self.rotate_face_counterclockwise('U')
        for _ in range(3):
            self.U()

    def D(self):  # Поворот нижней грани по часовой
        self.rotate_face_clockwise('D')
        temp = [self.state['F'][2][i] for i in range(3)]
        for i in range(3):
            self.state['F'][2][i] = self.state['L'][2][i]
            self.state['L'][2][i] = self.state['B'][2][i]
            self.state['B'][2][i] = self.state['R'][2][i]
            self.state['R'][2][i] = temp[i]

    def D_prime(self):  # Поворот нижней грани против часовой
        self.rotate_face_counterclockwise('D')
        for _ in range(3):
            self.D()

    def F(self):  # Поворот передней грани по часовой
        self.rotate_face_clockwise('F')
        temp = [self.state['U'][2][i] for i in range(3)]
        for i in range(3):
            self.state['U'][2][i] = self.state['L'][2-i][2]
            self.state['L'][2-i][2] = self.state['D'][0][2-i]
            self.state['D'][0][2-i] = self.state['R'][i][0]
            self.state['R'][i][0] = temp[i]

    def F_prime(self):  # Поворот передней грани против часовой
        self.rotate_face_counterclockwise('F')
        for _ in range(3):
            self.F()

    def B(self):  # Поворот задней грани по часовой
        self.rotate_face_clockwise('B')
        temp = [self.state['U'][0][i] for i in range(3)]
        for i in range(3):
            self.state['U'][0][i] = self.state['R'][i][2]
            self.state['R'][i][2] = self.state['D'][2][2-i]
            self.state['D'][2][2-i] = self.state['L'][2-i][0]
            self.state['L'][2-i][0] = temp[i]

    def B_prime(self):  # Поворот задней грани против часовой
        self.rotate_face_counterclockwise('B')
        for _ in range(3):
            self.B()

    def L(self):  # Поворот левой грани по часовой
        self.rotate_face_clockwise('L')
        temp = [self.state['U'][i][0] for i in range(3)]
        for i in range(3):
            self.state['U'][i][0] = self.state['B'][2-i][2]
            self.state['B'][2-i][2] = self.state['D'][i][0]
            self.state['D'][i][0] = self.state['F'][i][0]
            self.state['F'][i][0] = temp[i]

    def L_prime(self):  # Поворот левой грани против часовой
        self.rotate_face_counterclockwise('L')
        for _ in range(3):
            self.L()

    def R(self):  # Поворот правой грани по часовой
        self.rotate_face_clockwise('R')
        temp = [self.state['U'][i][2] for i in range(3)]
        for i in range(3):
            self.state['U'][i][2] = self.state['F'][i][2]
            self.state['F'][i][2] = self.state['D'][i][2]
            self.state['D'][i][2] = self.state['B'][2-i][0]
            self.state['B'][2-i][0] = temp[i]

    def R_prime(self):  # Поворот правой грани против часовой
        self.rotate_face_counterclockwise('R')
        for _ in range(3):
            self.R()

    def get_state_hash(self):
        """Получение хеша состояния кубика для проверки уникальности."""
        state_str = ""
        for face in ['U', 'D', 'F', 'B', 'L', 'R']:
            for row in self.state[face]:
                state_str += "".join(row)
        return state_str

def solve_rubiks_cube(initial_cube):
    """
    Решение кубика Рубика с использованием поиска в ширину (BFS).
    Возвращает последовательность ходов для сборки кубика.
    """
    if initial_cube.is_solved():
        return []

    # Все возможные ходы
    moves = [
        ('U', initial_cube.U), ('U\'', initial_cube.U_prime),
        ('D', initial_cube.D), ('D\'', initial_cube.D_prime),
        ('F', initial_cube.F), ('F\'', initial_cube.F_prime),
        ('B', initial_cube.B), ('B\'', initial_cube.B_prime),
        ('L', initial_cube.L), ('L\'', initial_cube.L_prime),
        ('R', initial_cube.R), ('R\'', initial_cube.R_prime)
    ]

    # Очередь для BFS: (кубик, путь_ходов)
    queue = deque([(initial_cube.copy(), [])])

    # Множество посещённых состояний
    visited = {initial_cube.get_state_hash()}

    # Максимальная глубина поиска (ограничение для предотвращения бесконечного выполнения)
    MAX_DEPTH = 7  # Для полного решения может потребоваться до 20 ходов, но это займёт очень много времени

    while queue:
        cube, path = queue.popleft()

        # Ограничение по длине пути
        if len(path) >= MAX_DEPTH:
            continue

        # Попробовать каждый возможный ход
        for move_name, move_func in moves:
            # Создаем копию кубика и применяем ход
            new_cube = cube.copy()
            move_func.__func__(new_cube)  # Вызываем метод как функцию с новым кубиком

            # Проверяем, не достигнуто ли решение
            if new_cube.is_solved():
                return path + [move_name]

            # Получаем хеш состояния
            state_hash = new_cube.get_state_hash()

            # Если состояние ещё не посещалось, добавляем в очередь
            if state_hash not in visited:
                visited.add(state_hash)
                queue.append((new_cube, path + [move_name]))

    # Если решение не найдено в пределах MAX_DEPTH
    return None  # Решение не найдено за разумное время/глубину

# Пример использования
if __name__ == "__main__":
    # Создаем собранный кубик
    cube = RubiksCube()

    # Применяем несколько случайных ходов, чтобы "разобрать" кубик
    cube.R()
    cube.U()
    cube.F()
    cube.R_prime()

    print("Кубик после перемешивания:")
    cube.display()

    # Решаем кубик
    print("\nИщем решение...")
    solution = solve_rubiks_cube(cube)

    if solution:
        print(f"\nРешение найдено! Последовательность ходов ({len(solution)} ходов):")
        print(" -> ".join(solution))

        # Проверим, что решение действительно работает
        test_cube = RubiksCube()
        # Перемешиваем как исходный кубик
        test_cube.R(); test_cube.U(); test_cube.F(); test_cube.R_prime()
        # Применяем решение
        for move in solution:
            if move == 'U': test_cube.U()
            elif move == 'U\'': test_cube.U_prime()
            elif move == 'D': test_cube.D()
            elif move == 'D\'': test_cube.D_prime()
            elif move == 'F': test_cube.F()
            elif move == 'F\'': test_cube.F_prime()
            elif move == 'B': test_cube.B()
            elif move == 'B\'': test_cube.B_prime()
            elif move == 'L': test_cube.L()
            elif move == 'L\'': test_cube.L_prime()
            elif move == 'R': test_cube.R()
            elif move == 'R\'': test_cube.R_prime()

        if test_cube.is_solved():
            print("✅ Проверка: кубик собран правильно!")
        else:
            print("❌ Ошибка: кубик не собран.")
    else:
        print("Решение не найдено в пределах максимальной глубины поиска.")
        print("Попробуйте увеличить MAX_DEPTH (но это значительно увеличит время выполнения).")