import functools

with open('day7.in') as f:
    lines = [x.strip() for x in f.readlines()]
    ins = [x for x in map(lambda x: x.split(' -> '), lines)]
    comm = {x[1]:sorted(x[0].split(), key=lambda y:ord(y[0]) if ord(y[0])>0x39 else ord(y[0])+127)for x in ins}
    

@functools.lru_cache(None)
def compute(rule, *inputs):
    #if it's a straight value
    if rule.isdigit():
        print("found a value! ", rule)
        return int(rule)
        
    #if it's a variable
    if rule.islower():
        return compute(*comm[rule])
    
    return gates[rule](*(compute(x) for x in inputs))
    
gates = {
    'NOT': lambda x: 65535-x,
    'AND': lambda x,y: x&y,
    'LSHIFT': lambda x,y:(x<<y)%65536,
    'RSHIFT': lambda x,y:x>>y,
    'OR': lambda x,y:x|y}

print(compute('a'))