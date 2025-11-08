# https://leetcode.com/problems/binary-tree-preorder-traversal/

from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        ret = list()

        def solve(root):
            nonlocal ret
            if root is None:
                return

            ret.append(root.val)
            solve(root.left)
            solve(root.right)

        solve(root)
        return ret
