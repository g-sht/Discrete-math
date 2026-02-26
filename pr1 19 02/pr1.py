import networkx as nx
import matplotlib.pyplot as plt

def check_reflect(R: list) -> bool:
    for el in R:
        pair = (el[0], el[0])
        if pair not in R:
            return False
    return True

def check_antireflect(R: list) -> bool:
    for el in R:
        pair = (el[0], el[0])
        if pair in R:
            return False
    return True

def check_simm(R: list) -> bool:
    for el in R:
        pair = (el[1], el[0])
        if pair not in R:
            return False
    return True

def check_antisimm(R: list) -> bool:
    for el in R:
        pair = (el[1], el[0])
        if pair in R and el[1] != el[0]:
            return False
    return True

def check_transit(R: list) -> bool:
    for (a, b) in R:
        for (c, d) in R:
            if b == c and (a, d) not in R:
                return False
    return True

def check_lin(R: list) -> bool:
    A = set([el[0] for el in R])
    for a in A:
        for b in A:
            if a != b and (a, b) not in R and (b, a) not in R:
                return False
    return True

R = [(1, 1), (2, 2), (3, 3)]
G = nx.DiGraph(directed=True)
G.add_nodes_from(set([el[0] for el in R]))
G.add_edges_from(R)

nx.draw(G, with_labels=True, node_color='lightblue')
plt.show()

is_reflect = check_reflect(R)
is_simm = check_simm(R)
is_antisimm = check_antisimm(R)
is_antireflect = check_antireflect(R)
is_transit = check_transit(R)
is_lin = check_lin(R)

print("Reflect:", is_reflect, "Anitreflect:", is_antireflect,  "Simm:", is_simm, "Antisimm:", is_antisimm)
print("Transit:", is_transit, "Lin:", is_lin)