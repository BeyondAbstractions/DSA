# https://leetcode.com/problems/subsets/


import copy
from typing import List
import unittest


class Solution:
    def subsets(self, arr: List[int]) -> List[List[int]]:
        arr_len = len(arr)
        slist = list()
        slist.append(list())

        def solve(n, i, clist, slist):
            nonlocal arr_len

            if n == 0:
                if clist:
                    slist.append(copy.deepcopy(clist))
                return

            if i >= arr_len:
                return

            solve(n, i + 1, clist, slist)

            clist.append(arr[i])
            solve(n - 1, i + 1, clist, slist)
            clist.pop()

        for i in range(0, arr_len + 1):
            solve(i, 0, list(), slist)

        return slist


class Test(unittest.TestCase):

    def test_simple(self):
        s = Solution()
        inp = [1, 2, 3]
        r = s.subsets(inp)
        # print(r)


if __name__ == "__main__":
    unittest.main()
