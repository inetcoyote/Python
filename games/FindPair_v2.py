import pygame
import random

# Константы
WIDTH, HEIGHT = 800, 600
CARD_SIZE = 100
GAP = 10
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (144, 238, 144)
FONT_COLOR = (0, 0, 0)
FPS = 30

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Найди пару")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Примеры символов (можно заменить на изображения)
#symbols = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵"]
symbols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]


def create_board(level_size):
    pairs = level_size // 2
    selected = random.sample(symbols, pairs)
    cards = selected * 2
    random.shuffle(cards)
    return cards


def draw_board(cards, revealed, level_text):
    screen.fill(WHITE)
    title = font.render(level_text, True, FONT_COLOR)
    screen.blit(title, (20, 10))

    cols = (WIDTH - GAP * 2) // (CARD_SIZE + GAP)
    for idx, card in enumerate(cards):
        row = idx // cols
        col = idx % cols
        x = GAP + col * (CARD_SIZE + GAP)
        y = GAP + row * (CARD_SIZE + GAP) + 80

        if revealed[idx]:
            pygame.draw.rect(screen, WHITE, (x, y, CARD_SIZE, CARD_SIZE))
            text = font.render(card, True, FONT_COLOR)
            text_rect = text.get_rect(center=(x + CARD_SIZE // 2, y + CARD_SIZE // 2))
            screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_SIZE, CARD_SIZE))

    pygame.display.flip()


def show_start_screen():
    screen.fill(WHITE)
    rules = [
        "Добро пожаловать в игру 'Найди пару'!",
        "",
        "Правила:",
        "- Кликните по двум карточкам, чтобы открыть их.",
        "- Если они совпадают, они остаются открытыми.",
        "- Если нет — они снова скрываются.",
        "- Пройдите все уровни, открывая все пары.",
        "",
        "Выберите уровень:",
        "1 - 10 карточек",
        "2 - 12 карточек",
        "3 - 14 карточек",
        "4 - 16 карточек",
        "5 - 18 карточек",
        "6 - 20 карточек"
    ]

    y = 20
    for line in rules:
        text = font.render(line, True, FONT_COLOR)
        screen.blit(text, (20, y))
        y += 40

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_6:
                    level_index = event.key - pygame.K_1
                    return [10, 12, 14, 16, 18, 20][level_index]


def show_level_complete(level_size):
    screen.fill(WHITE)
    message = f"Уровень {level_size} пройден!"
    text = font.render(message, True, FONT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    screen.blit(text, text_rect)

    prompt = "Переход на следующий уровень..."
    subtext = font.render(prompt, True, FONT_COLOR)
    sub_rect = subtext.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    screen.blit(subtext, sub_rect)

    pygame.display.flip()
    pygame.time.wait(2000)


def main():
    levels = [10, 12, 14, 16, 18, 20]

    selected_level = show_start_screen()
    if selected_level is None:
        return

    start_index = levels.index(selected_level)

    for level_size in levels[start_index:]:
        cards = create_board(level_size)
        revealed = [False] * level_size
        first_choice = None
        second_choice = None
        matched = [False] * level_size
        running = True
        attempts = 0

        level_text = f"Уровень: {level_size} карточек"

        while running:
            clock.tick(FPS)
            draw_board(cards, revealed, level_text)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if first_choice is not None and second_choice is not None:
                        continue

                    x, y = event.pos
                    cols = (WIDTH - GAP * 2) // (CARD_SIZE + GAP)

                    for idx, card in enumerate(cards):
                        row = idx // cols
                        col = idx % cols
                        card_x = GAP + col * (CARD_SIZE + GAP)
                        card_y = GAP + row * (CARD_SIZE + GAP) + 80

                        if card_x < x < card_x + CARD_SIZE and card_y < y < card_y + CARD_SIZE:
                            if not matched[idx] and not revealed[idx]:
                                revealed[idx] = True
                                if first_choice is None:
                                    first_choice = idx
                                elif second_choice is None:
                                    second_choice = idx
                                    attempts += 1

                                    # Проверяем совпадение
                                    if cards[first_choice] == cards[second_choice]:
                                        matched[first_choice] = True
                                        matched[second_choice] = True
                                        first_choice = second_choice = None
                                    else:
                                        pygame.time.wait(800)
                                        revealed[first_choice] = False
                                        revealed[second_choice] = False
                                        first_choice = second_choice = None

            if all(matched):
                show_level_complete(level_size)
                running = False

    screen.fill(WHITE)
    message = "Поздравляем! Все уровни пройдены!"
    text = font.render(message, True, FONT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()


if __name__ == "__main__":
    main()
