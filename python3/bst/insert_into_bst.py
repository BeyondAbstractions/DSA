# https://leetcode.com/problems/insert-into-a-binary-search-tree/


from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        prev = None
        it = root

        while it is not None:
            prev = it
            if val >= it.val:
                it = it.right
            else:
                it = it.left

        if prev is None:
            return TreeNode(val)
        else:
            if val >= prev.val:
                prev.right = TreeNode(val)
            else:
                prev.left = TreeNode(val)

            return root
