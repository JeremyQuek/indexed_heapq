# An example boiler solution to Leetcode 480. Sliding Window Median, solved with IPQ 

class Solution:
    def medianSlidingWindow(self, nums, k):
        if k == 1:
            return [float(x) for x in nums]

        lwr = index_pq_max()
        upp = index_pq()

        for i in range(k):
            lwr.push(nums[i], i)
        
        for _ in range(k - k // 2):
            val, key = lwr.pop()
            upp.push(val, key)

        def get_median():
            if k % 2 == 1:
                return float(upp[0])
            return (upp[0] + lwr[0]) / 2

        def balance():
            if len(lwr) > len(upp):
                val, key = lwr.pop()
                upp.push(val, key)
            elif len(upp) > len(lwr) + 1:
                val, key = upp.pop()
                lwr.push(val, key)

        res = [get_median()]

        for i in range(k, len(nums)):
            exp = i - k
            if exp in lwr:
                lwr.remove(exp)
            else:
                upp.remove(exp)
            top_upp = upp[0] if len(upp) else float('inf')
            if nums[i] >= top_upp:
                upp.push(nums[i], i)
            else:
                lwr.push(nums[i], i)
            balance()
            res.append(get_median())
        return res


class index_pq:
    def __init__(self, lst=None):
        self._reset()
        if lst is not None:
            self._heapify(lst)

    def get(self, key):
        # Dict auto raises key error
        return self._heap[self._index[key]][0]

    def push(self, value, key=None):
        if key is None:
            # Generate a unique key that doesnt collide with any existing user key
            while True:
                key = next(self._key)
                if key not in self._index:
                    break
        elif key in self._index:
            raise IndexError(f"Key: {key} already exists in the heap.")

        self._heappush((value, key))
        return key

    def pop(self):
        # Auto raise error if heap is emtpy
        value, key = self._heappop()
        return value, key

    def remove(self,key):
        if key not in self._index:
            raise KeyError(f"Key: {key} does not exist in the heap.")
        return self._heapremove(key)

    def update(self, key, value):
        if key not in self._index:
            raise KeyError(f"Key: {key} does not exist in the heap.")
        self._heapfix(key, value)

    def map(self):
        """"

        THIS OPERATION IS O(N) time!
        It might be better to maintain your own mapping of keys to values that rely on this frequently

        """

        if not self._warned:
            warnings.warn(
                "index_pq.map() is O(n); consider maintaining your own map for frequent access.",
                category=UserWarning,
                stacklevel=2
            )

        self._warned = True
        return {k:self._index[v] for (k,v) in self._index.items()}

    def clear(self):
        self._reset()


    def _reset(self):
        self._heap = []
        self._index = {}
        self._key =  itertools.count()
        self.warned = False

    def _heapify(self, lst):
        """

        Takes in a list as a one time built function for the heap.

        """
        if isinstance(lst, list):
            for value in lst:
                self.push(value)
            return

        if isinstance(lst, dict):
            for (k,v) in lst.items():
                self.push((v,k))

        raise TypeError("Must initialise with list or dict")

    def _heappush(self, item):
        # item is (value, key)
        self._index[item[1]] = len(self._heap)
        self._heap.append(item)
        self._indexed_siftdown(0, len(self._heap) - 1)

    def _heappop(self):
        lastitem = self._heap.pop()

        if self._heap:
            returnitem = self._heap[0]

            # Sync: Mark the popped ID as -1 and move the last element to root
            self._index.pop(returnitem[1])
            self._index[lastitem[1]] = 0

            self._heap[0] = lastitem
            self._indexed_siftup(0)
            return returnitem

        # Handle the case where the heap only had one item
        self._index.pop(lastitem[1])
        return lastitem

    def _heapfix(self, key, value) -> None:
        item_idx = self._index[key]

        old_value = self._heap[item_idx][0]
        if old_value == value:
            return

        self._heap[item_idx] = (value, key)
        # If new value is greater, it might need to move down
        # If new value is smaller, it might need to move up
        if value > old_value:
            self._indexed_siftup(item_idx)
        else:
            self._indexed_siftdown(0, item_idx)

    def _heapremove(self, key):
        old_value = self.get(key)
        delete_idx = self._index[key]
        bottom_value, bottom_key = self._heap[-1]
        
        self._heap.pop()
        self._index.pop(key)
        
        if delete_idx != len(self._heap):
            self._heap[delete_idx] = (bottom_value, bottom_key)
            self._index[bottom_key] = delete_idx
            # Try both directions
            self._indexed_siftdown(0, delete_idx)
            self._indexed_siftup(delete_idx)
        return old_value


    def _indexed_siftdown(self, startpos, pos):
        newitem = self._heap[pos]
        while pos > startpos:
            parentpos = (pos - 1) >> 1
            parent = self._heap[parentpos]
            if newitem < parent:
                self._heap[pos] = parent
                self._index[parent[1]] = pos
                pos = parentpos
                continue
            break
        self._heap[pos] = newitem
        self._index[newitem[1]] = pos

    def _indexed_siftup(self, pos):
        endpos = len(self._heap)
        startpos = pos
        newitem = self._heap[pos]
        childpos = 2 * pos + 1
        while childpos < endpos:
            rightpos = childpos + 1
            if rightpos < endpos and not self._heap[childpos] < self._heap[rightpos]:
                childpos = rightpos
            child_item = self._heap[childpos]
            self._heap[pos] = child_item
            self._index[child_item[1]] = pos
            pos = childpos
            childpos = 2 * pos + 1

        self._heap[pos] = newitem
        self._index[newitem[1]] = pos
        self._indexed_siftdown(startpos, pos)

    def __str__(self)->None:
        return str([v[0] for v in self._heap])

    def __len__(self)->None:
        return len(self._heap)

    def __contains__(self, key)->None:
        return (key in self._index)

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            # Support slicing
            return [self._heap[i][0] for i in range(*idx.indices(len(self._heap)))]
        else:
            # Single index access
            return self._heap[idx][0]

    def __repr__(self):
        return f"<{self.__class__.__name__} with {len(self)} elements>"

class index_pq_max:
    def __init__(self, lst=None):
        self._reset()
        if lst is not None:
            self._heapify_max(lst)

    def get(self, key):
        # Dict auto raises key error
        return self._heap[self._index[key]][0]

    def push(self, value, key=None):
        if key is None:
            # Generate a unique key that doesnt collide with any existing user key
            while True:
                key = next(self._key)
                if key not in self._index:
                    break
        elif key in self._index:
            raise IndexError(f"Key: {key} already exists in the heap.")

        self._heappush_max((value, key))
        return key

    def pop(self):
        # Auto raise error if heap is emtpy
        value, key = self._heappop_max()
        return value, key

    def remove(self,key):
        if key not in self._index:
            raise KeyError(f"Key: {key} does not exist in the heap.")
        return self._heapremove_max(key)

    def update(self, key, value):
        if key not in self._index:
            raise KeyError(f"Key: {key} does not exist in the heap.")
        self._heapfix_max(key, value)

    def map(self):
        # Maps key to index in heap
        if not self._warned:
            warnings.warn(
                "index_pq.map() is O(n); consider maintaining your own map for frequent access.",
                category=UserWarning,
                stacklevel=2
            )
        self._warned = True
        return {k:self._index[v] for (k,v) in self._index.items()}

    def clear(self):
        self._reset()

    def _reset(self):
        self._heap = []
        self._index = {}
        self._key =  itertools.count()
        self._warned = False

    def _heapify_max(self, lst):
        """

        Takes in a list as a one time built function for the heap.

        """
        if isinstance(lst, list):
            for value in lst:
                self.push(value)
            return

        if isinstance(lst, dict):
            for (k,v) in lst.items():
                self.push((v,k))

        raise TypeError("Must initialise with list or dict")

    def _heappush_max(self, item):
        # item is (value, key)
        self._index[item[1]] = len(self._heap)
        self._heap.append(item)
        self._indexed_siftdown_max(0, len(self._heap) - 1)

    def _heappop_max(self):
        lastitem = self._heap.pop()

        if self._heap:
            returnitem = self._heap[0]

            # Sync: Mark the popped ID as -1 and move the last element to root
            self._index.pop(returnitem[1])
            self._index[lastitem[1]] = 0

            self._heap[0] = lastitem
            self._indexed_siftup_max(0)
            return returnitem

        # Handle the case where the heap only had one item
        self._index.pop(lastitem[1])
        return lastitem

    def _heapfix_max(self, key, value) -> None:
        item_idx = self._index[key]

        old_value = self._heap[item_idx][0]
        if old_value == value:
            return

        self._heap[item_idx] = (value, key)
        # If new value is greater, it might need to move down
        # If new value is smaller, it might need to move up
        if value < old_value:
            self._indexed_siftup_max(item_idx)
        else:
            self._indexed_siftdown_max(0, item_idx)

    def _heapremove_max(self, key):
        old_value = self.get(key)
        delete_idx = self._index[key]
        bottom_value, bottom_key = self._heap[-1]
        
        self._heap.pop()
        self._index.pop(key)
        
        if delete_idx != len(self._heap):
            self._heap[delete_idx] = (bottom_value, bottom_key)
            self._index[bottom_key] = delete_idx
            self._indexed_siftdown_max(0, delete_idx)
            self._indexed_siftup_max(delete_idx)
        return old_value

    def _indexed_siftdown_max(self, startpos, pos):
        newitem = self._heap[pos]
        while pos > startpos:
            parentpos = (pos - 1) >> 1
            parent = self._heap[parentpos]
            if parent < newitem:
                self._heap[pos] = parent
                self._index[parent[1]] = pos
                pos = parentpos
                continue
            break
        self._heap[pos] = newitem
        self._index[newitem[1]] = pos

    def _indexed_siftup_max(self, pos):
        endpos = len(self._heap)
        startpos = pos
        newitem = self._heap[pos]
        childpos = 2 * pos + 1
        while childpos < endpos:
            rightpos = childpos + 1
            if rightpos < endpos and not self._heap[rightpos] < self._heap[childpos]:
                childpos = rightpos
            child_item = self._heap[childpos]
            self._heap[pos] = child_item
            self._index[child_item[1]] = pos
            pos = childpos
            childpos = 2 * pos + 1

        self._heap[pos] = newitem
        self._index[newitem[1]] = pos
        self._indexed_siftdown_max(startpos, pos)

    def __str__(self)->None:
        return str([v[0] for v in self._heap])

    def __len__(self)->None:
        return len(self._heap)

    def __contains__(self, key)->None:
        return (key in self._index)

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            # Support slicing
            return [self._heap[i][0] for i in range(*idx.indices(len(self._heap)))]
        else:
            # Single index access
            return self._heap[idx][0]

    def __repr__(self):
        return f"<{self.__class__.__name__} with {len(self)} elements>"
