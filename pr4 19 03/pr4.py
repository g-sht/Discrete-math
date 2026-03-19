import math

# сокращает числитель и знаменатель на НОД
def simplify(numerator, denominator):
    gcd = math.gcd(numerator, denominator)
    return numerator // gcd, denominator // gcd

# выводит в качестве строки цепную дробь
def print_continued_fractions(numerator, denominator, counter = 0):
    # считаем целую часть дроби и выводим её
    int_part = numerator // denominator
    numerator %= denominator

    print(int_part, "+ ", end='')

    # если дробь после переворота окажется числом, то мы заканчиваем вывод
    if denominator % numerator == 0:
        print(f"{numerator}/{denominator} ", end='')
        for i in range(counter):
            print(")", end='')
        return

    # в ином случае, пишем "1 /" переворачиваем дробь и повторяем операции
    print("1 / ( ", end='')
    print_continued_fractions(denominator, numerator, counter + 1)

input_numerator = int(input())
input_denominator = int(input())

simpled_num, simpled_denom = simplify(input_numerator, input_denominator)

print_continued_fractions(simpled_num, simpled_denom)