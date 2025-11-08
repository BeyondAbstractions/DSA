# Definition for a binary tree node.

from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:

    def get_max_index(self, start, end, arr: List[int]):
        max_i = start
        i = start

        while 1:

            if i > end:
                return max_i

            max_element = arr[max_i]
            current_element = arr[i]

            if current_element > max_element:
                max_i = i

            i += 1

    def constructMaximumBinaryTree(self, arr: List[int]) -> Optional[TreeNode]:
        arr_len = len(arr)

        def solve(l, r):
            nonlocal arr, arr_len, self

            if l > r or (l < 0 or l >= arr_len) or (r < 0 or r >= arr_len):
                return None

            max_i = self.get_max_index(l, r, arr)
            max_element = arr[max_i]

            node = TreeNode(val=max_element)
            node.left = solve(l, max_i - 1)
            node.right = solve(max_i + 1, r)

            return node

        root = solve(0, arr_len - 1)
        assert root is not None
        return root
