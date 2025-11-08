# https://leetcode.com/problems/search-in-a-binary-search-tree/description/


from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        it = root
        while 1:

            if it is None:
                break

            if it.val > val:
                it = it.left
            elif it.val < val:
                it = it.right
            else:
                return it

        return None
