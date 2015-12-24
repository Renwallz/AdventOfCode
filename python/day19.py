from collections import defaultdict

mapping = defaultdict(list)
seen = set()

with open('day19.in')as f:
    for line in f:
        line = line.rstrip()
        if '=>' in line:
            k, v = line.split(' => ')
            mapping[k].append(v)
        elif len(line) > 0:
            CHEMICAL = line

reversed_mapping = {v: k for k, x in mapping.items() for v in x}


def reduce(base, target='e', step=0):
    for i in range(len(base), -1, -1):
        for j in range(len(base), i, -1):
            if base[i:j] in reversed_mapping:
                new = ''.join((base[:i], reversed_mapping[base[i:j]], base[j:]))
                print(new)
                if new == target:
                    print(step + 1)
                    return True
                else:
                    if reduce(new, step=step + 1):
                        return True


print(CHEMICAL)
reduce(CHEMICAL)

'''
def generate_new_compounds(base):
    altered_chemicals = set()

    for i in range(len(base)):
        if base[i] in mapping:
            for altered in mapping[base[i]]:
                new = ''.join((base[:i], altered, base[i + 1:]))
                altered_chemicals.add(new)

        elif base[i:i + 2] in mapping:
            for altered in mapping[base[i:i + 2]]:
                new = ''.join((base[:i], altered, base[i + 2:]))
                altered_chemicals.add(new)
    return altered_chemicals


def get_distance(base, goal=CHEMICAL):
    return SequenceMatcher(None, base, goal).quick_ratio()

def solve(base, goal=CHEMICAL, step=0, distance=0):
    possibles = generate_new_compounds(base)
    possibles = sorted(map(lambda x: (get_distance(x), x), possibles), key=lambda x:x[0], reverse=True)
    for dist, possible in possibles:
        if possible in seen:
            continue
        seen.add(possible)
        if len(possible) > len(goal) + 10:
            return False
        print(possible)
        if possible == goal:
            print(step+1)
            return True
        if dist < distance:
            return False
        if solve(possible, goal, step=step + 1, distance=get_distance(possible)):
            return True
    return False

solve('e')
'''

'''
to_investigate = [('e', 0)]
investigating = []
seen = set()
run = True

while run:
    investigating = to_investigate
    to_investigate = []

    for new, step in investigating:
        new = generate_new_compounds(new)
        for result in new:
            if result in seen:
                continue

            seen.add(result)
            if result == CHEMICAL:
                print(result, step + 1)
                run = False
                break

            if len(result) > len(CHEMICAL) + 10:
                continue
            to_investigate.append((result, step + 1))

    sequences = map(lambda x: (SequenceMatcher(None, x[0], CHEMICAL),x), to_investigate)
    top_ten = sorted(sequences, key=lambda x: x[0].quick_ratio(), reverse=True)[:10]
    to_investigate = sorted(top_ten, key=lambda x: x[0].ratio(), reverse=True)[:5]
    to_investigate = [x for x in map(lambda x: x[1], to_investigate)]
    print(to_investigate[0])'''
