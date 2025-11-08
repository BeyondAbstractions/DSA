# https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/


from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> List[int]:
        ret = list()

        def solve_down(root, d):
            nonlocal ret, k
            if root is None:
                return

            if d > k:
                return

            if d == k and k != 0:
                ret.append(root.val)

            solve_down(root.left, d + 1)
            solve_down(root.right, d + 1)

        def solve(root):
            nonlocal solve_down, k, ret
            if root is None:
                return 0

            if root.val == target.val:
                if k == 0:
                    ret.append(root.val)
                solve_down(root, 0)
                return 1

            left = solve(root.left)
            right = solve(root.right)

            if left:
                if left == k:
                    ret.append(root.val)
                solve_down(root.right, left + 1)

            if right:
                if right == k:
                    ret.append(root.val)
                solve_down(root.left, right + 1)

            if left:
                return left + 1

            if right:
                return right + 1

            return 0

        solve(root)

        return ret
