import timeit
import random
import heapq
import matplotlib.pyplot as plt
from core import index_pq

def benchmark_ipq(size, updates):
    initial_data = [random.randint(0, 1_000_000) for _ in range(size)]
    ipq = index_pq(initial_data)
    for _ in range(updates):
        target_id = random.randint(0, size - 1)
        new_val = random.randint(-500_000, 500_000)
        ipq.update(target_id, new_val)
    while ipq:
        ipq.pop()

def benchmark_standard(size, updates):
    test_heap = [random.randint(0, 1_000_000) for _ in range(size)]
    heapq.heapify(test_heap)
    for _ in range(updates):
        val = random.randint(-500_000, 500_000)
        heapq.heappush(test_heap, val)
    while test_heap:
        heapq.heappop(test_heap)

def run_visual_benchmark():
    # Scaling sizes from 1k to 100k
    sizes = [1000, 5000, 10000, 25000, 50000, 75000, 100000]
    update_ratio = 0.1 # 10% of heap size updated

    ipq_results = []
    std_results = []

    print("Starting Benchmark...")
    for n in sizes:
        n_updates = int(n * update_ratio)

        t_ipq = timeit.timeit(lambda: benchmark_ipq(n, n_updates), number=3) / 3
        t_std = timeit.timeit(lambda: benchmark_standard(n, n_updates), number=3) / 3

        ipq_results.append(t_ipq)
        std_results.append(t_std)
        print(f"N={n} | IPQ: {t_ipq:.4f}s | Std: {t_std:.4f}s")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, ipq_results, label='Indexed PQ (In-place Fix)', marker='o', linewidth=2, color='orange')
    plt.plot(sizes, std_results, label='Standard heapq (Lazy/Push)', marker='s', linewidth=2,  color='blue')

    plt.title('Update Efficiency: Indexed Heap vs. Standard Heapq')
    plt.xlabel('Initial Heap Size ($N$)')
    plt.ylabel('Time (seconds)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()

    # Save the plot for your README
    plt.savefig('performance_graph.png')
    print("\n Graph saved as performance_graph.png")
    plt.show()

# run python3 -m test.stress from project root
if __name__ == "__main__":
    run_visual_benchmark()
