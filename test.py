from sys import stdin
import numpy as np

N = int(stdin.readline())
matriz = np.zeros([N,N], dtype=int)

for i in range(0, N):
    line = stdin.readline()
    array = line.split('\t')
    matriz[i] = array 

a = matriz.view()

print(a)