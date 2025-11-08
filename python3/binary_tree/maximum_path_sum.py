# https://leetcode.com/problems/binary-tree-maximum-path-sum/

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:

        max_sum = 0
        max_val = -1001
        f = False

        def solve(root):
            nonlocal max_sum, f, max_val
            if root is None:
                return 0

            max_val = max(max_val, root.val)

            left = solve(root.left)
            right = solve(root.right)

            if left > max_sum:
                max_sum = left
                f = True

            if right > max_sum:
                max_sum = right
                f = True

            if root.val + left + right > max_sum:
                max_sum = root.val + left + right
                f = True

            if root.val + max(left, right) < 0:
                if root.val < 0:
                    return 0
                else:
                    return root.val
            else:
                return root.val + max(left, right)

        solve(root)

        if f:
            return max_sum
        else:
            return max_val
