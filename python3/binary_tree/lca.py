# https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Ret:

    def __init__(self):
        self.n1 = None
        self.n2 = None
        self.lca = None

    @staticmethod
    def __or(left, right):
        if left is not None:
            return left

        if right is not None:
            return right

        return None

    def __or__(self, other):
        ret = Ret()
        ret.n1 = Ret.__or(self.n1, other.n1)
        ret.n2 = Ret.__or(self.n2, other.n2)
        ret.lca = Ret.__or(self.lca, other.lca)
        return ret

    def __bool__(self):
        if self.n1 is not None and self.n2 is not None and self.lca is not None:
            return True
        else:
            return False


class Solution:
    def lowestCommonAncestor(
        self, root: TreeNode, p: TreeNode, q: TreeNode
    ) -> TreeNode:
        def solve(root, n1, n2):
            ret = Ret()
            if root is None:
                return ret

            ret_l = solve(root.left, n1, n2)
            if not ret_l:
                ret_r = solve(root.right, n1, n2)
            else:
                return ret_l

            ret = ret_l | ret_r

            if ret.n1 is not None and ret.n2 is not None and ret.lca is None:
                ret.lca = root
                return ret
            else:
                if root.val == n1:
                    ret.n1 = root
                    if ret.n2 is not None:
                        ret.lca = root

                elif root.val == n2:
                    ret.n2 = root
                    if ret.n1 is not None:
                        ret.lca = root

                return ret

        return solve(root, p.val, q.val).lca
