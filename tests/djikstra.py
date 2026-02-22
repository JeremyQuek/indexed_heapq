import random
import heapq
import time
from core import index_pq

import matplotlib.pyplot as plt

def generate_graph(n_nodes, density=0.3, max_weight=10):
    graph = {i: {} for i in range(n_nodes)}
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i != j and random.random() < density:
                graph[i][j] = random.randint(1, max_weight)
    return graph


def dijkstra_ipq(graph, start=0):
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0
    visited = set()

    pq = index_pq()
    keys = [pq.push(dist[i]) for i in range(n)]

    while pq:
        u_dist, u = pq.pop()
        if u in visited:
            continue
        visited.add(u)

        for v, w in graph[u].items():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pq.update(keys[v], dist[v])

    return dist

def dijkstra_heapq(graph, start=0):
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0
    visited = set()

    pq = [(dist[i], i) for i in range(n)]
    heapq.heapify(pq)

    while len(pq) > 0:
        u_dist, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        for v, w in graph[u].items():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    return dist

def run_benchmark():
    sizes = [10, 50, 100, 250, 500, 1000, 2000, 3000, 5000,10000]
    ipq_times = []
    heapq_times = []
    density = 0.2

    for N in sizes:
        graph = generate_graph(N, density)

        # Benchmark IPQ
        start = time.time()
        dijkstra_ipq(graph)
        ipq_times.append(time.time() - start)

        # Benchmark Heapq
        start = time.time()
        dijkstra_heapq(graph)
        heapq_times.append(time.time() - start)

        print(f"Finished N={N}")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, ipq_times, label='Indexed Priority Queue (IPQ)', marker='o', color='orange')
    plt.plot(sizes, heapq_times, label='Standard Heapq (Lazy)', marker='s', color='blue')

    plt.title('Dijkstra Performance: IPQ vs. Heapq')
    plt.xlabel('Input Size (Number of Nodes $N$)')
    plt.ylabel('Execution Time (seconds)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()



# run python3 -m test.djikstra from project root
if __name__ == "__main__":
    random.seed(42)
    N = 10
    DENSITY = 0.2

    graph = generate_graph(N, DENSITY)

    # Indexed PQ
    start = time.time()
    dist_ipq = dijkstra_ipq(graph)
    t_ipq = time.time() - start
    print(f"Indexed PQ Dijkstra: {t_ipq:.6f} sec")

    # Heapq
    start = time.time()
    dist_heapq = dijkstra_heapq(graph)
    t_heapq = time.time() - start
    print(f"Heapq Dijkstra: {t_heapq:.6f} sec")

    # Validate results match
    assert dist_ipq == dist_heapq, "Distances do not match!"
    print("Distances match for both implementations")
    run_benchmark()
