from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        i = 0
        ret = None

        def solve(root):
            nonlocal i, k, ret
            if root is None:
                return

            solve(root.left)
            i += 1
            if i == k:
                ret = root.val
            solve(root.right)

        solve(root)

        return ret
