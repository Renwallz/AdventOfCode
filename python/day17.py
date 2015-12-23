from itertools import combinations

containers = [43, 3, 4, 10, 21, 44, 4, 6, 47, 41, 34, 17, 17, 44, 36, 31, 46, 9, 27, 38]

TOTAL_AMOUNT = 150
answer = 0

for i in range(len(containers)):
    for comb in combinations(containers, i):
        if sum(comb) == TOTAL_AMOUNT:
            answer += 1

print(answer)
