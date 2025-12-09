import uuid

def my_print():
    print("Печать из другого файла")

def my_print2():
    print("Печать из другого файла 2")

def my_sum(in1, in2):
    return in1 + in2

def testfunc():
    print("Тестовая функция")
    print("Введите а")
    a = int(input())
    print("Введите m")
    m = int(input())
    #n = int(input())
    print(m // a)
    print(m % a)

def uuid_generate():
    print(uuid.uuid4())

def test_func():
    a = int(input())

    if a >= 2 and a <= 17:
        b = 3
        p = a * a + b * b
    else:
        b = 5

    p = (a + b) * (a + b)
    print(p)