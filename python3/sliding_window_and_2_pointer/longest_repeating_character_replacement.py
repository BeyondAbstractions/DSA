# https://leetcode.com/problems/longest-repeating-character-replacement/

import string


class Solution:

    def solve(self, s: str, k: int, target: str) -> int:
        i = 0
        j = 0
        max_ret = 0
        org_k = k
        len_s = len(s)
        state = "init"

        while 1:

            if state == "init":
                if i >= len_s or j >= len_s:
                    state = "done"
                elif s[i] == target:
                    state = "one"
                else:
                    state = "zero"
                continue

            elif state == "one":
                while 1:
                    if j >= len_s:
                        state = "done"
                        break

                    if s[j] != target:
                        state = "zero"
                        break

                    j += 1
                max_ret = max(max_ret, j - i)
                continue

            elif state == "zero":
                if k > 0:
                    while 1:
                        if j >= len_s:
                            state = "done"
                            break

                        if s[j] == target:
                            state = "one"
                            break

                        if k == 0:
                            state = "kis0"
                            break

                        j += 1
                        k -= 1

                    max_ret = max(max_ret, j - i)
                else:
                    state = "kis0"
                continue

            elif state == "kis0":
                assert k == 0

                while 1:
                    if i == j:
                        assert org_k == 0
                        i += 1
                        j += 1
                        state = "init"
                        break

                    if s[i] != target:
                        assert org_k != 0
                        i += 1
                        k += 1
                        if i == j:
                            state = "init"
                        else:
                            state = "zero"
                        break

                    i += 1
                max_ret = max(max_ret, j - i)
                continue

            elif state == "done":
                max_ret = max(max_ret, j - i)
                break

        return max_ret

    def characterReplacement(self, s: str, k: int) -> int:
        max_ret = 0
        for c in string.ascii_uppercase:
            max_ret = max(self.solve(s=s, k=k, target=c), max_ret)
        return max_ret
