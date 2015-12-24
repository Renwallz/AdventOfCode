import math

TARGET = 29000000


def get_divisors(x):
    divisors = []
    for i in range(int(math.floor(math.sqrt(x))), 0, -1):
        if x % i == 0:
            divisors.extend([i, x // i])
    divisors = set(divisors)
    return divisors


def calculate_presents(house_number):
    divisors = filter(lambda x: x * 50 >= house_number, get_divisors(house_number))
    divisors = map(lambda x: x * 11, divisors)
    return sum(divisors)


for i in range(1, 10):
    print(i, calculate_presents(i))

while True:
    val = calculate_presents(i)
    if val >= TARGET:
        print(i, val)
        break
    i += 1
