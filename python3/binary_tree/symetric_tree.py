# https://leetcode.com/problems/symmetric-tree/

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:

        def solve(root0, root1):

            if root0 is None and root1 is None:
                return True

            elif root0 is not None and root1 is not None and root0.val == root1.val:
                return solve(root0.left, root1.right) and solve(root0.right, root1.left)

            else:
                return False

        return solve(root, root)
