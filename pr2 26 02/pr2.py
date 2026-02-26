import networkx as nx
from matplotlib import pyplot as plt

#поиск всех делителей числа n. результат в отсортированном списке
def find_divisors(n):
    dividers = set()
    for i in range(1, n+1):
        if n % i == 0:
            dividers.add(i)
    return list(dividers)

#построение диаграммы Хассе делителей числа n
def build_hasse_graph(n):
    divisors = find_divisors(n)
    G = nx.Graph()
    G.add_nodes_from(divisors)

    for i, a in enumerate(divisors):
        for b in divisors[i+1:]:
            if b % a == 0 and not find_coverage(a, b, divisors):
                G.add_edge(a, b)

    nx.draw(G, with_labels=True)
    plt.show()

#проверка на наличие числа c, нарушающего условие покрытия
def find_coverage(a, b, num_list):
    covered = False
    for c in num_list:
        if a < c < b and c % a == 0 and b % c == 0:
            covered = True
            break
    return covered

build_hasse_graph(24)