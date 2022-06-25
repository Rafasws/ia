# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 92737 André Morgado
# 97343 Rafael Ferreira

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

from math import ceil
import numpy as np
from sys import stdin


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
        
        return self.matriz[row,col]

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
    
    def remove(self, row: int, col: int, num: int):
        try:
            self.get_number(row,col).remove(num)
        except AttributeError:
            pass
        except ValueError:
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
                if isinstance(num, int):
                    if vizinhos_horizontais[0] == num and isinstance(vizinhos_horizontais[1], list):
                        self.remove(l, c + 1, num)
                    if vizinhos_horizontais[1] == num and isinstance(vizinhos_horizontais[0], list):
                        self.remove(l, c - 1, num)
                    if vizinhos_verticais[1] == num and isinstance(vizinhos_verticais[0], list):
                        self.remove(l + 1, c, num)
                    if vizinhos_verticais[0] == num and isinstance(vizinhos_verticais[1], list):
                        self.remove(l - 1 , c, num)
                else:
                    if vizinhos_horizontais[0] == vizinhos_horizontais[1]:
                        self.remove(l, c, vizinhos_horizontais[0])
                    if vizinhos_verticais[0] == vizinhos_verticais[1]:
                        self.remove(l, c, vizinhos_verticais[0])

    def restricao_nr_iguais(self):
        """Há um número igual de 1s e 0s em cada linha e coluna (ou mais um 
        para grelhas de dimensão ímpar)"""
        dim = self.N
        for linha, values in self.linhas.items():
            if values[0] == values[1]:
                continue
            if values[0] == ceil(dim/2):
                eliminar = 0
            if values[1] == ceil(dim/2):
                eliminar = 1
            for coluna in range(0, dim):
                self.remove(linha, coluna, eliminar)
        
        for coluna, values in self.linhas.items():
            if values[0] == values[1]:
                continue
            if values[0] == ceil(dim/2):
                eliminar = 0
            if values[1] == ceil(dim/2):
                eliminar = 1
            for linha in range(0, dim):
                self.remove(linha, coluna, eliminar)
            
            
    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        new_board = Board()
        dim = int(stdin.readline())
        new_board.N = dim
        new_board.matriz = np.zeros([dim,dim], dtype=object)

        new_board.linhas = {key: 0 for key in range(0, dim)}
        new_board.colunas = {key: 0 for key in range(0, dim)}

        for i in range(0, dim):
            line = stdin.readline()
            array = list(map(int, line.split('\t')))
            n = 0
            nr_0 = 0 
            nr_1 = 0
            for j in array:
                if j == 0:
                    nr_0 += 1
                elif j == 1:
                    nr_1 += 1
                else:
                    array[n] = [0,1]
                n += 1
            new_board.linhas[i] = [nr_0, nr_1]
            new_board.matriz[i] = array  

            for coluna in range(0, dim):
                nr_0 = 0
                nr_1 = 0
                for linha in range(0, dim):
                    if new_board.matriz[linha][coluna] == 0:
                        nr_0 += 1
                    if new_board.matriz[linha][coluna] == 1:
                        nr_1 += 1
                new_board.colunas[coluna] = [nr_0, nr_1]
     
        return new_board     


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        # TODO
        pass


    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input, check
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    tabuleiro = Board.parse_instance_from_stdin()
    problema = Takuzu(tabuleiro)
    # problema.actions(problema.initial)
    # # depth_first_tree_search(problema)
    a = tabuleiro.matriz.view()
    print(a)
    tabuleiro.restricao_nr_iguais()
    print(a)


