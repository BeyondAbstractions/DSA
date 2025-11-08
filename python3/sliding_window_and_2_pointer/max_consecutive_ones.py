# https://leetcode.com/problems/max-consecutive-ones-iii/description/


from typing import List
import unittest


class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:

        i = 0
        j = 0
        max_ret = 0
        org_k = k
        len_nums = len(nums)
        state = "init"

        while 1:

            if state == "init":
                if i >= len_nums or j >= len_nums:
                    state = "done"
                elif nums[i] == 1:
                    state = "one"
                else:
                    state = "zero"
                continue

            elif state == "one":
                while 1:
                    if j >= len_nums:
                        state = "done"
                        break

                    if nums[j] == 0:
                        state = "zero"
                        break

                    j += 1
                max_ret = max(max_ret, j - i)
                continue

            elif state == "zero":
                if k > 0:
                    while 1:
                        if j >= len_nums:
                            state = "done"
                            break

                        if nums[j] == 1:
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

                    if nums[i] == 0:
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


class Test(unittest.TestCase):

    def test(self):
        s = Solution()
        ret = s.longestOnes(
            nums=[0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], k=3
        )
        self.assertEqual(0, 0)


def unittest_main():
    unittest.main()


def main():
    s = Solution()
    print(
        "longestOnes:",
        s.longestOnes(
            nums=[0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], k=3
        ),
    )


if __name__ == "__main__":
    # main()
    unittest_main()
