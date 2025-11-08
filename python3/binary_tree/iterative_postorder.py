from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        st = list()
        ret = list()

        if root is not None:
            st.append((root, "l"))

        while st:
            node, state = st.pop()

            if state == "l":
                st.append((node, "r"))
                if node.left is not None:
                    st.append((node.left, "l"))

            elif state == "r":
                st.append((node, "p"))
                if node.right is not None:
                    st.append((node.right, "l"))

            elif state == "p":
                ret.append(node.val)

        return ret
