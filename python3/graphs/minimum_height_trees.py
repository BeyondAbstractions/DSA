# link: https://leetcode.com/problems/minimum-height-trees/description/?envType=problem-list-v2&envId=graph

from typing import List
from collections import deque


class Solution:
    def findMinHeightTrees_bruteforce(
        self, n: int, edges: List[List[int]]
    ) -> List[int]:
        G = {i: list() for i in range(n)}

        for s, d in edges:
            G[s].append(d)
            G[d].append(s)

        min_height = 10**5
        ret = dict()

        for s in G:
            q = deque()
            q.append((s, 0))
            visited = set()
            max_height = -1
            while q:
                current, ht = q.popleft()
                visited.add(current)
                neibh = G[current]

                if ht > max_height:
                    max_height = ht

                for d in filter(lambda _n: _n not in visited, neibh):
                    new_ht = ht + 1
                    q.append((d, new_ht))

            if max_height < min_height:
                min_height = max_height
                ret.clear()
                ret[s] = None
            elif max_height == min_height:
                ret[s] = None
        return list(ret.keys())

    def findMinHeightTrees_optimized(self, n: int, edges: List[List[int]]) -> List[int]:
        return list()

    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        # return self.findMinHeightTrees_bruteforce(n=n, edges=edges)
        return self.findMinHeightTrees_optimized(n=n, edges=edges)


import unittest


class Test(unittest.TestCase):

    def test_findMinHeightTrees_0(self):
        s = Solution()
        n = 4
        edges = [[1, 0], [1, 2], [1, 3]]
        ret = s.findMinHeightTrees(n=n, edges=edges)
        print()
        print("ret = ", ret)
        self.assertEqual(ret, [1])

    def test_findMinHeightTrees_1(self):
        s = Solution()
        n = 6
        edges = [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]
        ret = s.findMinHeightTrees(n=n, edges=edges)
        print()
        print("ret = ", ret)
        self.assertEqual(ret, [3, 4])

    def test_findMinHeightTrees_2(self):
        s = Solution()
        n = 6
        edges = [[0, 1], [0, 2], [0, 3], [3, 4], [4, 5]]
        ret = s.findMinHeightTrees(n=n, edges=edges)
        print()
        print("ret = ", ret)
        self.assertEqual(ret, [3])


if __name__ == "__main__":
    unittest.main()
