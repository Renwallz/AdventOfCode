import ast

with open('day12.in') as f:
    data = ast.literal_eval(f.read())
    
#Part 1 (data is a string in this case):
#sum([int(x) for x in  re.findall('-?\d+', data)])

def addNums(structure):
    tot = 0
    if isinstance(structure, int):
        return structure
    if isinstance(structure, str):
        return tot
    if isinstance(structure, dict):
        if 'red' in structure.keys() or 'red' in structure.values():
            return tot
        tot += sum(addNums(k) for k in structure.keys())
        tot += sum(addNums(v) for v in structure.values())
    else:   #is a list
        tot = sum(addNums(x) for x in structure)
    return tot
        
print(addNums(data))