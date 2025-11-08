# https://leetcode.com/problems/next-greater-element-ii/

from typing import List


class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        nums_len = len(nums)
        nge = [-1 for i in range(nums_len)]
        i = len(nums) - 2

        while 1:

            if i < 0:
                break

            next_idx = i + 1
            next_element = nums[next_idx]
            current_element = nums[i]

            while 1:

                if next_element > current_element:
                    nge[i] = next_idx
                    break

                next_idx = nge[next_idx]

                if next_idx == -1:
                    break

                next_element = nums[next_idx]

            i -= 1

        next_idx = 0
        last_idx = nums_len - 1
        current_element = nums[last_idx]
        while 1:

            if next_idx >= last_idx:
                break

            next_element = nums[next_idx]

            if next_element > current_element:
                nge[last_idx] = next_idx
                break

            next_idx += 1

        i = len(nums) - 2
        while 1:

            if i < 0:
                break

            if nge[i] == -1:
                next_idx = nge[last_idx]
                next_element = nums[next_idx]
                current_element = nums[i]

                while 1:

                    if next_idx >= i:
                        break

                    if next_element > current_element:
                        nge[i] = next_idx
                        break

                    next_idx = nge[next_idx]

                    if next_idx == -1:
                        break

                    next_element = nums[next_idx]

            i -= 1

        i = 0
        while 1:

            if i >= nums_len:
                break

            if nge[i] != -1:
                nge[i] = nums[nge[i]]
            i += 1

        return nge
