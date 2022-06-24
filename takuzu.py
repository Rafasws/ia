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

        return (self.get_number(row + 1,col),self.get_number(row - 1,col))

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
    
        return (self.get_number(row,col - 1),self.get_number(row,col + 1))

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        new_board = Board()
        dim = int(stdin.readline())
        new_board.N = dim
        new_board.matriz = np.zeros([dim,dim], dtype=object)

        for i in range(0, dim):
            line = stdin.readline()
            array = list(map(int, line.split('\t')))
            n = 0
            for j in array:
                if j == 2:
                    array[n] = [0,1]
                n += 1
            new_board.matriz[i] = array   
        return new_board     


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        for i in state.board.matriz:
            if isinstance(i, list):
                #TODO restrições

        # TODO


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
    problema.actions(problema.initial)
    # depth_first_tree_search(problema)
    a= tabuleiro.matriz.view()
    #print(a)

    # print(tabuleiro.get_number(0,1))
    # print(tabuleiro.adjacent_vertical_numbers(2,2))
    # print(tabuleiro.adjacent_horizontal_numbers(2,2))