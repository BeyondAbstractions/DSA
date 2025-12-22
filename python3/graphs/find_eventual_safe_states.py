# link: https://leetcode.com/problems/find-eventual-safe-states/description/?envType=problem-list-v2&envId=graph

import sys
from typing import List

from collections import defaultdict, deque


class Solution:
    def eventualSafeNodes_slow(self, graph: List[List[int]]) -> List[int]:
        g = defaultdict(dict)
        indegree = defaultdict(int)
        outdegree = defaultdict(int)
        terminalvertices = {i: None for i in range(len(graph))}
        safevertices = {i: None for i in range(len(graph))}

        for s, adjlist in enumerate(graph):
            for d in adjlist:
                g[s][d] = None
                indegree[d] += 1
                outdegree[s] += 1
            if outdegree[s] >= 1 and s in terminalvertices:
                del terminalvertices[s]

        path = dict()

        def dfs(s):
            nonlocal path, safevertices, g

            if s in path:
                return False

            path[s] = None

            if s not in safevertices:
                del path[s]
                return False

            if safevertices[s] is not None:
                del path[s]
                return True

            if outdegree[s] == 0:
                del path[s]
                safevertices[s] = "definitely safe"
                return True

            ret = True
            for d in g[s]:
                if ret:
                    ret = dfs(d)

            if not ret:
                if s in safevertices:
                    del safevertices[s]
                del path[s]
                return False
            else:
                safevertices[s] = "definitely safe"
                del path[s]
                return True

        sys.setrecursionlimit(10**8)
        for i in range(len(graph)):
            dfs(i)

        return [i for i in range(len(graph)) if i in safevertices]

    def eventualSafeNodes_fast(self, graph: List[List[int]]) -> List[int]:
        g = defaultdict(dict)
        indegree_rev_g = defaultdict(int)
        outdegree = defaultdict(int)
        terminalvertices = {i: None for i in range(len(graph))}
        q = deque()

        for s, adjlist in enumerate(graph):
            for d in adjlist:
                g[d][s] = None
                indegree_rev_g[s] += 1
                outdegree[s] += 1

            if outdegree[s] >= 1 and s in terminalvertices:
                del terminalvertices[s]

        for v in terminalvertices:
            q.append(v)

        ret = list()
        while q:
            current = q.popleft()
            ret.append(current)
            for d in g[current]:
                indegree_rev_g[d] -= 1
                if indegree_rev_g[d] == 0:
                    q.append(d)

        return sorted(ret)

    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        # return self.eventualSafeNodes_slow(graph=graph)
        return self.eventualSafeNodes_fast(graph=graph)


# import unittest


# class Test(unittest.TestCase):

#     def test_case_0(self):
#         graph = [[1, 2], [2, 3], [5], [0], [5], [], []]
#         s = Solution()
#         ret = s.eventualSafeNodes(graph=graph)
#         self.assertEqual(ret, [2, 4, 5, 6])

#     def test_case_1(self):
#         graph = [[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []]
#         s = Solution()
#         ret = s.eventualSafeNodes(graph=graph)
#         self.assertEqual(ret, [4])

#     def test_case_2(self):
#         graph = [[0], [1, 2, 3, 4], [1, 3, 4], [2, 4], [2]]
#         s = Solution()
#         ret = s.eventualSafeNodes(graph=graph)
#         self.assertEqual(ret, [])


# if __name__ == "__main__":
#     unittest.main()
