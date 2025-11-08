# https://leetcode.com/problems/sliding-window-maximum/


from typing import List
from collections import deque


# hint monotonic q
# https://medium.com/algorithms-and-leetcode/monotonic-queue-explained-with-leetcode-problems-7db7c530c1d6


class Solution:

    def fill_window(self, arr: List[int], k):
        max_element = -(10**4) - 1
        dq = deque()
        i = k - 1

        while 1:
            if i < 0:
                break

            current_element = arr[i]

            if current_element > max_element:
                max_element = current_element
                dq.appendleft((current_element, i))

            i -= 1

        return dq

    def move_window(self, i: int, dq: deque, arr: List[int], k):

        if (i - k) >= dq[0][-1]:
            dq.popleft()

        while 1:
            if not dq:
                break

            if dq[-1][0] > arr[i]:
                break

            dq.pop()

        dq.append((arr[i], i))

    def maxSlidingWindow(self, arr: List[int], k: int) -> List[int]:
        len_arr = len(arr)
        dq = self.fill_window(arr, k)
        ret = list()
        ret.append(dq[0][0])
        i = k
        while 1:

            if i >= len_arr:
                break

            self.move_window(i, dq, arr, k)
            assert len(dq) > 0

            ret.append(dq[0][0])

            i += 1

        return ret
