# https://www.geeksforgeeks.org/problems/minimum-element-in-bst/1


class Node:
    def __init__(self, val):
        self.right = None
        self.data = val
        self.left = None


class Solution:
    def minValue(self, root):
        it = root
        while 1:
            if it is None:
                return 0

            if it.left is None:
                return it.data

            it = it.left
