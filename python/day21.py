from collections import namedtuple
from itertools import combinations

boss = {'Hit Points': 109, 'Damage': 8, 'Armor': 2}
item = namedtuple('Item', ['Name', 'Cost', 'Damage', 'Armor'])

store = '''Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3'''.split('\n')

weapons = []
armor = []
rings = []

for line in store:
    if line.startswith('Weapons:'):
        current_list = weapons
        continue
    if line.startswith('Armor:'):
        current_list = armor
        continue
    if line.startswith('Rings:'):
        current_list = rings
        continue
    if line == '':
        continue
    stats = line.split()
    current_list.append(item(' '.join(stats[:-3]), int(stats[-3]), int(stats[-2]), int(stats[-1])))

armor.append(item('No Armor', 0, 0, 0))
rings.append(item('No Ring1', 0, 0, 0))
rings.append(item('No Ring2', 0, 0, 0))


def simulate(kit):
    player_hitpoints = 100
    player_attack = sum(map(lambda x: x.Damage, kit))
    player_armor = sum(map(lambda x: x.Armor, kit))
    boss_hitpoints = boss['Hit Points']
    boss_attack = boss['Damage']
    boss_armor = boss['Armor']

    while player_hitpoints > 0 and boss_hitpoints > 0:
        # player goes first
        boss_hitpoints -= max(player_attack - boss_armor, 1)
        player_hitpoints -= max(boss_attack - player_armor, 1)

    # if the player's health also drops below 0, they still win since that's the boss attacking after it's dead
    return boss_hitpoints <= 0


min_cost = 999999
max_cost = 0

for weapon in weapons:
    for arm in armor:
        for ring in combinations(rings, 2):
            kit = (weapon, arm, ring[0], ring[1])
            result = simulate(kit)
            cost = sum(map(lambda x: x.Cost, kit))
            if result:  # if we win!
                if cost < min_cost:
                    layout = kit
                    min_cost = cost
            else:  # if we lose!
                if cost > max_cost:
                    big_layout = kit
                    max_cost = cost

print("Cheapest winning outfit costs {} and contains {}".format(min_cost, layout))
print("Most expensive losing outfit costs {} and contains {}".format(max_cost, big_layout))
