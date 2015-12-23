from collections import defaultdict

mapping = defaultdict(list)

with open('day19.in')as f:
    for line in f:
        line = line.rstrip()
        if '=>' in line:
            k, v = line.split(' => ')
            mapping[k].append(v)
        elif len(line) > 0:
            CHEMICAL = line

altered_molecules = set()

for i in range(len(CHEMICAL)):
    if CHEMICAL[i] in mapping:
        for altered in mapping[CHEMICAL[i]]:
            new = ''.join((CHEMICAL[:i], altered, CHEMICAL[i + 1:]))
            altered_molecules.add(new)
    elif CHEMICAL[i:i + 2] in mapping:
        for altered in mapping[CHEMICAL[i:i + 2]]:
            new = ''.join((CHEMICAL[:i], altered, CHEMICAL[i + 2:]))
            altered_molecules.add(new)

print(len(altered_molecules))
