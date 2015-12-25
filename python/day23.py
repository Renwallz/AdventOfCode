program = []

with open('day23.in') as f:
    for line in f:
        line = line.strip()
        line = line.split()
        program.append(line)

a = b = 0
i = 0
while i < len(program):
    line = program[i]
    if line[0] == ('inc'):
        if line[1] == 'a':
            a += 1
        else:
            b += 1
    elif line[0] == ('hlf'):
        if line[1] == 'a':
            a //= 2
        else:
            b //= 2
    elif line[0] == ('tpl'):
        if line[1] == 'a':
            a *= 3
        else:
            b *= 3
    elif line[0] == ('jmp'):
        offset = int(line[1])
        i += offset
        continue
    elif line[0] == ('jie'):
        offset = int(line[2])
        if line[1].startswith('a'):
            i += offset if a % 2 == 0 else 1
        else:
            i += offset if b % 2 == 0 else 1
        continue
    else:
        offset = int(line[2])
        if line[1].startswith('a'):
            i += offset if a == 1 else 1
        else:
            i += offset if b == 1 else 1
        continue
    i += 1

print(b)
