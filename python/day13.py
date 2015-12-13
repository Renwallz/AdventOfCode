from itertools import permutations
from collections import defaultdict

places = defaultdict(dict)

with open("day13.in") as f:
    for line in f:
        line = line.strip('.\n')
        line = line.split()
        first = line[0]
        negator = -1 if line[2] == 'lose' else 1
        amount = int(line[3])
        second = line[-1]
        places[first][second] = amount * negator

print(places)

#brute force method  
maxdistance = 0
combo = tuple()   
for permi in permutations(places.keys(), len(places.keys())):
    distance = sum(places[source][dest] for source, dest in zip(permi, permi[1:]+(permi[0],)))
    distance += sum(places[source][dest] for source, dest in zip(permi[1:]+(permi[0],), permi))
    if distance > maxdistance:
        combo = permi
        maxdistance = distance
        
print (combo, maxdistance)