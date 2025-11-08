from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        ret = list()
        q = deque()
        view = dict()

        if root is not None:
            q.append((root, 0))

        while q:
            node, y = q.popleft()

            view[y] = node.val

            if node.left is not None:
                q.append((node.left, y + 1))

            if node.right is not None:
                q.append((node.right, y + 1))

        for k in sorted(view.keys()):
            ret.append(view[k])

        return ret
