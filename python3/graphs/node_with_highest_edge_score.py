# link: https://leetcode.com/problems/node-with-highest-edge-score/description/?envType=problem-list-v2&envId=graph

from typing import List

from collections import defaultdict
from functools import cmp_to_key


class Solution:
    def edgeScore(self, edges: List[int]) -> int:
        score = defaultdict(int)
        for s, d in enumerate(edges):
            score[d] += s

        def comparator(a, b):
            nonlocal score
            if score[a] < score[b]:
                return -1
            elif score[a] > score[b]:
                return 1
            else:
                if a < b:
                    return 1
                elif a > b:
                    return -1
                else:
                    return 0

        return max(score.keys(), key=cmp_to_key(comparator))


# import unittest


# class Test(unittest.TestCase):

#     def test_case_0(self):
#         edges = [1, 0, 0, 0, 0, 7, 7, 5]
#         s = Solution()
#         result = s.edgeScore(edges)
#         self.assertEqual(result, 7)

#     def test_case_1(self):
#         edges = [2, 0, 0, 2]
#         s = Solution()
#         result = s.edgeScore(edges)
#         self.assertEqual(result, 0)


# if __name__ == "__main__":
#     unittest.main()
