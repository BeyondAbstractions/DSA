from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:

        preorder = list()
        inorder = list()
        postorder = list()

        st = list()

        if root is not None:
            st.append((root, "preorder"))

        while st:
            top = st.pop()
            node, state = top
            if state == "preorder":
                preorder.append(node.data)
                st.append((node, "left"))
            elif state == "left":
                st.append((node, "inorder"))
                if node.left is not None:
                    st.append((node.left, "preorder"))
            elif state == "inorder":
                inorder.append(node.data)
                st.append((node, "right"))
            elif state == "right":
                st.append((node, "postorder"))
                if node.right is not None:
                    st.append((node.right, "preorder"))
            elif state == "postorder":
                postorder.append(node.data)

        return [preorder, inorder, postorder]
