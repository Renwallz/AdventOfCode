entry = (2978, 3083)


def get_value(row, col):
    val = 0
    for i in range(1, col + 1):
        val += i
    j = col
    for i in range(1, row):
        val += j
        j += 1
    return val


iterations = get_value(*entry)

state = 20151125


def next_code():
    global state
    state = (state * 252533) % 33554393
    return state


for _ in range(iterations - 1):
    next_code()

print(state)
