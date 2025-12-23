# A heap is a nearly complete binary tree: all but the last level is completely filled.
# 0 based indexing.
# Memory wise it is represented as an array with the relations:
# parent(i) = i // 2 if i % 2 == 1 else (i // 2) - 1
# left(i) = 2*i + 1
# right(i) = 2*i + 2

# Assuming n is odd then n-1(the last element in 0 based index scheme) will be even and parent will be (n-1)//2 - 1
# n is odd
# n-1 is even
# heap size is n.
# Leaf nodes start appearing at (n-1)//2, (n-1)//2 + 1,  ... n-1
# The last parent is at index (n-1)//2 - 1
# The first leaf is at index (n-1)//2
# Why ?
# Every leaf node must have a parent otherwise you get a disjoint heap forest which is not a nearly complete binary tree.
# parent(n-1) = (n-1)//2 - 1
# left((n-1)//2 - 1) = 2*((n-1)//2 - 1) + 1 = n - 1 - 2 + 1 = n - 2 = 2nd last index in a 0 based index scheme
# right((n-1)//2 - 1) = 2*((n-1)//2 -1) + 2 = n - 1 - 2 + 2 = n - 1 = last index in a 0 based index scheme
# So the last parent is at (n-1)//2 - 1.
# The first leaf is at (n-1)//2.
# Any i > than the last parent i.e i > (n-1)//2 - 1 will result in a index >= n.
# left((n-1)//2) = 2*((n-1)//2) + 1 = n-1 + 1 = n >= n
# right((n-1)//2) = 2*((n-1)//2) + 2 = n-1 + 2 = n + 1 >= n
# Similar analysis can be done when n is even.

# The heap property is that for every node i other than root, we have A[parent(i)] >= A[i] for max heap
# and A[parent(i)] <= A[i] for min heap.


import abc
import pprint


class Comparator(abc.ABC):

    @abc.abstractmethod
    def lt(self, lhs, rhs):
        pass

    @abc.abstractmethod
    def lte(self, lhs, rhs):
        pass

    @abc.abstractmethod
    def gt(self, lhs, rhs):
        pass

    @abc.abstractmethod
    def gte(self, lhs, rhs):
        pass


class DefaultComparator(Comparator):
    def lt(self, lhs, rhs):
        return lhs < rhs

    def lte(self, lhs, rhs):
        return lhs <= rhs

    def gt(self, lhs, rhs):
        return lhs > rhs

    def gte(self, lhs, rhs):
        return lhs >= rhs


class Heap(object):

    def __init__(self, l=[], comparator=DefaultComparator()):
        self.heap = l
        self.heapsize = len(l)
        self.comparator = comparator
        self.objmap = dict()
        for idx, obj in enumerate(l):
            self.objmap[Heap._get_obj_hash(obj)] = idx

    @staticmethod
    def _get_obj_hash(obj):
        try:
            return hash(obj)
        except:
            return id(obj)

    def parent(self, i):
        return i // 2 if i % 2 == 1 else (i // 2) - 1

    def left(self, i):
        return 2 * i + 1

    def right(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.objmap[Heap._get_obj_hash(self.heap[i])] = i
        self.objmap[Heap._get_obj_hash(self.heap[j])] = j

    def get(self, i):
        return self.heap[i]

    def set(self, i, obj):
        self.heap[i] = obj
        self.objmap[Heap._get_obj_hash(obj)] = i

    def locate(self, obj):
        return self.objmap.get(Heap._get_obj_hash(obj))

    # push the object down the heap tree until its in correct position
    def heapify(self, i):
        root = i

        while 1:
            left = self.left(root)
            right = self.right(root)

            assert left < right

            if left >= self.heapsize:
                break

            lorsm = root

            if self.heapify_compare(left, lorsm):
                lorsm = left

            if right < self.heapsize and self.heapify_compare(right, lorsm):
                lorsm = right

            if lorsm == root:
                break

            self.swap(root, lorsm)
            root = lorsm

    @abc.abstractmethod
    def heapify_compare(self, lhs, rhs):
        pass

    def build_heap(self):
        # The last parent is at index (n-1)//2 - 1
        # We need to heapify from the last parent to the root
        # This is because all leaf nodes are already heaps of size 1
        # and we can use the heapify operation to build the heap property
        # for the entire tree.

        parent_of_last_leaf = self.parent(self.heapsize - 1)
        for i in range(parent_of_last_leaf, -1, -1):
            self.heapify(i)

    def __str__(self):
        return pprint.pformat(self.heap)

    def is_empty(self):
        return self.heapsize == 0

    def extract(self):
        # minheap: replace the root with an element that is greater
        #          than the roots(non-leaf) of all subtrees in the
        #          heap at the root and push it down
        # maxheap: replace the root with an element that is smaller
        #          than the roots(non-leaf) of all subtrees in the
        #          heap at the root and push it down
        # either case you cause the corect root to come up

        if self.heapsize == 0:
            raise Exception("Heap is empty")

        root = self.get(0)
        self.swap(0, self.heapsize - 1)
        self.heapsize -= 1
        del self.objmap[Heap._get_obj_hash(root)]
        self.heapify(0)

        return root


class MaxHeap(Heap):

    def __init__(self, l=[], comparator=DefaultComparator()):
        Heap.__init__(self, l=l, comparator=comparator)

    def heapify_compare(self, lhs, rhs):
        lhs_val = self.get(lhs)
        rhs_val = self.get(rhs)
        return self.comparator.gt(lhs_val, rhs_val)

    def max(self):
        return self.get(0)

    # push the object up the heap tree until it is in the correct position
    def increase(self, obj):
        i = self.locate(obj)
        iobj = self.get(i)
        root = i

        while 1:
            if root == 0:
                break

            parent = self.parent(root)
            pobj = self.get(parent)

            if self.comparator.gt(iobj, pobj):
                self.swap(root, parent)
                root = parent
            else:
                break

        self.set(root, obj)


class MinHeap(Heap):
    def __init__(self, l=[], comparator=DefaultComparator()):
        Heap.__init__(self, l=l, comparator=comparator)

    def heapify_compare(self, lhs, rhs):
        lhs_val = self.get(lhs)
        rhs_val = self.get(rhs)
        return self.comparator.lt(lhs_val, rhs_val)

    def min(self):
        return self.get(0)

    # push the object up the heap tree until it is in the correct position
    def decrease(self, obj):
        i = self.locate(obj)
        iobj = self.get(i)
        root = i

        while 1:
            if root == 0:
                break

            parent = self.parent(root)
            pobj = self.get(parent)

            if self.comparator.lt(iobj, pobj):
                self.swap(root, parent)
                root = parent
            else:
                break

        self.set(root, obj)


MinPriorityQ = MinHeap
MaxPriorityQ = MaxHeap


import unittest


class TestHeap(unittest.TestCase):

    def test_heapify_empty(self):
        for C in [MaxHeap, MinHeap]:
            h = C([])
            h.build_heap()
            self.assertEqual(h.heap, [])

    def test_heapify_single(self):
        for C in [MaxHeap, MinHeap]:
            h = C([1])
            h.build_heap()
            self.assertEqual(h.heap, [1])

    def test_max_heapify(self):
        h = MaxHeap([4, 1, 3, 2, 16, 9, 10, 14, 8, 7, 3])
        h.build_heap()
        for i in [16, 14, 10, 9, 8, 7, 4, 3, 3, 2, 1]:
            self.assertEqual(h.extract(), i)

    def test_min_heapify(self):
        h = MinHeap([4, 1, 3, 2, 16, 9, 10, 14, 8, 7, 3])
        h.build_heap()
        for i in [1, 2, 3, 3, 4, 7, 8, 9, 10, 14, 16]:
            self.assertEqual(h.extract(), i)

    class MyComparator(Comparator):
        def lt(self, a, b):
            return a.priority < b.priority

        def gt(self, a, b):
            return a.priority > b.priority

        def lte(self, a, b):
            return a.priority <= b.priority

        def gte(self, a, b):
            return a.priority >= b.priority

    def test_heap_increase_single(self):
        from types import SimpleNamespace

        l = [SimpleNamespace(priority=1)]
        h = MaxPriorityQ(l, comparator=TestHeap.MyComparator())
        h.build_heap()
        self.assertEqual(h.max().priority, 1)

        h.max().priority = 5
        h.increase(h.max())
        self.assertEqual(h.extract().priority, 5)

    def test_heap_increase(self):
        from types import SimpleNamespace

        l = [SimpleNamespace(priority=1), SimpleNamespace(priority=2)]
        h = MaxPriorityQ(l, comparator=TestHeap.MyComparator())
        h.build_heap()
        self.assertEqual(h.max().priority, 2)

        h.get(1).priority = 5
        h.increase(h.get(1))
        self.assertEqual(h.extract().priority, 5)
        self.assertEqual(h.extract().priority, 2)

    def test_heap_decrease_single(self):
        from types import SimpleNamespace

        l = [SimpleNamespace(priority=5)]
        h = MinPriorityQ(l, comparator=TestHeap.MyComparator())
        h.build_heap()
        self.assertEqual(h.min().priority, 5)

        h.min().priority = 1
        h.decrease(h.min())
        self.assertEqual(h.extract().priority, 1)

    def test_heap_decrease(self):
        from types import SimpleNamespace

        l = [SimpleNamespace(priority=5), SimpleNamespace(priority=2)]
        h = MinPriorityQ(l, comparator=TestHeap.MyComparator())
        h.build_heap()
        self.assertEqual(h.min().priority, 2)

        before_id = Heap._get_obj_hash(h.get(1))
        h.get(1).priority = 1
        after_id = Heap._get_obj_hash(h.get(1))
        self.assertEqual(before_id, after_id)

        h.decrease(h.get(1))
        self.assertEqual(h.extract().priority, 1)
        self.assertEqual(h.extract().priority, 2)


if __name__ == "__main__":
    unittest.main()
