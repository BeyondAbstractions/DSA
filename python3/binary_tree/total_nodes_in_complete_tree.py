from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def countNodes(self, root: Optional[TreeNode]) -> int:

        def left_height(root):
            if root is None:
                return 0

            height = 0
            while root is not None:
                root = root.left
                height += 1
            return height - 1

        def right_height(root):
            if root is None:
                return 0

            height = 0
            while root is not None:
                root = root.right
                height += 1
            return height - 1

        def solve(root):
            nonlocal left_height, right_height

            if root is None:
                return 0

            left = left_height(root)
            right = right_height(root)

            if left == right:
                return (2 ** (left + 1)) - 1
            else:
                return 1 + solve(root.left) + solve(root.right)

        return solve(root)
