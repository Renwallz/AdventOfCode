SEED = '1113222113'

def play(number):
    previous = number[0]
    count = 0
    r = []
    for digit in number:
        if digit != previous:
            r.append(str(count))
            r.append(previous)
            previous = digit
            count = 1
        else:
            count += 1
    r.append(str(count))
    r.append(previous)
    return r
    
answer = seed
for _ in range(50):
    answer = play(answer)
    
print(len(answer))