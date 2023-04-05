import copy
import numpy as np

# Importação do arquivo de entrada
grid = np.loadtxt('input.txt', dtype=int)
objetivo = (grid.shape[0] - 1, grid.shape[1] - 1)

def countGreensNeigb(updated_grid, i, j):
    '''
    Conta a quantidade de células verdes vizinhas da célula (i, j)
    '''
    i_min = max(0, i-1)
    i_max = min(len(updated_grid)-1, i+1)
    j_min = max(0, j-1)
    j_max = min(len(updated_grid[i])-1, j+1)
    greens = 0
    for x in range(i_min, i_max + 1):
        for y in range(j_min, j_max + 1):
            if updated_grid[x][y] == 1 and not (x == i and y == j):
                greens += 1
    return greens

def updateGrid(updated_grid):
    '''
    Cria um novo grid de jogo atualizado com as movimentações realizadas pela células em uma unidade de tempo
    '''
    grid2 = copy.deepcopy(updated_grid)
    for i in range(0, len(updated_grid)):
        for j in range(0, len(updated_grid[i])):
            greens_neigb = countGreensNeigb(updated_grid, i, j)
            if updated_grid[i][j] == 0 and greens_neigb > 1 and greens_neigb < 5:
                grid2[i][j] = 1
            elif updated_grid[i][j] == 1 and greens_neigb <= 3 or greens_neigb >= 6:
                grid2[i][j] = 0
    return grid2

def get_moves(i, j):
    '''
    Retorna uma lista de tuplas representando as células para as quais é possível ir a partir da célula atual fazendo 1 movimento, levando em conta as bordas. 
    '''
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

def calc_dist(cell):
    '''
    Calcula a distância Manhattan de cell (tupla xy) até o objetivo
    '''
    return objetivo[0] - cell[0] + objetivo[1] - cell[1]

# Tuplas (x, y, t) posição x e y, e instante de tempo t
open_list = [(0, 0, 0)]
closed_list = [] # Utiliza tupla simples (x, y)
cost_F = {(0, 0, 0): calc_dist((0, 0))} 
cost_G = {(0, 0, 0): 0}
cost_H = {}
parent = {(0, 0, 0): (0, 0, 0)} # Filho: Pai, Quer dizer que o movimento foi do pai para o filho

tempos = [grid] # Guarda o estado do grid em cada instante de tempo
tempo = 0 # Controla o instante de tempo atual, para acessar o grid e os dicinários de tempo no instante correto

# Método A*
while open_list and objetivo not in closed_list:
    mov_atual = open_list.pop(open_list.index(min(open_list, key=lambda e: cost_F[e])))
    
    # Sempre que o movimento sendo processado estiver no último instante de tempo, processa o grid do próximo instante de tempo
    tempo = mov_atual[2]
    if tempo == len(tempos) - 1:
        tempos.append(updateGrid(tempos[-1]))
    
    closed_list.append((mov_atual[0], mov_atual[1]))
    moves_list = get_moves(mov_atual[0], mov_atual[1])
    
    # Percorrer os possíveis movimentos a partir da célula atual
    for prox in moves_list:
        prox_mov = (*prox, tempo + 1)
        
        if tempos[tempo + 1][prox_mov[0]][prox_mov[1]] != 1: # Verificar se o movimento escolhido não vai se chocar com um verde no próximo grid
            # Adicionar o movimento na lista aberta, atualizando seus custos
            if prox_mov not in open_list:
                open_list.append(prox_mov)
                parent[prox_mov] = mov_atual
                cost_G[prox_mov] = cost_G[parent[prox_mov]] + 1
                cost_H[prox_mov] = calc_dist(prox_mov)
                cost_F[prox_mov] = cost_G[prox_mov] + cost_H[prox_mov]
            
            # Se o custo G do caminho atual for melhor, atualizar o prox
            elif cost_G[mov_atual] + 1 < cost_G[prox_mov]:
                parent[prox_mov] = mov_atual
                cost_G[prox_mov] = cost_G[parent[prox_mov]] + 1
                cost_H[prox_mov] = calc_dist(prox_mov)
                cost_F[prox_mov] = cost_G[prox_mov] + cost_H[prox_mov]

if not open_list and objetivo not in closed_list:
    print("Caminho não encontrado!")
else:
    caminho = []
    filho = (64, 84, tempo)
    pai = parent[filho]
    # Percorrer a lista de pais, para montar o caminho
    while pai != (0, 0, 0) or filho != (0, 0, 0):
        if filho[1] < pai[1]:
            caminho.append('L')
        elif filho[1] > pai[1]:
            caminho.append('R')
        elif filho[0] < pai[0]:
            caminho.append('U')
        elif filho[0] > pai[0]:
            caminho.append('D')
        filho = pai
        pai = parent[pai]

caminho.reverse()
np.savetxt('out.txt', caminho, fmt = "%s", newline = " ")
