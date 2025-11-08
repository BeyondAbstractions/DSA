# https://leetcode.com/problems/diameter-of-binary-tree/


from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:

        dia = 0

        def solve(root):
            nonlocal dia
            if root is None:
                return 0

            left = solve(root.left)
            right = solve(root.right)

            dia = max(left + right, dia)

            return max(left, right) + 1

        solve(root)

        return dia
