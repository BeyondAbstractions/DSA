from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:

    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        ret = list()
        st = list()

        if root is not None:
            st.append((root, "l"))

        while st:
            node, state = st.pop()
            if state == "l":
                if node.left is not None:
                    st.append((node, "p"))
                    st.append((node.left, "l"))

                if node.left is None:
                    st.append((node, "p"))

            elif state == "p":
                ret.append(node.val)
                st.append((node, "r"))

            elif state == "r":
                if node.right is not None:
                    st.append((node.right, "l"))

        return ret
