# https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/

from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        ret = list()
        vorder = dict()

        def solve(root, x, y):
            if root is None:
                return

            if x not in vorder:
                vorder[x] = dict()
                vorder[x][y] = list()
            else:
                if y not in vorder[x]:
                    vorder[x][y] = list()

            vorder[x][y].append(root.val)

            solve(root.left, x - 1, y + 1)
            solve(root.right, x + 1, y + 1)

        solve(root, 0, 0)

        for x in sorted(vorder.keys()):
            v = list()
            for y in sorted(vorder[x].keys()):
                v += sorted(vorder[x][y])
            ret.append(v)

        return ret
