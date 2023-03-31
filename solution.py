import copy
import numpy as np

grid = np.loadtxt('input2.txt', dtype=int)   

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
    return 3 - move[0] + 7 - move[1]

def calc_dist_list(list_moves):
    list_moves_dist = []
    for move in list_moves:
        list_moves_dist.append(calc_dist(move))
    return list_moves_dist

def print_grid(pos):
    for i in range(0, grid.shape[0]):
        for j in range(0, grid.shape[1]):
            if i == pos[0] and j == pos[1]:
                print('X', end='')
            else:
                print(grid[i][j], end='')
            print(" ", end='')
        print()
    print()

open_list = [(0,0)]
closed_list = []
cost_F = {(0, 0): calc_dist((0, 0))}
cost_G = {(0, 0): 0}
cost_H = {}
parent = {(0, 0): (0, 0)}

print(cost_F)

while open_list and (3, 7) not in closed_list:
    mov_atual = open_list.pop(open_list.index(min(open_list, key=lambda e: cost_F[e])))
    closed_list.append(mov_atual)
    print_grid(mov_atual)
    moves_list = moves(*mov_atual)
    for prox_mov in moves_list:
        if grid[prox_mov[0]][prox_mov[1]] != 1 and prox_mov not in closed_list:
            if prox_mov not in open_list:
                open_list.append(prox_mov)
                parent[prox_mov] = mov_atual
                cost_G[prox_mov] = cost_G[parent[prox_mov]] + 1
                cost_H[prox_mov] = calc_dist(prox_mov)
                cost_F[prox_mov] = cost_G[prox_mov] + cost_H[prox_mov]
            elif cost_G[mov_atual] + 1 < cost_G[prox_mov]:
                parent[prox_mov] = mov_atual
                cost_G[prox_mov] = cost_G[parent[prox_mov]] + 1
                cost_H[prox_mov] = calc_dist(prox_mov)
                cost_F[prox_mov] = cost_G[prox_mov] + cost_H[prox_mov]
                