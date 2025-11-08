# https://www.geeksforgeeks.org/problems/floor-in-bst/1?utm_source=youtube&utm_medium=collab_striver_ytdescription&utm_campaign=floor-in-bst


class Solution:
    def floor(self, root, x):

        last_right = None
        it = root

        while it is not None:

            if it.data == x:
                return x

            if x > it.data:
                last_right = it
                it = it.right
            else:
                it = it.left

        if last_right is None:
            return -1
        else:
            return last_right.data
