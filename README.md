<div align=center>
  <h1>⚡ Indexed Priority Queues in Python? </h1>
</div>

<div align=center>
  <img src="https://github.com/btjm123/hashmap/actions/workflows/test-macos.yaml/badge.svg"/>
  <img src="https://github.com/btjm123/hashmap/actions/workflows/test-ubuntu.yaml/badge.svg"/>
  </br>
</div>
</br>
</br>


My inspiration for creating this library were the pattern of algorithmic questions often seen in interviews and competitive programming scenarios where you are required to use `decreaseKey()` 
on a heap. 


* [Codeforces 1526C2 - Potions (Hard Version)](https://codeforces.com/contest/1526/problem/C2)
* [Codeforces 865D - Buy Low Sell High](https://codeforces.com/contest/865/problem/D)
* [Codeforces 1428E - Carrots for Rabbits](https://codeforces.com/contest/1428/problem/E)
* [Codeforces 1251E2 - Voting (Hard Version)](https://codeforces.com/contest/1251/problem/E2)
* [LeetCode 3013 - Divide an Array Into Subarrays With Minimum Cost II](https://leetcode.com/problems/divide-an-array-into-subarrays-with-minimum-cost-ii/description/)
* [LeetCode 3510 - Minimum Pair Removal to Sort Array II (Solution)](https://leetcode.com/problems/minimum-pair-removal-to-sort-array-ii/solutions/7570722/toxic-double-linked-list-lazy-heap-delet-nhef/)


It's annoying that these problems often require a dynamic updates to arbitrary heap nodes and stdlib priority queues like  `C++ std::priority_queue` or Python `heapq` do not support modifying elements in-place. Instead the common technique is to use the "Lazy Deletion" to handle `decreaseKey()`. Well, there has to be a better way right?
</br>
</br>

## The Main Idea: `fixheap()`
<p align="center">
  <img width="800" height="450" alt="image" src="https://github.com/user-attachments/assets/ac16dea7-00b6-4453-95a2-fdde5d492081" />
</p>



The pedagogical `fixheap()` function is used on theoretical implementations of heaps as an efficient way to arbitrary update heap nodes while maintaining its invariant. For instance, pseudo code of Djikstra's often include an efficient decrease function on heap node. <br>
This is usually implemented using either `siftup` or `siftdown` logic

### Python's heapq
[(link to cpython/lib/heapq.py)](https://github.com/python/cpython/blob/main/Lib/heapq.py)<br>
Reading through the heappq reading, I quickly found that the internal heapq function also employs `siftup()` or `siftdown()` functions. However, they are reserved for root/bottom nodes.
This makes sense as  `siftup()`/`siftdown()` requires knowing the index of an arbitray node, which is not a property of binary heaps.

<br/>

**Thus the question is:** <br>
Suppose we could track the index of all heap node, can we update any nodes value correctly and efficiently using `siftup()`/`siftdown()`?
<br/>
<br/>

## Theoretical Breakdown 
(Skip to the performance section if you're bored)

`Fixheap()` preserves the heap invariant by re-sifting nodes following any value mutation. Since the tree height is strictly bounded by $H = \lfloor \log_2 n \rfloor$, the operation remains a highly efficient $O(\log n)$.

For **Standard Deletion** at the root:
* Swap the leaf node ($A[n-1]$) to the root ($A[0]$).
* Execute `list.pop()` to truncate the redundant tail.
* Invoke **siftdown** to restore the invariant $P(i) \leq \min(C_L, C_R)$.

For **Insertion**:
* Append the element to the array terminus.
* Invoke **siftup** to migrate the node to its valid hierarchical stratum.



The **Fixheap** logic addresses arbitrary modifications at index $i$, where a new value may violate invariants in either direction. The state transitions follow:
* $V_{new} = V_{old}$: $O(1)$ identity operation.
* $V_{new} < V_{old}$: **siftup** to re-establish the ancestor invariant.
* $V_{new} > V_{old}$: **siftdown** to re-establish descendant invariants.

Both procedures are naturally terminating, governed by the recurrence $T(n) = T(n/2) + O(1)$.

For **Arbitrary Removal** at index $k$:
* Overwrite $A[k]$ with the current leaf node.
* Perform `list.pop()`.
* Apply **fixheap** at index $k$ to re-equilibrate the structure.

To finalize the implementation, I integrated **Index-Tracking** ($\text{Pos} \leftrightarrow \text{ID}$). By augmenting the `stdlib heapq` source logic, `Fixheap()` preserves the heap invariant by re-sifting nodes following any value mutation. Since the tree height is strictly bounded by $H = \lfloor \log_2 n \rfloor$, the operation remains a highly efficient $O(\log n)$.

<br/>

## Indexed Priority Queue Implementation 

After working through the theory and rigorously testing the heap functions, it was time to implement them. I made sure to reference and emulate the `heappq` code as much as possible, to ensure correctness and reliabilt.

**Create Object**
```python3
from index_heapq import index_pq, maxindex_pq
index_pq()
maxindex_pq()


# They can taken a list during construction:
# Keys will be auto generated 
pq = index_pq([1,2,3,4,5,6,7])

# Use map to retrieve keys. NOTE: O(N) time!!
keys = pq.map() 



# Alt constructor: pass in dict to specify keys
pq = index_pq({"a":1, "b":2,"c":3})
```


<br/>

**Heap Push**
```python3
# Heap push returns the key
key = pq.push(4, "Key")

# Auto generate key if not given
auto_key = pq.push(4)
```

<br/>

**Heap Pop**
```python3
# Heap push returns the key
(value, key) = pq.pop()
```


<br/>

**Change a node's value** 
```python3
pq.update(key, -1000)
```

<br/>

**Remove random node** 
```python3
pq.remove(key, -1000)
```

<br/>

**Get top element** 
```python3
# Heap can be access like a list using []
# Note this only shows the value, not the value + key
(value) = heap[0] 
```
<br/>

### Example Code Snippets

Class **`index_pq()`**
```python
from index_heapq import index_pq

# 1. Initialization
pq = index_pq([20, 30,40]) 



# Pushing returns a default unique key if not specified
pq.push(5, "urgent_task")
pq.push(10, "not_urgent_task") 



# Updated priority
pq.update("not_urgent_task", 2) 


print(pq[0])                     # Output: 2 -> Head of heap updated to (not_urgent_task, 2) 
print(pq.get("not_urgent_task")) # Output: 2 

if "urgent_task in pq:
  pq.remove("urgent_task")       # Output: Remove non-head node



# Pop from head
val, key = pq.pop()
print(f"Popped: {val} with Key: {key}")
```
<br/>

Example use in Dijsktra's
```python3
from indexed_heapq import index_pq

def dijkstra(graph, start=0):
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
```

<br/>
This library also exposes a max-heap variant of the class

Class **`maxindex_pq()`**
```python3
from index_heapq import maxindex_pq

# 1. Initialization 
pq = maxindex_pq([10, 20, 30])  



# Pushing returns a default unique key if not specified
pq.push(5, "urgent_task")
pq.push(10, "not_urgent_task")  



# Updated priority
pq.update("not_urgent_task", 40)  



print(pq[0])                     # Output: 40 -> Head of heap updated to (not_urgent_task, 40) 
print(pq.get("not_urgent_task")) # Output: 40 

if "urgent_task" in pq:
  pq.remove("urgent_task")       # Output: Remove non-head node



# Pop from head
val, key = pq.pop()
print(f"Popped: {val} with Key: {key}")
# Output: Popped: 40 with Key: not_urgent_task
```
<br/>

## API Functions
### Complexity Table

| Operation | Method | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- |
| **Push** | `push(val, key)` | $O(\log N)$ | $O(1)$ |
| **Pop** | `pop()` | $O(\log N)$ | $O(1)$ |
| **Update Key** | `update(key, val)` | $O(\log N)$ | $O(1)$ |
| **Remove Key** | `remove(key)` | $O(\log N)$ | $O(1)$ |
| **Get Key Value** | `get(key)` | $O(1)$ | $O(1)$ |

<br/>

### Utiliy Operations 
| Operation | Method | Time | Space | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Contains** | `key in pq` | $O(1)$ | $O(1)$ | Check if key exists. |
| **Size** | `len(pq)` | $O(1)$ | $O(1)$ | Get current element count. |
| **Initilisation** | `index_pq(list)` | $O(N)$ | $O(N)$ | Initialize heap from data. |

<br/>
<br/>



## Performance
Comparison of performance using raw stress test (raw operation speed) & situational test (Djikstra) against `heappq`

### Stress Test
Stress test simply applies thousands of `fix_heap()` operations and compares them to thousands of `lazy deletes`.
<img width="800" height="584" alt="Screenshot 2026-02-21 at 5 45 59 PM" src="https://github.com/user-attachments/assets/45bf4c1b-2a50-4abc-8c46-e618c1e1f3f5" />


As expected, the stdlib heappq is roughly 4 times faster than the indexed_pq implementation. <br>
This makes sense since the indexed pq needs to track additional operations for its key using a slow hashmap.<br>
Moreover, stdlib heapq is implemented in C, which makes each instruction much more optimized.

<br/>

### Djikstra Test
<img width="800" height="591" alt="Screenshot 2026-02-21 at 5 44 22 PM" src="https://github.com/user-attachments/assets/b29f0085-344d-4845-b924-ad66958ef3ee" />

The results are more favourable, and this likely because `index_heap()` constraints the heap size to number of vertices V.<br>
Wherein `heapq` lazy deletion, outdate nodes are not cleaned which makes the heap scale with edges E. <br>
Depending on graph density, this has varying impact.

<br/>

### Verdict

Overall, in terms of raw speed `heapq` is superior. Did `index_heap()` perform as well as I hope? Not particularly. <br>
But in the very least, implementing it djikstra did feel idiomatic and clean, which probably signals that its API design is passable (kudos me). 

However, benchmarking `fix_heap()` alone (no class wrapper) against lazy deletion, shows that they are nearly identical in speed.
<img width="800" height="583" alt="Screenshot 2026-02-21 at 9 18 02 PM" src="https://github.com/user-attachments/assets/4857d524-46f9-4ec1-9e76-2a88c2649033" />

The suggests that the latency in `index_heap()` comes from Python's OOP layer & hashmap operations.<br>
With better optimization like CPython support, indexed pqs could perform better



<br/>

## 🏁 Closing Thoughts 

When evaluating this library, I asked myself these hard questions:

- **Does it work?** Yes. 

- **Is it faster?** Nope. Pure heapq is C, and doesnt require extra operations for indexing

- **Is it better?** Maybe. If you are memory-constrained or lazy to maintain a stale set

- **Do I like it?** Yes, because I made it.

In conclusion, I would say I did not waste my time on this, as it has been fun trying to modify and optimize an existing lib for a real need I have.
