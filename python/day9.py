from itertools import permutations
from collections import defaultdict

places = defaultdict(dict)

with open("day9.in") as f:
    for line in f:
        line = line.strip()
        first, second, distance = line.split()[::2]
        places[first][second] = int(distance)
        places[second][first] = int(distance)


#brute force method  
maxdistance = 0
combo = tuple()   
for permi in permutations(places.keys(), len(places.keys())):
    distance = sum(places[source][dest] for source, dest in zip(permi, permi[1:]))
    if distance > maxdistance:
        combo = permi
        maxdistance = distance
        
print (combo, maxdistance)