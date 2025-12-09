import pygame
import random

# Инициализация pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 40
TRACK_WIDTH = WIDTH // 3
FPS = 60

# Настройки экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Прыгунок")

# Шрифт для отображения счёта
FONT = pygame.font.SysFont("Arial", 24)

# Класс игрока
class Player:
    def __init__(self):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = TRACK_WIDTH // 2 - self.width // 2  # Начальное положение (дорожка 1)
        self.y = HEIGHT - self.height - 10
        self.track = 0  # Начальная дорожка (0, 1, 2)
        self.moving = False  # Флаг, чтобы не прыгать дважды
        self.target_x = self.x  # Целевая позиция для плавного движения
        self.speed = 5  # Скорость перемещения между дорожками

    def move(self, direction):
        if self.moving:
            return  # Если уже движемся, не принимаем новое направление

        if direction == "LEFT" and self.track > 0:
            self.track -= 1
            self.moving = True
        elif direction == "RIGHT" and self.track < 2:
            self.track += 1
            self.moving = True

        self.target_x = (self.track * TRACK_WIDTH) + (TRACK_WIDTH // 2) - (self.width // 2)

    def update(self):
        # Плавное движение к целевой позиции
        if self.moving:
            if abs(self.target_x - self.x) < self.speed:
                self.x = self.target_x
                self.moving = False
            else:
                direction = 1 if self.target_x > self.x else -1
                self.x += self.speed * direction


# Класс препятствий
class Obstacle:
    def __init__(self, track):
        self.width = 40
        self.height = 40
        self.track = track
        self.x = (track * TRACK_WIDTH) + (TRACK_WIDTH // 2) - (self.width // 2)
        self.y = 0
        self.speed = random.randint(5, 10)
        self.passed = False  # Флаг, чтобы отметить, что игрок прошёл препятствие

    def move(self):
        self.y += self.speed


# Основной игровой цикл
def main():
    clock = pygame.time.Clock()
    player = Player()
    obstacles = []
    game_over = False
    score = 0  # Счёт игрока

    while not game_over:
        direction = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            direction = "LEFT"
        elif keys[pygame.K_RIGHT]:
            direction = "RIGHT"

        if direction:
            player.move(direction)

        player.update()  # Обновляем позицию игрока

        # Генерация препятствий
        if random.randint(1, 60) == 1:
            track = random.randint(0, 2)
            obstacles.append(Obstacle(track))

        # Движение препятствий и проверка столкновений
        for obstacle in obstacles:
            obstacle.move()

            # Проверка на столкновение
            if (obstacle.y + obstacle.height > player.y and
                    obstacle.x < player.x + player.width and
                    obstacle.x + obstacle.width > player.x):
                game_over = True

            # Проверка, прошёл ли игрок препятствие
            if not obstacle.passed and obstacle.y + obstacle.height > 0 and obstacle.y > player.y:
                score += 10
                obstacle.passed = True

        # Удаление препятствий, вышедших за экран
        obstacles = [obs for obs in obstacles if obs.y < HEIGHT]

        # Отрисовка
        screen.fill(WHITE)

        # Отрисовка дорожек
        for i in range(3):
            pygame.draw.rect(screen, BLACK, (i * TRACK_WIDTH, 0, TRACK_WIDTH, HEIGHT), 1)

        # Отрисовка игрока
        pygame.draw.rect(screen, BLACK, (player.x, player.y, player.width, player.height))

        # Отрисовка препятствий
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, (obstacle.x, obstacle.y, obstacle.width, obstacle.height))

        # Отображение счёта
        score_text = FONT.render(f"Очки: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()