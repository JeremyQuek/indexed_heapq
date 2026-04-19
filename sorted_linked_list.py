class ListBucket(object):
    def __init__(self, value):
        self.keys = set()
        self.value = value
        self.prev=None
        self.next = None

class LinkedList(object):
    def __init__(self):
        self.head = ListBucket(-1)
        self.tail = ListBucket(-1)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.map = {}
    
    def insert(self, bucket, pos):
        prev_bucket = pos
        next_bucket = pos.next

        prev_bucket.next = bucket
        bucket.prev = prev_bucket

        next_bucket.prev = bucket
        bucket.next = next_bucket
    
    def remove(self, bucket):
        prev_bucket = bucket.prev
        next_bucket = bucket.next

        prev_bucket.next = next_bucket
        next_bucket.prev = prev_bucket
    
        bucket.next = None
        bucket.prev = None
    
    def add_new_key(self, key):
        min_bucket = self.head.next

        if min_bucket.value !=1:
            new_bucket = ListBucket(1)
            new_bucket.keys.add(key)

            self.insert(new_bucket, self.head)
            self.map[key] = new_bucket

        else:
            min_bucket.keys.add(key)
            self.map[key] = min_bucket

    def inc(self, key):
        if key not in self.map:
            self.add_new_key(key)
            return 
        
        bucket = self.map[key]
        next_bucket = bucket.next

        if next_bucket.value!=bucket.value+1:
            next_bucket = ListBucket(bucket.value+1)
            self.insert(next_bucket, bucket)

        next_bucket.keys.add(key)  
        self.map[key] = next_bucket

        bucket.keys.remove(key)
        if len(bucket.keys)==0:
            self.remove(bucket)

    def dec(self, key):
        bucket = self.map[key]
        if bucket.value==1:
            del self.map[key]
            bucket.keys.remove(key)
            if len(bucket.keys)==0:
                self.remove(bucket)
            return 
    
        bucket = self.map[key]
        prev_bucket = bucket.prev

        if prev_bucket.value<bucket.value-1:
            new_bucket = ListBucket(bucket.value-1)
            self.insert(new_bucket, prev_bucket)
            prev_bucket = new_bucket

        self.map[key] = prev_bucket
        prev_bucket.keys.add(key)

        bucket.keys.remove(key)
        if len(bucket.keys)==0:
            self.remove(bucket)
