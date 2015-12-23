from copy import deepcopy

grid = []

ON = '#'
OFF = '.'
NUM_ITERATIONS = 100


def get_active_neighbour_count(i, j):
    count = 0

    for k in range(i - 1, i + 2):
        if k < 0 or k >= len(grid):
            continue

        for l in range(j - 1, j + 2):
            if l < 0 or l >= len(grid[k]) or (k == i and l == j):
                continue

            if grid[k][l] == ON:
                count += 1
    return count


with open('day18.in') as f:
    for line in f:
        line = line.rstrip('\n')
        grid.append(list(line))

for _ in range(NUM_ITERATIONS):
    new_grid = deepcopy(grid)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == ON and get_active_neighbour_count(i, j) not in (2, 3):
                new_grid[i][j] = OFF
            elif grid[i][j] == OFF and get_active_neighbour_count(i, j) == 3:
                new_grid[i][j] = ON

    grid = new_grid

print(sum(map(lambda a: a.count(ON), (x for x in grid))))
