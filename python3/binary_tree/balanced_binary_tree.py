# https://leetcode.com/problems/balanced-binary-tree/

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:

        def solve(root):
            if root is None:
                return (0, True)

            left_height, left_balanced = solve(root.left)

            if left_balanced:
                right_height, right_balanced = solve(root.right)

                if right_balanced:
                    if abs(left_height - right_height) <= 1:
                        return (max(left_height, right_height) + 1, True)
                    else:
                        return (0, False)
                else:
                    return (0, False)
            else:
                return (0, False)

        return solve(root)[-1]
