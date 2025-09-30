import Functions

def main():
    print("4 рандомных UUID")
    for i in range(4):
        Functions.uuid_generate()

    print("Вызов функции из другого файла")
    a = 4
    b = 2
    res = Functions.my_sum(a, b)
    print(f"Сумма {a} и {b} равна {res}")
    a = 4.1
    b = 2.4
    res = Functions.my_sum(a, b)
    print(f"Сумма {a} и {b} равна {res}")



if __name__ == "__main__":
    main()