# link: https://leetcode.com/problems/validate-binary-tree-nodes/description/?envType=problem-list-v2&envId=graph

from typing import List
from collections import deque


class Solution:

    def update_ddict(self, root, left, right, ddict) -> bool:

        if root not in ddict:
            ddict[root] = {"in": 0, "out": 0}
        if left != -1:
            ddict[root]["out"] += 1
        if right != -1:
            ddict[root]["out"] += 1

        if ddict[root]["out"] > 2:
            return False

        if left != -1:
            if left not in ddict:
                ddict[left] = {"in": 1, "out": 0}
            else:
                ddict[left]["in"] += 1
                if ddict[left]["in"] > 1:
                    return False

        if right != -1:
            if right not in ddict:
                ddict[right] = {"in": 1, "out": 0}
            else:
                ddict[right]["in"] += 1
                if ddict[right]["in"] > 1:
                    return False

        return True

    def solve(self, n: int, leftChild: List[int], rightChild: List[int]) -> bool:
        root = None
        ddict = dict()

        for i in range(0, n):
            if not self.update_ddict(i, leftChild[i], rightChild[i], ddict):
                return False

        for i in range(0, n):
            if ddict[i]["in"] == 0:
                if root is None:
                    root = i
                else:
                    return False

        if root is None:
            return False

        q = deque()
        q.append(root)
        visitedset = set()
        while q:
            node = q.popleft()
            if node in visitedset:
                return False
            visitedset.add(node)
            if leftChild[node] != -1:
                if leftChild[node] not in visitedset:
                    q.append(leftChild[node])
                else:
                    return False
            if rightChild[node] != -1:
                if rightChild[node] not in visitedset:
                    q.append(rightChild[node])
                else:
                    return False
        return len(visitedset) == n

    def validateBinaryTreeNodes(
        self, n: int, leftChild: List[int], rightChild: List[int]
    ) -> bool:
        return self.solve(n=n, leftChild=leftChild, rightChild=rightChild)


import unittest


class Test(unittest.TestCase):

    def test_case0(self):
        solution = Solution()
        left = [1, -1, 3, -1]
        right = [2, -1, -1, -1]

        self.assertTrue(solution.validateBinaryTreeNodes(4, left, right))


if __name__ == "__main__":
    unittest.main()
