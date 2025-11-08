# https://leetcode.com/problems/maximum-width-of-binary-tree/


from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def widthOfBinaryTree(self, root: Optional[TreeNode]) -> int:

        q1 = deque()
        q1_rc = [0]

        q2 = deque()
        q2_rc = [0]

        max_width = 0

        q = q1
        rc = q1_rc
        q.append(("real", root))
        rc[0] += 1

        counter = 0
        first_real = None
        last_real = None

        while rc[0]:
            counter += 1
            nq = None

            if q is q1:
                nq = q2
                nrc = q2_rc
            else:
                nq = q1
                nrc = q1_rc

            node_type, node = q.popleft()

            if node_type is "real":

                if first_real is None:
                    first_real = counter

                last_real = counter

                if node.left is not None:
                    nq.append(("real", node.left))
                    nrc[0] += 1
                else:
                    nq.append(("fake", 1))

                if node.right is not None:
                    nq.append(("real", node.right))
                    nrc[0] += 1
                else:
                    nq.append(("fake", 1))
            else:
                counter -= 1
                counter += node
                nq.append(("fake", 2 * node))

            if not q:
                if q is q1:
                    q = q2
                    rc = q2_rc
                    q1_rc = [0]

                else:
                    q = q1
                    rc = q1_rc
                    q2_rc = [0]

                if first_real is not None and last_real is not None:
                    max_width = max(max_width, abs(last_real - first_real + 1))

                counter = 0
                first_real = None
                last_real = None

        return max_width
