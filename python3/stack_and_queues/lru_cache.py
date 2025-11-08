# https://leetcode.com/problems/lru-cache/


class Key:

    def __init__(self, key=None):
        self.key = key
        self.next = None
        self.prev = None

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, value):
        return self.key == getattr(value, "key", None)


class Value:

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value


class LRUCache:

    def __init__(self, capacity: int):
        self.lru = None
        self.mru = None
        self.capacity = capacity
        self.cache = dict()

    def get(self, key: int) -> int:
        key = Key(key=key)
        if key in self.cache:
            # assert self.lru is not None
            # assert self.mru is not None
            # assert self.mru.next is None

            key = self.cache[key].key
            # assert key in self.cache

            value = self.cache[key].value

            if key is self.lru and key.next is not None:
                self.lru = key.next

            if key is not self.mru:
                if key.prev is not None:
                    key.prev.next = key.next

                if key.next is not None:
                    key.next.prev = key.prev

                key.next = None
                key.prev = None

                self.mru.next = key
                key.prev = self.mru
                self.mru = key

            return value
        else:
            return -1

    def put(self, key: int, value: int) -> None:
        key = Key(key=key)
        if key in self.cache:
            key = self.cache[key].key
            self.cache[key].value = value

            if key is self.lru and key.next is not None:
                self.lru = key.next

            if key is not self.mru:
                if key.prev is not None:
                    key.prev.next = key.next

                if key.next is not None:
                    key.next.prev = key.prev

                key.next = None
                key.prev = None

                self.mru.next = key
                key.prev = self.mru
                self.mru = key
        else:
            value = Value(key=key, value=value)

            if not self.cache:
                self.lru = key
            elif len(self.cache) == self.capacity:
                # assert self.lru in self.cache
                self.cache.pop(self.lru)
                # assert self.lru not in self.cache

                if self.lru is self.mru:
                    self.mru = None

                if self.lru.next is not None:
                    self.lru.next.prev = None
                    lru = self.lru
                    self.lru = self.lru.next
                    lru.next = None
                else:
                    self.lru = key

            if self.mru is not None:
                self.mru.next = key
                key.prev = self.mru

            self.mru = key
            self.cache[key] = value

            # assert self.cache[key].key is key
