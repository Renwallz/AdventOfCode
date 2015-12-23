known_info = '''children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1'''.split('\n')


class aunt(object):
    def __init__(self, known):
        self.info = known

    def get_value(self, attribute):
        return self.info.get(attribute, None)

    def __repr__(self):
        return str(self.info)


aunties = {}

with open('day16.in') as f:
    for line in f:
        name, attributes = line.split(': ', 1)
        d = {}
        attributes = attributes.rstrip()
        for attr in attributes.split(', '):
            k, v = attr.split(': ')
            d[k] = v
        aunties[name] = aunt(d)

valid_aunties = aunties.keys()

for line in known_info:
    k, v = line.split(': ')
    new_valid = []
    for a in valid_aunties:
        if aunties[a].get_value(k) in (v, None):
            new_valid.append(a)
    valid_aunties = new_valid

print(valid_aunties)
