# https://www.geeksforgeeks.org/problems/burning-tree/1?utm_source=youtube&utm_medium=collab_striver_ytdescription&utm_campaign=burning-tree


class Solution:
    def minTime(self, root, target):
        ret = 0

        def solve_down(root, d):
            nonlocal ret
            if root is None:
                return

            ret = max(ret, d)

            solve_down(root.left, d + 1)
            solve_down(root.right, d + 1)

        def solve(root):
            nonlocal solve_down, ret
            if root is None:
                return 0

            if root.data == target:
                solve_down(root, 0)
                return 1

            left = solve(root.left)
            right = solve(root.right)

            if left:
                ret = max(left, ret)
                solve_down(root.right, left + 1)

            if right:
                ret = max(right, ret)
                solve_down(root.left, right + 1)

            if left:
                return left + 1

            if right:
                return right + 1

            return 0

        solve(root)

        return ret
