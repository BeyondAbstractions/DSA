# link: https://leetcode.com/problems/min-cost-to-connect-all-points/description/?envType=problem-list-v2&envId=graph

from typing import List, Tuple, Any
import random


class DisJointSet(object):

    def __init__(self):
        # keys are all elements, value is parent
        self.pi = dict()

        # keys are always roots of the various trees
        self.size = dict()

        # number of disjoint trees/sets
        self.components = 0

    def find(self, x) -> Tuple[bool, Any]:
        if x not in self.pi:
            return (False, None)
        else:
            # find the representative root of the set that x belongs to

            # assume x itself is the root
            root = x

            # as long as x is not the root keep going up the parent chain
            while root != self.pi[root]:
                root = self.pi[root]

            # now we have found the root, let's do path compression
            # make every node on the path point directly to the root
            while x != root:
                next_x = self.pi[x]
                self.pi[x] = root
                x = next_x

            return (True, root)

    def same_set(self, x, y) -> bool:
        return self.find(x) == self.find(y)

    def union(self, x, y) -> bool:
        found_x, root_x = self.find(x)
        found_y, root_y = self.find(y)

        if not found_x or not found_y:
            return False

        if root_x == root_y:
            return True

        # make root_x the smaller tree
        if self.size[root_x] > self.size[root_y]:
            root_x, root_y = root_y, root_x

        # now root_x is the smaller tree
        # merge root_x into root_y
        self.pi[root_x] = root_y
        self.size[root_y] += self.size[root_x]
        del self.size[root_x]
        self.components -= 1
        return True

    def total(self, x) -> int:
        return self.size[self.find(x)[1]]

    def members(self, x) -> set:
        found, root = self.find(x)
        if not found:
            return set()
        else:
            # find all nodes that have root as their representative
            # and return them as a set
            return {k for k in self.pi.keys() if self.find(k)[1] == root}

    def add(self, x):
        if x not in self.pi:
            self.pi[x] = x
            self.size[x] = 1
            self.components += 1

    def isolate(self, x) -> bool:
        found, root = self.find(x)
        if not found:
            return False
        elif root == x and self.size[root] == 1:
            # x is already isolated
            return True
        else:
            members = {k for k in self.pi.keys() if self.find(k)[1] == root and k != x}
            new_root = random.choice(members)
            self.size[new_root] = len(members)
            for k in members:
                self.pi[k] = new_root

            del self.pi[x]
            del self.size[x]
            self.components -= 1

            self.add(x)

    def delete(self, x) -> bool:
        if self.isolate(x):
            del self.pi[x]
            del self.size[x]
            self.components -= 1
            return True
        else:
            return False


class Vertex(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    def __repr__(self):
        return str(self)


class Edge(object):

    def __init__(self, va, vb):
        self.va = va
        self.vb = vb
        self.distance = abs(va.x - vb.x) + abs(va.y - vb.y)

    def __lt__(self, other):
        return self.distance < other.distance

    def __str__(self):
        return "(%s, %s, %s)" % (self.distance, self.va, self.vb)

    def __repr__(self):
        return str(self)


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        pointslen = len(points)
        vlist = [0] * pointslen
        elistpointslen = pointslen - 1
        elist = [0] * (((elistpointslen * (elistpointslen + 1)) // 2))
        ds = DisJointSet()
        k = 0
        for i, (x, y) in enumerate(points):
            vlist[i] = Vertex(x, y)
            ds.add(vlist[i])
            for j in range(i - 1, -1, -1):
                elist[k] = Edge(vlist[i], vlist[j])
                k += 1
        elist = sorted(elist)
        distance = 0
        for e in elist:
            if not ds.same_set(e.va, e.vb):
                assert ds.union(e.va, e.vb)
                distance += e.distance
        return distance


# import unittest


# class Test(unittest.TestCase):

#     def test_case0(self):
#         print()
#         points = [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]
#         s = Solution()
#         ret = s.minCostConnectPoints(points=points)
#         self.assertEqual(ret, 20)


# if __name__ == "__main__":
#     unittest.main()
