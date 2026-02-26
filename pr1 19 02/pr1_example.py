#https://colab.research.google.com/drive/1nH9CSmoUtUmHTOUvu8AYMGKLOhld3oWS?usp=sharing#scrollTo=j75SdEY-wFDO

from scipy.sparse import csr_array
from scipy.sparse.csgraph import floyd_warshall
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Создание графа
G = nx.Graph() #не ориентированный
G=nx.DiGraph(directed=True) # ориентированный

# Добавление вершин, т.е. задание множества A для прямого произведения A*A
G.add_nodes_from([1, 2, 3, 4, 5])
# Добавление рёбер, то есть задание бинарного отношения, т.е. подмножества A*A
A=[(1, 3), (2, 3), (2, 1),(5,4),(1,5),(2,3)]

G.add_edges_from(A)

# Визуализация графа
nx.draw(G, with_labels=True, node_color='lightblue')
plt.show()

#Нахождение матрицы смежности B по бинарному отношению
n=5 #задание числа вершин графа
B = np.zeros((n, n))

for t in A:
    B[t[0]-1][t[1]-1]=1
#матрица смежности графа по заданному бинарному отношению
print(B)

graph = B
graph = csr_array(graph)
print(graph)

dist_matrix, predecessors = floyd_warshall(csgraph=graph, directed=True, return_predecessors=True)
print(dist_matrix) # Матрица расстояний N x N между узлами графа. dist_matrix[i,j] задает кратчайшее расстояние от точки i до точки j на графе
print(predecessors)