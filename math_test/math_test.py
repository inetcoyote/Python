import random
from colorama import init, Fore, Style

# Инициализация colorama
init(autoreset=True)

def generate_examples():
    print("Решите примеры на сложение и вычитание в пределах 20.\n")

    total_attempts = 0      # Общее количество попыток
    mistakes = 0            # Количество ошибок
    examples_solved = 0     # Количество решённых примеров (ровно 10)

    while examples_solved < 10:
        operation = random.choice(['+', '-'])

        if operation == '+':
            a = random.randint(1, 19)
            b = random.randint(1, 20 - a)
            correct_answer = a + b
        else:  # operation == '-'
            a = random.randint(2, 20)
            b = random.randint(1, a - 1)
            correct_answer = a - b

        # Повторяем пример, пока ответ не будет верным
        answered_correctly = False
        while not answered_correctly:
            user_input = input(f"{examples_solved + 1}. {a} {operation} {b} = ")
            total_attempts += 1

            try:
                user_answer = int(user_input)
                if user_answer == correct_answer:
                    print(Fore.GREEN + f"✅ Правильно! {a} {operation} {b} = {correct_answer}" + Style.RESET_ALL + "\n")
                    answered_correctly = True
                    examples_solved += 1
                else:
                    mistakes += 1
                    print(Fore.RED + f"❌ Неверно. Попробуйте ещё раз..." + Style.RESET_ALL)
            except ValueError:
                mistakes += 1
                print(Fore.RED + f"❌ Введите число! Попробуйте снова..." + Style.RESET_ALL)

    # Финальная статистика
    print(Fore.CYAN + "📊 Статистика:" + Style.RESET_ALL)
    print(f"Всего примеров: 10")
    print(f"Всего попыток: {total_attempts}")
    print(f"Ошибок: {mistakes}")

    accuracy = (10 / total_attempts) * 100 if total_attempts > 0 else 0
    print(f"Точность: {accuracy:.1f}%")

    if mistakes == 0:
        print(Fore.GREEN + "🎉 Безупречный результат! Вы молодец!" + Style.RESET_ALL)
    elif mistakes <= 3:
        print(Fore.GREEN + "👏 Хорошая работа! Почти идеально!" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "💪 Продолжайте тренироваться — будет ещё лучше!" + Style.RESET_ALL)

# Запуск программы
generate_examples()