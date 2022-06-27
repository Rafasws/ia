# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 19:
# 92737 André Morgado
# 97347 Rafael Ferreira

from copy import deepcopy
import time
from tracemalloc import start
import numpy as np
from sys import stdin
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    compare_graph_searchers,
    compare_searchers,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        
        return self.matriz.item(row,col)

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        if row == 0:
            return(self.get_number(row + 1,col), None)
        elif row == (self.N - 1):
            return(None, self.get_number(row - 1,col))
        else:
            return (self.get_number(row + 1,col),self.get_number(row - 1,col))

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            return (None, self.get_number(row,col + 1))
        elif col == (self.N - 1):
            return (self.get_number(row, col - 1), None)
        else:
            return (self.get_number(row,col - 1), self.get_number(row,col + 1))

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        board = Board()
        board.N = int(stdin.readline())
        board.cel_livres = dict() # dicionário com as posicoes a preencher as opcoes possiveis
        board.linhas = dict()   # contador de 0s e 1s em cada linha
        board.colunas = dict()  # contador de 0s e 1s em cada coluna
        board.linhas_completas = set() # set com as linhas completas
        board.colunas_completas = set() # set com as colunas completas

        dim = board.N
        # inicializa a matriz
        board.matriz = np.zeros([dim,dim], dtype=int)
        # le linhas do input
        for l in range(0, dim):
            line = stdin.readline()
            array = list(map(int, line.split('\t')))
            nr_0 = 0 # contador de 0s por linha
            nr_1 = 0 # contador de 1s por coluna
            for c in range(0, dim):
                if array[c] == 0:
                    nr_0 += 1
                elif array[c] == 1:
                    nr_1 += 1
                else:
                    # guarda no dicionario a posicao livre
                    board.cel_livres[(l,c)] = [0,1]
            # guarda o nº de 0s e 1s de cada linha        
            board.linhas[l] = [nr_0, nr_1]
            # guarda linha na matriz
            board.matriz[l] = array  
            # guarda as linhas comletas no set
            if nr_0 + nr_1 == dim:
                board.linhas_completas.add(tuple(array))

        # apos feita a matriz vai ver o nr de 0s e 1s por colunas e se já existe
        # alguma coluna completa
        for c in range(0, dim):
            nr_0 = 0 # contador de 0s na coluna
            nr_1 = 0 # contador de 1s na coluna
            for l in range(0, dim):
                if board.matriz[l][c] == 0:
                    nr_0 += 1
                if board.matriz[l][c] == 1:
                    nr_1 += 1
            # guarda o nr de 0s e 1s da coluna
            board.colunas[c] = [nr_0, nr_1]
            # adiciona coluna completa ao set de colunas completas
            if nr_0 + nr_1 == dim:
                board.colunas_completas.add(tuple(board.matriz[:, c]))
        return board   

    def remove(self, key, valor):
        """ Remove valor possivel de célula livre """
        try:
            self.cel_livres[key].remove(valor)
        except:
            pass

    def restricao_adjacentes(self):
        """ Faz as restrições do dominio das células do tabuleiro ainda não atribuidas
        com base na restrição que não há mais do que dois numeros iguais adjacentes"""
        dim = self.N
        for l in range(0, dim):
            for c in range(0, dim):
                num = self.get_number(l, c)
                vizinhos_horizontais = self.adjacent_horizontal_numbers(l, c)
                vizinhos_verticais = self.adjacent_vertical_numbers(l, c)
                if num in (0,1):
                    # nr igual à esquerda e cel livre à direita
                    if vizinhos_horizontais[0] == num and vizinhos_horizontais[1] == 2:
                        self.remove((l, c + 1), num)
                    # nr igual à direita e cel livre à esquerda
                    if vizinhos_horizontais[1] == num and vizinhos_horizontais[0] == 2:
                        self.remove((l, c - 1), num)
                    # nr igual em cima e cel livre em baixo
                    if vizinhos_verticais[1] == num and vizinhos_verticais[0] == 2:
                        self.remove((l + 1, c), num)
                    # nr igual em baixo e cel livre em cima
                    if vizinhos_verticais[0] == num and vizinhos_verticais[1] == 2:
                        self.remove((l - 1 , c), num)
                else:
                    # cel livre entre dois numeros iguais na horizontal
                    if vizinhos_horizontais[0] == vizinhos_horizontais[1]:
                        self.remove((l, c), vizinhos_horizontais[0])
                    # cel livre entre dois numeros iguais na vertical
                    if vizinhos_verticais[0] == vizinhos_verticais[1]:
                        self.remove((l, c), vizinhos_verticais[0])

    def restricao_nr_iguais(self):
        """Há um número igual de 1s e 0s em cada linha e coluna (ou mais um 
        para grelhas de dimensão ímpar)"""
        dim = self.N
        for linha, values in self.linhas.items():
            eliminar = -1
            # linha completa
            if values[0] == values[1]:
                continue # não interessa
            # já so falta acrescentar 1s a linha
            if values[0] == np.ceil(dim/2):
                # eliminamos os 0s como possibilidade das celulas livres dessa linha
                eliminar = 0 
            if values[1] == np.ceil(dim/2):
                # eliminamos os 1s como possibilidade das celulas livres dessa linha
                eliminar = 1
            if eliminar != -1:
                # eliminar opcções 
                for coluna in range(0, dim):
                    self.remove((linha, coluna), eliminar)
        
        # mesma coisa so que para colunas
        for coluna, values in self.colunas.items():
            eliminar = -1
            if values[0] == values[1]:
                continue
            if values[0] == np.ceil(dim/2):
                eliminar = 0
            if values[1] == np.ceil(dim/2):
                eliminar = 1
            if eliminar != -1:
                for linha in range(0, dim):
                    self.remove((linha, coluna), eliminar)


    def lin_e_col_diferentes(self):
        """ Compara as linhas completas com as linhas por completar, devolve
        False se houver pelo menos uma linha, coluna cujas restriçoes do dominio
        não permitam que esta seja diferente de uma já completa. True caso
        ainda seja possivel terminar o jogo por este caminho """
        dim = self.N
        cel_livres = self.cel_livres
        # obtem linha já completa
        for completa in self.linhas_completas:
            for l in range(0, dim):
                # obtem linha do tabuleiro
                linha = self.matriz[l]
                if tuple(linha) == completa:
                    break # é a linha completa em questão
                # verifica que nas posições quer não temos valor atribuido só há um hipotese em cada que tornaria esta linha igual a uma já completa
                if all(list(map(lambda x, y, c: x == y or (x == 2 and len(cel_livres[(l,c)]) == 1 and cel_livres[(l,c)][0] == y), linha, completa, range(0, dim)))):
                    return False # impossível seguir este caminho
        for completa in self.colunas_completas:
            for c in range(0, dim):
                coluna = self.matriz[:, c]
                if tuple(coluna) == completa:
                    break
                if all(list(map(lambda x, y, l: x == y or (x == 2 and len(cel_livres[(l,c)]) == 1 and cel_livres[(l,c)][0] == y), coluna, completa, range(0, dim)))):
                    return False
        return True
        
class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        dim = state.board.N
        cel_livres = state.board.cel_livres
        actions = []
        # aplica as restrições de dominio das células livres
        state.board.restricao_adjacentes()
        state.board.restricao_nr_iguais()
        min_len = 3
        key_action = None
        # verifica que se ainda é possivel obter linhas e colunas diferentes
        if state.board.lin_e_col_diferentes():
            for key, values in cel_livres.items():
                # encontrou uma célula livre que não tem mais opcoes
                if values == []:
                    # não é possivel terminar o jogo por este camnho
                    return []
                # guarda as acoes
                elif len(values) < min_len:
                    min_len = len(values)
                    key_action = (key[0], key[1])
                    actions = [(key[0], key[1], value) for value in values]
            # retorna as acoes, e apaga da celula livre se houver
            if key_action != None:
                del cel_livres[key_action]
            return actions
        # não é possível terminar o jogo por este caminho
        else:  
            return []


    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
              #inicializações
        new_state = TakuzuState(state.board)
        new_state.board = deepcopy(state.board)
        dim = new_state.board.N
        counter_linhas = new_state.board.linhas
        counter_colunas = new_state.board.colunas
        # faz ação
        new_state.board.matriz.itemset((action[0], action[1]), action[2])
        # soma os contadores de 0s e 1s de cada linha e coluna
        counter_linhas[action[0]][action[2]] += 1
        counter_colunas[action[1]][action[2]] += 1
        # vê se terminamos alguma linha ou coluna e caso tenha, adcioanmos aos sets
        if counter_linhas[action[0]][0] + counter_linhas[action[0]][1] == dim:
            new_state.board.linhas_completas.add(tuple(new_state.board.matriz[action[0]]))
        if counter_colunas[action[1]][0] + counter_colunas[action[1]][1] == dim:
            new_state.board.colunas_completas.add(tuple(new_state.board.matriz[:, action[1]]))
        return new_state

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        return len(state.board.linhas_completas) == state.board.N and\
                 len(state.board.colunas_completas) == state.board.N

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return len(node.state.board.cel_livres)


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    def imprime_goal(board, goal):
        for l in range(0,board.N):
            for c in range(0, board.N):
                if c == (board.N-1):
                    print(goal.state.board.matriz[l][c], end= "\n")
                else:
                    print(goal.state.board.matriz[l][c], end= "\t") 

    board = Board.parse_instance_from_stdin()
    problem0 = Takuzu(board)
    problem1 = deepcopy(problem0)
    problem2 = deepcopy(problem0)
    problem3 = deepcopy(problem0)
    problem4 = deepcopy(problem0)
    # Largura
    # start_time = time.time()
    # goal = breadth_first_tree_search(problem0)
    # imprime_goal(board, goal)
    # print("Largura primeiro:")
    # print("--- %s seconds ---" % (time.time() - start_time))

    # print("-----------")

    # # Profundidade
    # start_time2 = time.time()
    # problem = Takuzu(board)
    # goal = depth_first_tree_search(problem1)
    # imprime_goal(board, goal)
    # print("Profundidade primeiro:")
    # print("--- %s seconds ---" % (time.time() - start_time2))

    # print("-----------")

    # # Gananciosa
    # start_time3 = time.time()
    # goal = greedy_search(problem2)
    # imprime_goal(board, goal)
    # print("Greedy:")
    # print("--- %s seconds ---" % (time.time() - start_time3))
    
    # print("-----------")

    # # Astar_search
    # start_time4 = time.time()
    # goal = astar_search(problem3, lambda x:problem.h(x))
    # imprime_goal(board, goal)
    # print("A*:")
    # print("--- %s seconds ---" % (time.time() - start_time4))

    # print("-----------")

    compare_searchers(problems=[problem0], 
                    header= ['Searcher', 'Valores'], 
                    searchers=[breadth_first_tree_search])

    compare_searchers(problems=[problem1], 
                    header= ['Searcher', 'Valores'], 
                    searchers=[depth_first_tree_search])

    compare_searchers(problems=[problem2], 
                    header= ['Searcher', 'Valores'], 
                    searchers=[greedy_search])

    compare_searchers(problems=[problem3], 
                    header= ['Searcher', 'Valores'], 
                    searchers=[astar_search])
    


    # imprime matriz com o output indicado
      
    #print("--- %s seconds ---" % (time.time() - start_time))

