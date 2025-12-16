# link: https://leetcode.com/problems/minimum-number-of-vertices-to-reach-all-nodes/description/?envType=problem-list-v2&envId=graph

from typing import List
from collections import defaultdict


class Solution:
    def findSmallestSetOfVertices(self, n: int, edges: List[List[int]]) -> List[int]:
        indeg = defaultdict(int)
        for s, d in edges:
            indeg[d] += 1

        return [i for i in range(n) if indeg[i] == 0]


import unittest


class Test(unittest.TestCase):

    def test_case0(self):
        pass


if __name__ == "__main__":
    unittest.main()
