# https://leetcode.com/problems/binary-tree-postorder-traversal/

from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        ret = list()

        def solve(root):

            if root is None:
                return

            solve(root.left)
            solve(root.right)
            ret.append(root.val)

        solve(root)
        return ret
