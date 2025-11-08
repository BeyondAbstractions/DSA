# https://www.geeksforgeeks.org/problems/largest-bst/1


class Node:
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None


class Solution:
    def largestBst(self, root):

        def solve(root, parent=None):

            if root.left is None and root.right is None:
                return (root.data, 1, True)

            ldata, lcount, lbst = None, 0, True
            rdata, rcount, rbst = None, 0, True

            if root.left is not None:
                ldata, lcount, lbst = solve(root.left, parent="l")
                if lbst:
                    lbst = root.data > ldata

            if root.right is not None:
                rdata, rcount, rbst = solve(root.right, parent="r")
                if rbst:
                    rbst = root.data < rdata

            if lbst and rbst:
                if parent is None:
                    return (None, lcount + rcount + 1, True)
                elif parent == "l":
                    return (
                        rdata if root.right is not None else root.data,
                        lcount + rcount + 1,
                        True,
                    )
                elif parent == "r":
                    return (
                        ldata if root.left is not None else root.data,
                        lcount + rcount + 1,
                        True,
                    )
            else:
                return (None, max(lcount, rcount), False)

        if root is not None:
            return solve(root)[1]
        else:
            return 0
