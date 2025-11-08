import copy


class Node:
    def _init_(self, val):
        self.data = val
        self.left = None
        self.right = None


class Solution:
    def Paths(self, root):
        ret = list()

        def solve(node, st):
            nonlocal ret
            if node.left is None and node.right is None:
                st.append(node.data)
                ret.append(copy.deepcopy(st))
                return

            st.append(node.data)

            if node.left is not None:
                solve(node.left, st)
                st.pop()

            if node.right is not None:
                solve(node.right, st)
                st.pop()

        if root is not None:
            solve(root, list())

        return ret
