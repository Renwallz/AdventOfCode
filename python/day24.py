import operator
from copy import copy
from functools import reduce
from itertools import chain, combinations, tee, compress, product

packages = [1, 2, 3, 7, 11, 13, 17, 19, 23, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
            109, 113]


# packages = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]


# the following functions are taken from the cookbook in the itertools page. Itertools is AWESOME.

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    yield chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def split_compress(iterable, selector):
    """like compress, but return two lists, one where selector is 1 for that element and one where the selector is 0"""
    # split_compress(range(10), [1,0,1,0,1,0,1,0,1,0]) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return compress(t1, selector), (d for d, s in zip(t2, selector) if not s)


def quantum_entanglement(items):
    return reduce(operator.mul, items)


def divide(l):
    """divide a single list into two lists"""
    for combo in product(range(2), repeat=len(l)):
        yield split_compress(l, combo)


solved = []
global_counter = 0

for r in range(1, len(packages)):
    for combo in combinations(packages, r):
        remaining = copy(packages)
        for item in combo:
            remaining.remove(item)

        if sum(combo) == sum(remaining) / 2:
            for left, right in divide(remaining):
                left = list(left)
                right = list(right)
                if sum(left) == sum(right):
                    print(r, combo, left, right)
                    solved.append((combo, global_counter, left, right))
                    global_counter += 1
                    break
    if solved:
        if len(solved) == 1:
            print(solved[0][0])
            print(quantum_entanglement(solved[0][0]), solved)
            break
        solved = map(lambda x: (quantum_entanglement(x[0]), x), solved)
        solved = sorted(solved)
        print(solved[0])
        break
