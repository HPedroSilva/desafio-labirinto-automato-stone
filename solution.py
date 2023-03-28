import copy
import numpy as np
import random

# Inicialização dos parâmetros do ACO
K = 50 # Número de formigas
alpha = 1 # Influência do feromônio
beta = 1 # Influência da distância
iteracoes = 100 # Quantidade de iterações
rho = 0.5 # Taxa de evaporação
Q = 1 # Quantidade feromônio liberado por cada formiga por iteração

grid = np.loadtxt('input.txt', dtype=int)
ferom = np.ones((grid.shape[0], grid.shape[1])) # Matriz de feromônio, indica a quantidade de feromônio em cada nó

def atualizaFerom(formigas_dist, formigas_caminho):
    global ferom
    feromX = np.zeros((grid.shape[0], grid.shape[0])) # Matriz de feromonios provisória de todas as formigas

    for k in range (0, K): # Para cada formiga
        Dferom = Q / formigas_dist[k] # quantidade de feromonio que a formiga vai depositar

        for l in range(1, len(formigas_caminho[k])): # Iterar na rota da formiga k
            i = formigas_caminho[k][l-1]
            j = formigas_caminho[k][l]
            feromX[i][j] += Dferom # Inserindo o feromonio da formiga k na aresta ij da matriz provisória

    ferom = (1 - rho) * ferom + feromX # Atualizando a matriz de feromonio segundo a equação (2)

def roleta(prob):
    r = random.random() # Define o valor aleatorio [0-1]
    contador = 0
    soma = 0
    while (soma <= r): # Enquanto a soma for menor do que o valor escolhido        
        soma += prob[contador] # probabilidade da aresta
        contador += 1 
    return contador - 1

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
    return move[0], move[1], 64 - move[0] + 84 - move[1]

def calc_dist_list(list_moves):
    list_moves_dist = []
    for move in list_moves:
        list_moves_dist.append(calc_dist(move))
    return list_moves_dist

def play(grid1, pos, t):
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
        moves_list = [move for move in moves_list if grid2[move[0]][move[1]] != 1]
        dist_moves_list = [i[2] for i in calc_dist_list(moves_list)]
        atratividade = 1 / np.array([dist_moves_list])

        prob = (ferom[*moves_list] ** alpha * atratividade ** beta) / (ferom[*moves_list] ** alpha).dot((atratividade ** beta).T) # Vetor de probabilidades dos nós possíveis
        prox = roleta(prob)

        print(f'Próx mov: {calc_dist(moves_list[prox])}')
        a = play(grid2, calc_dist(moves_list[prox]), t+1)
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


print(play(grid_1, (0, 0), 0))