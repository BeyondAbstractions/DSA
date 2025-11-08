# https://leetcode.com/problems/binary-tree-preorder-traversal/description/

from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        ret = list()
        st = list()

        if root is not None:
            st.append((root, "p"))

        while st:
            top = st.pop()
            node, state = top
            if state == "p":
                ret.append(node.val)
                st.append((node, "l"))
            elif state == "l":
                if node.left is not None:
                    st.append((node, "r"))
                    st.append((node.left, "p"))
                elif node.right is not None:
                    st.append((node, "r"))
            elif state == "r":
                if node.right is not None:
                    st.append((node.right, "p"))

        return ret
