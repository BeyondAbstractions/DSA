# https://www.geeksforgeeks.org/problems/predecessor-and-successor/1


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class Solution:

    def ceil(self, root, key):
        it = root
        left = None
        while it is not None:
            if key >= it.key:
                it = it.right
            else:
                left = it
                it = it.left
        if left is not None:
            return left.key
        else:
            return None

    def floor(self, root, key):
        it = root
        right = None
        while it is not None:
            if key > it.key:
                right = it
                it = it.right
            else:
                it = it.left
        if right is not None:
            return right.key
        else:
            return None

    def findPreSuc(self, root, pre, suc, key):
        suc.key = self.ceil(root, key)
        pre.key = self.floor(root, key)
