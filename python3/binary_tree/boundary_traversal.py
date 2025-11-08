# https://www.geeksforgeeks.org/problems/boundary-traversal-of-binary-tree/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card


class Node:
    def __init__(self, val):
        self.right = None
        self.data = val
        self.left = None


from collections import deque


class Solution:

    def boundaryTraversal(self, root):

        left = deque()
        right = deque()
        bottom = deque()

        if root is not None:
            if root.left is not None or root.right is not None:
                left.append(root.data)

            it = root.left
            while it is not None:
                if it.left is not None or it.right is not None:
                    left.append(it.data)

                if it.left is not None:
                    it = it.left
                else:
                    it = it.right

            it = root.right
            while it is not None:
                if it.left is not None or it.right is not None:
                    right.appendleft(it.data)

                if it.right is not None:
                    it = it.right
                else:
                    it = it.left

        def preorder(root):
            if root is None:
                return

            if root.left is None and root.right is None:
                bottom.append(root.data)

            preorder(root.left)
            preorder(root.right)

        preorder(root)

        left.extend(bottom)
        left.extend(right)

        return left
