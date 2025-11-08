# https://leetcode.com/problems/validate-binary-search-tree/


from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        f = True
        prev = None

        def solve(root):
            nonlocal f, prev
            if root is None:
                return

            solve(root.left)
            if prev is None:
                prev = root.val
            else:
                f = prev < root.val and f
                prev = root.val
            solve(root.right)

        solve(root)

        return f
