# link: https://leetcode.com/problems/all-ancestors-of-a-node-in-a-directed-acyclic-graph/description/?envType=problem-list-v2&envId=graph

from typing import List
from collections import defaultdict
from collections import deque


class Solution:
    def getAncestors(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        g = defaultdict(list)
        ind = defaultdict(int)
        for x, y in edges:
            g[x].append(y)
            ind[y] += 1

        q = deque()
        for i in range(n):
            if ind[i] == 0:
                q.append(i)

        pi = defaultdict(set)
        ancestors = defaultdict(set)
        ret = defaultdict(list)

        def get_ancestors(node) -> set:
            nonlocal pi, ancestors
            ret = set()
            for p in pi[node]:
                ret.add(p)
                ret |= ancestors[p]
            ancestors[node] = ret
            return ret

        while q:
            node = q.popleft()
            for child in g[node]:
                pi[child].add(node)
                ind[child] -= 1
                if ind[child] == 0:
                    ret[child] = sorted(get_ancestors(child))
                    q.append(child)

        ret = [ret[i] for i in range(n)]
        return ret


import unittest


class Test(unittest.TestCase):

    def test_case0(self):
        print()
        s = Solution()
        edges = [[0, 3], [0, 4], [1, 3], [2, 4], [2, 7], [3, 5], [3, 6], [3, 7], [4, 6]]
        ret = s.getAncestors(8, edges)
        import pprint

        pprint.pprint(ret)


if __name__ == "__main__":
    unittest.main()
