# https://www.geeksforgeeks.org/problems/implementing-ceil-in-bst/1


class Solution:
    def findCeil(self, root, inp):
        last_left = None
        it = root

        while it is not None:
            if it.key == n:
                return n

            if inp > it.key:
                it = it.right
            else:
                last_left = it
                it = it.left

        if last_left is None:
            return -1
        else:
            return last_left.key
