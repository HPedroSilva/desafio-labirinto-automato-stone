import copy
import numpy as np

grid = np.loadtxt('input.txt', dtype=int)

def countGreensNeigb(grid1, i, j):
    i_min = max(0, i-1)
    i_max = min(len(grid1)-1, i+1)
    j_min = max(0, j-1)
    j_max = min(len(grid1[i])-1, j+1)
    greens = 0
    for x in range(i_min, i_max + 1):
        for y in range(j_min, j_max + 1):
            if grid1[x][y] == 1 and not (x == i and y == j):
                greens += 1
    return greens

def updateGrid(grid1):
    grid2 = copy.deepcopy(grid1)
    for i in range(0, len(grid1)):
        for j in range(0, len(grid1[i])):
            greens_neigb = countGreensNeigb(grid1, i, j)
            if grid1[i][j] == 0 and greens_neigb > 1 and greens_neigb < 5:
                grid2[i][j] = 1
            elif grid1[i][j] == 1 and greens_neigb <= 3 or greens_neigb >= 6:
                grid2[i][j] = 0
    return grid2

def moves(i, j):
    moves_list = []
    if (i - 1 >= 0):
        moves_list.append((i - 1, j))
    if (i + 1 < len(grid)):
        moves_list.append((i + 1, j))
    if (j - 1 >= 0):
        moves_list.append((i, j - 1))
    if (j + 1 < len(grid[i])): 
        moves_list.append((i, j + 1))
    return moves_list

def calc_dist(move):
    return move[0], move[1], 6 - move[0] + 7 - move[1]

def calc_dist_list(list_moves):
    list_moves_dist = []
    for move in list_moves:
        list_moves_dist.append(calc_dist(move))
    return list_moves_dist

def play(grid1, pos, last, t):
    print(f'Tempo: {t}')
    print(f'Posição: {pos}')
    for i in grid1:
        if np.where(grid1==i) == pos[0]:
            a = i.copy()
            a[pos[1]] = 'X'
            print(list(a))
        else:
            print(list(i))
    input()
    print()

    if grid1[pos[0]][pos[1]] == 4:
        return 1
    else:
        grid2 = updateGrid(grid1)
        moves_list = moves(*pos)
        moves_list = calc_dist_list(moves_list)
        moves_list.sort(key = lambda e: e[2])

        if last in moves_list:
           moves_list.remove(last)

        for move in moves_list:
            if grid2[move[0]][move[1]] == 0 or grid2[move[0]][move[1]] == 4:
                print(f'Próx mov: {calc_dist(pos)}')
                a = play(grid2, (move[0], move[1]), calc_dist(pos), t+1)
                if a:
                    return 1
        return 0

grid_1 = copy.deepcopy(grid)
# while True:
#     grid_1 = updateGrid(grid_1)
#     for i in grid_1:
#         print(i)
#     input()
#     print()


print(play(grid_1, (0, 0), (0, 0), 0))