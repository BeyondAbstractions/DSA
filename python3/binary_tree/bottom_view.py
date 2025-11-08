# https://www.geeksforgeeks.org/problems/bottom-view-of-binary-tree/1


class TreeNode:
    def __init__(self, data=0):
        self.data = data
        self.left = None
        self.right = None


from collections import deque


class Solution:
    def bottomView(self, root):

        view = dict()

        q = deque()

        if root is not None:
            q.append((root, 0))

        while q:
            node, x = q.popleft()
            view[x] = node.data

            if node.left is not None:
                q.append((node.left, x - 1))

            if node.right is not None:
                q.append((node.right, x + 1))

        ret = list()
        for k in sorted(view.keys()):
            ret.append(view[k])

        return ret
