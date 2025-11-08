# https://leetcode.com/problems/construct-binary-search-tree-from-preorder-traversal/

from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def bstFromPreorder(self, preorder: List[int]) -> Optional[TreeNode]:
        inorder = sorted(preorder)
        i = 0

        def solve(l, r):
            nonlocal i, inorder

            root = TreeNode()
            root.val = preorder[i]

            val = inorder.index(root.val)

            if (val - 1) in range(l, r + 1):
                i += 1
                root.left = solve(l, val - 1)

            if (val + 1) in range(l, r + 1):
                i += 1
                root.right = solve(val + 1, r)

            return root

        return solve(0, len(preorder) - 1)
