# https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/

from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        i = len(postorder) - 1

        def solve(l, r):
            nonlocal inorder, postorder, i
            if i < 0:
                return None

            root = TreeNode()
            root.val = postorder[i]

            val = inorder.index(postorder[i])

            if (val + 1) in range(l, r + 1):
                i -= 1
                root.right = solve(val + 1, r)

            if (val - 1) in range(l, r + 1):
                i -= 1
                root.left = solve(l, val - 1)

            return root

        return solve(0, len(inorder) - 1)
