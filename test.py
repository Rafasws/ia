from math import ceil
from sys import stdin
import numpy as np

dim = int(stdin.readline())
new_board = np.zeros([dim,dim], dtype=object)
for i in range(0, dim):
            line = stdin.readline()
            array = list(map(int, line.split('\t')))
            n = 0
            for j in array:
                if j == 2:
                    array[n] = [0,1]
                n += 1
            new_board[i] = array

a = new_board.view()

print(a)
print(array)
array = [0]
print(array == 0)


print(ceil(4.1))