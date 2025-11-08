# https://leetcode.com/problems/binary-tree-level-order-traversal/


from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        ret = list()

        q1 = deque()
        q2 = deque()

        if root is not None:
            q1.append(root)

        while 1:
            f = 0

            if q1:
                f = 1
                ret.append(list((map(lambda n: n.val, q1))))

            while q1:
                node = q1.popleft()
                if node.left is not None:
                    q2.append(node.left)

                if node.right is not None:
                    q2.append(node.right)

            if q2:
                f = 1
                ret.append(list((map(lambda n: n.val, q2))))

            while q2:
                node = q2.popleft()
                if node.left is not None:
                    q1.append(node.left)

                if node.right is not None:
                    q1.append(node.right)

            if not f:
                break

        return ret
