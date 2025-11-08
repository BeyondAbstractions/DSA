# https://www.hackerrank.com/challenges/min-max-riddle/problem


from typing import List
from collections import deque


# hint monotonic q
# https://medium.com/algorithms-and-leetcode/monotonic-queue-explained-with-leetcode-problems-7db7c530c1d6


class Solution:

    def fill_window(self, arr: List[int], k):
        min_element = (10**9) + 1
        dq = deque()
        i = k - 1

        while 1:
            if i < 0:
                break

            current_element = arr[i]

            if current_element <= min_element:
                min_element = current_element
                dq.appendleft((current_element, i))

            i -= 1

        return dq

    def move_window(self, i: int, dq: deque, arr: List[int], k):

        if (i - k) >= dq[0][-1]:
            dq.popleft()

        while 1:
            if not dq:
                break

            if dq[-1][0] < arr[i]:
                break

            dq.pop()

        dq.append((arr[i], i))

    def minSlidingWindow(self, arr: List[int], k: int) -> List[int]:
        len_arr = len(arr)
        dq = self.fill_window(arr, k)
        ret = dq[0][0]
        i = k
        while 1:

            if i >= len_arr:
                break

            self.move_window(i, dq, arr, k)
            assert len(dq) > 0

            ret = max(ret, dq[0][0])

            i += 1

        return ret

    def max_of_min(self, arr):
        arr_len = len(arr)
        ret = list()
        for i in range(1, arr_len + 1):
            ret.append(self.minSlidingWindow(arr, i))
        return ret
