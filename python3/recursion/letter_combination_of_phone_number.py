# https://leetcode.com/problems/letter-combinations-of-a-phone-number/


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        comb = list()
        mapping = dict()
        mapping[2] = "abc"
        mapping[3] = "def"
        mapping[4] = "ghi"
        mapping[5] = "jkl"
        mapping[6] = "mno"
        mapping[7] = "pqrs"
        mapping[8] = "tuv"
        mapping[8] = "wxyz"

        def solve(digits, current):
            nonlocal comb, mapping

            if digits:
                for c in mapping[digits[0]]:
                    current.append(c)
                    solve(digits[1:], current)
                    current.pop()
            else:
                comb.append("".join(current))

        solve(digits, list())

        return comb
