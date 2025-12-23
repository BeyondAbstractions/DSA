# link: https://leetcode.com/problems/minimum-time-to-visit-disappearing-nodes/description/?envType=problem-list-v2&envId=graph

from typing import List
from collections import defaultdict


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


class Vertex(object):

    def __init__(self, id, wt=None, expire=None):
        self.id = id
        self.wt = wt
        self.expire = expire
        self.reached = False

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        if other.wt is None and self.wt is None:
            return False

        if self.wt is not None and other.wt is None:
            return True

        if self.wt is None and other.wt is not None:
            return False

        return self.wt < other.wt

    def __str__(self):
        return "[id=%s, wt=%s, expire=%s, reached=%s]" % (
            self.id,
            self.wt,
            self.expire,
            self.reached,
        )

    def __repr__(self):
        return str(self)

    def relax(self, ewt, dv):
        pwt = None
        if self.wt is not None:
            pwt = self.wt + ewt

        pdv = Vertex(id=None, wt=pwt, expire=None)

        if pdv < dv:
            if pdv.wt < dv.expire:
                dv.wt = pdv.wt
                return True
            else:
                return False
        else:
            return False


class Solution:
    def minimumTime(
        self, n: int, edges: List[List[int]], disappear: List[int]
    ) -> List[int]:

        vlist = [None] * n
        vmap = dict()
        for i in range(n):
            v = Vertex(id=i, expire=disappear[i])
            vlist[i] = v
            vmap[i] = v

        g = defaultdict(list)
        for s, d, t in edges:
            g[vlist[s]].append({"d": vlist[d], "tt": t})
            g[vlist[d]].append({"d": vlist[s], "tt": t})

        vlist[0].wt = 0
        vlist[0].reached = True

        h = MinPriorityQ(l=vlist)

        while not h.is_empty():
            v = h.extract()
            for dd in g[v]:
                dv = dd["d"]
                ewt = dd["tt"]
                if v.relax(ewt, dv):
                    dv.reached = True
                    h.decrease(dv)

        # pprint.pprint(vlist)

        return [
            vmap[i].wt if vmap[i].reached and vmap[i].wt < vmap[i].expire else -1
            for i in range(n)
        ]


# import unittest


# class Test(unittest.TestCase):

#     def test_case_0(self):
#         n = 3
#         edges = [[0, 1, 2], [1, 2, 1], [0, 2, 4]]
#         disappear = [1, 1, 5]
#         s = Solution()
#         ret = s.minimumTime(n=n, edges=edges, disappear=disappear)
#         self.assertEqual(ret, [0, -1, 4])

#     def test_case_1(self):
#         n = 3
#         edges = [[0, 1, 2], [1, 2, 1], [0, 2, 4]]
#         disappear = [1, 3, 5]
#         s = Solution()
#         ret = s.minimumTime(n=n, edges=edges, disappear=disappear)
#         self.assertEqual(ret, [0, 2, 3])

#     def test_case_2(self):
#         n = 2
#         edges = [[0, 1, 1]]
#         disappear = [1, 1]
#         s = Solution()
#         ret = s.minimumTime(n=n, edges=edges, disappear=disappear)
#         self.assertEqual(ret, [0, -1])


# if __name__ == "__main__":
#     unittest.main()
