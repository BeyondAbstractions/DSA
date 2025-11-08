# https://leetcode.com/problems/generate-parentheses/


from typing import List
import track
import functools


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        ret = set()

        def solve(m):
            if m == 0:
                return set()

            if m == 1:
                return set(["()"])

            r = set()

            i = 1
            while 1:
                if i >= m:
                    break

                for comb1 in solve(m - i):
                    if i == 1:
                        r.add("(" + comb1 + ")")
                    for comb2 in solve(i):
                        r.add(comb1 + comb2)

                i += 1

            return r

        ret = list(solve(n))
        assert len(ret) >= 1
        return ret
