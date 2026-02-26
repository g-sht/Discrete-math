def bul_umn(M1, M2):
    A = np.array(M1)
    B = np.array(M2)
    C = (A @ B > 0).astype(int)
    return C

# По заданным бинарным отношениям строятся графы объединения, пересечения и композиции бинарных отношений

from scipy.sparse import csr_array
from scipy.sparse.csgraph import floyd_warshall
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def bul_umn(M1, M2):# булево умножение двух матриц M1 и M2
    A = np.array(M1)
    B = np.array(M2)
    C = (A @ B > 0).astype(int)
    return C

def bul_slozh(M1, M2):
    A = np.array(M1)
    B = np.array(M2)
    C = (A + B > 0).astype(int)
    return C


k=[1, 2, 3]

r1=[(1,1),(2,2), (3,3), (1,2), (2,3)]
r2=[(3,2),(1,3),(2,1), (2,2)]


n = 3
BB = np.zeros((n, n))
CC = np.zeros((n, n))

for t in r1:
    BB[t[0] - 1][t[1] - 1] = 1

for t in r2:
    CC[t[0] - 1][t[1] - 1] = 1

print("Матрица смежности графа G1", BB)
print("Матрица смежности графа G2", CC)
N3 = bul_umn(BB, CC)
print("Матрица смежности графа композиции G1 и G2", N3)
N4 = bul_slozh(BB, CC)

print("Матрица смежности графа объединения G1 и G2", N4)
N5 = BB*CC
print("Матрица смежности графа пересечения G1 и G2", N5)


G1 = nx.DiGraph(np.matrix(BB))
G2 = nx.DiGraph(np.matrix(CC))
G3 = nx.DiGraph(np.matrix(N3))
G4 = nx.DiGraph(np.matrix(N4))
G5 = nx.DiGraph(np.matrix(N5))

pos1 = nx.spring_layout(G1, scale=100000,center=[0, 0])
pos2 = nx.circular_layout(G2, scale=80000,center=[30, 40])
pos3 = nx.spectral_layout(G3, scale=50000,center=[300, 400])
pos4 = nx.spiral_layout(G4, scale=40000,center=[35, 4])
pos5 = nx.spring_layout(G5, scale=60000,center=[3000, 477])


nx.draw(G1, pos=pos1, with_labels=True, node_size=200, arrows=True, node_color="blue",font_size=10,font_weight="bold")
nx.draw(G2, pos=pos2,with_labels=True, node_size=200, arrows=True, node_color="lightblue",font_size=10,font_weight="bold")
#nx.draw(G3, with_labels=True, pos=pos3, node_size=200, arrows=True, node_color="red",font_size=10,font_weight="bold")
nx.draw(G4, with_labels=True, node_size=200,pos=pos4, arrows=True, node_color="orange",font_size=10,font_weight="bold")
#nx.draw(G5, with_labels=True, node_size=200,pos=pos5, arrows=True,node_color="green",font_size=10,font_weight="bold")
plt.show()