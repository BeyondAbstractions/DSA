# https://www.geeksforgeeks.org/problems/children-sum-parent/1?utm_source=youtube&utm_medium=collab_striver_ytdescription&utm_campaign=hildren-sum-parent


# Node Class:
class Node:
    def init(self, val):
        self.data = val
        self.left = None
        self.right = None


class Solution:
    # Function to check whether all nodes of a tree have the value
    # equal to the sum of their child nodes.
    def isSumProperty(self, root):

        def solve(root):
            if root is None:
                return True

            if root.left is None and root.right is None:
                return True

            left = solve(root.left)

            if left:
                right = solve(root.right)
                if not right:
                    return False
            else:
                return False

            if root.left is None:
                left = 0
            else:
                left = root.left.data

            if root.right is None:
                right = 0
            else:
                right = root.right.data

            return root.data == (left + right)

        if solve(root):
            return 1
        else:
            return 0
