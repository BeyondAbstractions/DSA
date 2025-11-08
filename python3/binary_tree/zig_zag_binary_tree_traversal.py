from collections import deque
from typing import Optional, List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        ret = list()
        stack_lr = list()
        stack_rl = list()
        current_dir = "rl"

        if root is not None:
            stack_rl.append(root)

        while 1:
            data = list()
            if current_dir == "rl":
                while stack_rl:
                    element = stack_rl.pop()
                    data.append(element.data)
                    if element.right is not None:
                        stack_lr.append(element.right)
                    if element.left is not None:
                        stack_lr.append(element.left)

            if current_dir == "lr":
                while stack_lr:
                    element = stack_lr.pop()
                    data.append(element.data)
                    if element.left is not None:
                        stack_lr.append(element.left)
                    if element.right is not None:
                        stack_rl.append(element.right)

            if current_dir == "lr":
                current_dir = "rl"
            else:
                current_dir = "lr"

            if data:
                ret.append(data)

            if not stack_lr and not stack_rl:
                break

        return ret
