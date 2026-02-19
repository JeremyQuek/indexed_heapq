import timeit
import random
from indexed_pq import indexed_pq

# Benchmark Settings
HEAP_SIZE = 100000
NUM_UPDATES = 10000
N_RUNS = 10

def benchmark_indexed_heap_scenario():
    # 1. Setup Phase: Initial population of the indexed heap
    initial_data = [random.randint(0, 1_000_000) for _ in range(HEAP_SIZE)]
    ipq = indexed_pq(initial_data)

    # 2. Update Phase: Performance test of O(log N) updates
    # We use the IDs generated during the initial push (0 to HEAP_SIZE-1)
    for _ in range(NUM_UPDATES):
        target_id = random.randint(0, HEAP_SIZE - 1)
        new_val = random.randint(-500_000, 500_000)

        # This is the O(log N) magic
        ipq.update(target_id, new_val)

    # 3. Finalization Phase: Pop all elements
    out = []
    while ipq.heap:
        out.append(ipq.pop())
    return out

def benchmark_standard_heapq_push_only():
    # This represents the "standard" way people use heapq (just pushing more stuff)
    test_heap = [random.randint(0, 1_000_000) for _ in range(HEAP_SIZE)]
    import heapq
    heapq.heapify(test_heap)

    for _ in range(NUM_UPDATES):
        val = random.randint(-500_000, 500_000)
        heapq.heappush(test_heap, val)

    out = []
    while test_heap:
        out.append(heapq.heappop(test_heap))
    return out

# --- Run benchmarks ---
print(f"--- Running Benchmarks (Size: {HEAP_SIZE}, Updates: {NUM_UPDATES}) ---")

time_indexed = timeit.timeit(benchmark_indexed_heap_scenario, number=N_RUNS)
time_standard = timeit.timeit(benchmark_standard_heapq_push_only, number=N_RUNS)

print(f"Indexed Heap (In-place update): {time_indexed / N_RUNS:.4f}s avg")
print(f"Standard Heap (Push-only growth): {time_standard / N_RUNS:.4f}s avg")
