# https://www.geeksforgeeks.org/problems/top-view-of-binary-tree/1

from collections import deque


class Node:
    def __init__(self, val):
        self.right = None
        self.data = val
        self.left = None


class Solution:

    def topView(self, root: Node):

        view = dict()
        q = deque()
        ret = list()

        if root is not None:
            q.append((root, 0))

        while q:
            node, x = q.popleft()

            if x not in view:
                view[x] = node.data

            if node.left is not None:
                q.append((node.left, x - 1))

            if node.right is not None:
                q.append((node.right, x + 1))

        for k in sorted(view.keys()):
            ret.append(view[k][1])

        return ret
