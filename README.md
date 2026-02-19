# Indexed Priority Queues

This module provides two high-performance priority queue implementations designed to feel as native as Python’s collections.deque. These are particularly useful for shell job management where you need to update the priority of a process or remove a specific task by its ID.Features$O(\log n)$ Updates: Change the priority of an existing element instantly via its key.$O(\log n)$ Removal: Remove any element from the middle of the heap without a full scan.Auto-Key Generation: If no key is provided, the heap generates unique integer keys automatically.Slicing Support: Preview the heap contents using standard Python slicing (pq[0:5]).API Referenceindexpq (Min-Heap)Maintains elements such that the smallest value is always at the root.maxindexpq (Max-Heap)Maintains elements such that the largest value is always at the root.Common MethodsMethodComplexityDescriptionpush(value, key=None)$O(\log n)$Adds a value to the heap. Returns the key.pop()$O(\log n)$Removes and returns the top (value, key) pair.update(key, value)$O(\log n)$Updates the priority/value of an existing key.remove(key)$O(\log n)$Removes a specific key from the heap.get(key)$O(1)$Returns the current value of a key without moving it.map()$O(n)$Returns a dictionary mapping keys to their current heap index.Usage ExamplePythonfrom core import indexpq

## Initialize
jobs = indexpq()

## Push jobs with custom keys (e.g., Process IDs)
jobs.push(priority=10, key=4501)
jobs.push(priority=2, key=4502)

##Update a priority
jobs.update(4501, 1)  # PID 4501 is now higher priority (lower value)

## Pop the highest priority
val, pid = jobs.pop()
print(f"Running PID {pid} with priority {val}")

Implementation DetailsThe "Sync" MechanismThe core of these classes is the self._index dictionary. Every time a "sift" operation (up or down) moves an element in the self._heap list, the dictionary is updated to map the element's unique key to its new list_index.Time Complexity Warning[!WARNING]The map() method is an $O(n)$ operation. It is intended for debugging or infrequent snapshots. If you need to check values frequently, maintain a separate dictionary in your main shell logic.
