# https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/description/


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def lowestCommonAncestor(
        self, root: "TreeNode", p: "TreeNode", q: "TreeNode"
    ) -> "TreeNode":
        it = root
        while it is not None:
            if p.val < it.val and q.val < it.val:
                it = it.left
                continue

            if p.val > it.val and q.val > it.val:
                it = it.right
                continue

            if (p.val > it.val and q.val < it.val) or (
                p.val < it.val and q.val > it.val
            ):
                return it

            if (p.val == it.val and (q.val < it.val or q.val > it.val)) or (
                q.val == it.val and (p.val < it.val or p.val > it.val)
            ):
                return it
