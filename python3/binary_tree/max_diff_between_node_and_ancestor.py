# https://leetcode.com/problems/maximum-difference-between-node-and-ancestor/


from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxAncestorDiff(self, root: Optional[TreeNode]) -> int:
        max_diff = 0

        def solve(root, max_node, min_node):
            nonlocal max_diff
            if root is None:
                return

            if root.val > max_node.val:
                max_node = root

            if root.val < min_node.val:
                min_node = root

            max_diff = max(max_diff, abs(max_node.val - min_node.val))

            solve(root.left, max_node, min_node)
            solve(root.right, max_node, min_node)

        solve(root, root, root)

        return max_diff
