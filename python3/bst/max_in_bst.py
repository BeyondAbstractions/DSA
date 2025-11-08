# https://www.geeksforgeeks.org/problems/max-and-min-element-in-binary-tree/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card


class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


class Solution:
    def findMax(self, root):
        it = root
        while 1:
            if it is None:
                return 0

            if it.right is None:
                return it.data

            it = it.right
