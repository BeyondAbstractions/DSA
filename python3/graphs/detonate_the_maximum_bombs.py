# link: https://leetcode.com/problems/detonate-the-maximum-bombs/description/?envType=problem-list-v2&envId=graph

from typing import List
from collections import defaultdict, deque
import functools


class Vertex(object):

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def __str__(self):
        return "(%s, %s, %s)" % (self.x, self.y, self.r)

    def __repr__(self):
        return str(self)


class Edge(object):

    def __init__(self, va, vb):
        self.va = va
        self.vb = vb
        self.distance = ((va.x - vb.x) ** 2 + (va.y - vb.y) ** 2) ** 0.5
        self.within_va = self.distance <= self.va.r
        self.within = self.within_va

    def __str__(self):
        return "(%s, %s, %s)" % (self.distance, self.va, self.vb)

    def __repr__(self):
        return str(self)


class Solution:
    def bfs(self, g, start):
        q = deque()
        q.append(start)
        v = dict()
        v[start] = None
        k = 0
        while q:
            k += 1
            head = q.popleft()
            for adjv in g[head]:
                if adjv not in v:
                    v[adjv] = None
                    q.append(adjv)
        return k

    def maximumDetonation(self, bombs: List[List[int]]) -> int:
        bombslen = len(bombs)
        vlist = [0] * bombslen
        g = defaultdict(list)
        for i, (x, y, r) in enumerate(bombs):
            vlist[i] = Vertex(x, y, r)
            g[vlist[i]] = list()

        for i in range(bombslen):
            for j in range(i + 1, bombslen):
                vi = vlist[i]
                vj = vlist[j]
                e = Edge(vi, vj)
                if e.within:
                    g[vi].append(vj)
                e = Edge(vj, vi)
                if e.within:
                    g[vj].append(vi)

        f = functools.partial(self.bfs, g)
        return max(map(f, g.keys()))


# import unittest


# class Test(unittest.TestCase):

#     def test_case0(self):
#         bombs = [[1, 1, 5], [10, 10, 5]]
#         s = Solution()
#         ret = s.maximumDetonation(bombs=bombs)
#         self.assertEqual(ret, 1)


# if __name__ == "__main__":
#     unittest.main()
