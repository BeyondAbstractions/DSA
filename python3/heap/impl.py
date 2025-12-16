# A heap is a nearly complete binary tree: all but the last level is completely filled
# Memory wise it is represented as an array with the relations:
# parent(i) = i//2 - 1
# left(i) = i*2 + 1
# right(i) = i*2 + 2

# Leaf nodes start appearing at (n-1)//2, (n-1)//2 + 1, ... n-1
# The last parent is at index (n-1)//2 - 1
# The first leaf is at index (n-1)//2
# Why ?
# Every leaf node must have a parent otherwise you get a disjoint heap forest which is not a nearly complete binary tree.
# parent(n-1) = (n-1)//2 - 1
# left((n-1)//2 - 1) = 2*((n-1)//2 - 1) + 1 = n - 1 - 2 + 1 = n - 2 = 2nd last index in a 0 based index scheme
# right((n-1)//2 - 1) = 2*((n-1)//2) + 2 = n - 1 - 2 + 1 = n - 1 = last index in a 0 based index scheme
# So the last parent is at (n-1)//2 - 1.
# The first leaf is at (n-1)//2.
# Any i > than the last parent i.e i > (n-1)//2 - 1 will result in a index >= n.
# left(n//2) = 2*(n//2) + 1 = n + 1 >= n, so no more leaves.
# right(n//2) = 2*(n//2) + 2 = n + 2 >= n, so no more leaves.

# The heap property is that for every node i other than root, we have A[parent(i)] >= A[i] for max heap
# and A[parent(i)] <= A[i] for min heap.


import abc


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

    def parent(self, i):
        return (i // 2) - 1

    def left(self, i):
        return 2 * i + 1

    def right(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def get(self, i):
        return self.heap[i]

    def heapify(self, i):
        root = i

        while 1:
            left = self.left(root)
            right = self.right(root)

            assert left > right

            if left >= self.heapsize:
                break

            lorsm = root

            if self.heapify_compare(lorsm, left):
                lorsm = left
            elif self.heapify_compare(lorsm, right):
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


class MaxHeap(object):

    def __init__(self, l=[], comparator=DefaultComparator()):
        Heap.__init__(self, l=l, comparator=comparator)

    def heapify_compare(self, lhs, rhs):
        lhs_val = self.get(lhs)
        rhs_val = self.get(rhs)
        return self.comparator.gt(lhs_val, rhs_val)


class MinHeap(object):
    def __init__(self, l=[], comparator=DefaultComparator()):
        Heap.__init__(self, l=l, comparator=comparator)

    def heapify_compare(self, lhs, rhs):
        lhs_val = self.get(lhs)
        rhs_val = self.get(rhs)
        return self.comparator.lt(lhs_val, rhs_val)


MinPriorityQ = MinHeap
MaxPriorityQ = MaxHeap
