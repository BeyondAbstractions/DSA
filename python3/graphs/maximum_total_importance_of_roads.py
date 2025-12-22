# link: https://leetcode.com/problems/maximum-total-importance-of-roads/description/?envType=problem-list-v2&envId=graph

from typing import List


from collections import defaultdict


class Solution:
    def maximumImportance(self, n: int, roads: List[List[int]]) -> int:
        degree = defaultdict(int)
        g = defaultdict(dict)
        for s, d in roads:
            g[s][d] = None
            degree[s] += 1
            degree[d] += 1

        vertex_val = dict()
        i = n
        for vertex, _ in sorted(degree.items(), key=lambda x: x[1], reverse=True):
            vertex_val[vertex] = i
            i -= 1

        total = 0
        for s in g:
            for d in g[s]:
                total += vertex_val[s] + vertex_val[d]

        return total


# import unittest


# class Test(unittest.TestCase):

#     def test_case_0(self):
#         n = 5
#         roads = [[0, 1], [1, 2], [2, 3], [0, 2], [1, 3], [2, 4]]
#         s = Solution()
#         ret = s.maximumImportance(n=n, roads=roads)
#         self.assertEqual(ret, 43)

#     def test_case_1(self):
#         n = 5
#         roads = [[0, 3], [2, 4], [1, 3]]
#         s = Solution()
#         ret = s.maximumImportance(n=n, roads=roads)
#         self.assertEqual(ret, 20)


# if __name__ == "__main__":
#     unittest.main()
