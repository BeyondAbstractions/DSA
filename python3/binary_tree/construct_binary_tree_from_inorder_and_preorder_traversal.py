# https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/


from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        i = 0

        def solve(l, r):
            nonlocal i, preorder, inorder

            if i >= len(preorder):
                return None

            root = TreeNode()
            root.val = preorder[i]

            val = inorder.index(preorder[i])

            if (val - 1) in range(l, r + 1):
                i += 1
                root.left = solve(l, val - 1)

            if (val + 1) in range(l, r + 1):
                i += 1
                root.right = solve(val + 1, r)

            return root

        return solve(0, len(inorder) - 1)
