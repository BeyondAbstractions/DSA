# link: https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/description/?envType=problem-list-v2&envId=graph

from typing import List


from collections import defaultdict


class Solution:
    def findTheCity(
        self, n: int, edges: List[List[int]], distanceThreshold: int
    ) -> int:
        g = defaultdict(dict)
        for s, d, t in edges:
            g[s][d] = t
            g[d][s] = t

        for x in g:

            for s in g:
                if s == x:
                    continue

                for d in g:
                    if s == d or d == x:
                        continue

                    wt_sd = g[s][d] if d in g[s] else None
                    wt_sx = g[s][x] if x in g[s] else None
                    wt_xd = g[x][d] if d in g[x] else None

                    if wt_sd is None:
                        if wt_sx is not None and wt_xd is not None:
                            g[s][d] = wt_sx + wt_xd
                    else:
                        if wt_sx is None or wt_xd is None:
                            pass
                        else:
                            g[s][d] = min(wt_sd, wt_sx + wt_xd)

        min_city = None
        min_count = None
        for s in range(n):
            within_threshold = 0
            for d in g[s]:
                if s != d:
                    if g[s][d] <= distanceThreshold:
                        within_threshold += 1
            if min_count is None:
                min_count = within_threshold
                min_city = s
            else:
                if within_threshold <= min_count:
                    min_count = within_threshold
                    min_city = s
        return min_city


# import unittest


# class Test(unittest.TestCase):

#     def test_case_0(self):
#         n = 4
#         edges = [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]]
#         distanceThreshold = 4
#         s = Solution()
#         ret = s.findTheCity(n=n, edges=edges, distanceThreshold=distanceThreshold)
#         self.assertEqual(ret, 3)

#     def test_case_1(self):
#         n = 5
#         edges = [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]]
#         distanceThreshold = 2
#         s = Solution()
#         ret = s.findTheCity(n=n, edges=edges, distanceThreshold=distanceThreshold)
#         self.assertEqual(ret, 0)

#     def test_case_2(self):
#         n = 6
#         edges = [[0, 3, 7], [2, 4, 1], [0, 1, 5], [2, 3, 10], [1, 3, 6], [1, 2, 1]]
#         distanceThreshold = 417
#         s = Solution()
#         ret = s.findTheCity(n=n, edges=edges, distanceThreshold=distanceThreshold)
#         self.assertEqual(ret, 5)


# if __name__ == "__main__":
#     unittest.main()
