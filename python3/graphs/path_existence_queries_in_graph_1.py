# link: https://leetcode.com/problems/path-existence-queries-in-a-graph-i/description/?envType=problem-list-v2&envId=graph

from typing import List

from typing import Tuple, Any
import random


class DisJointSet(object):

    def __init__(self):
        # keys are all elements
        self.pi = dict()

        # keys are always roots of the various trees
        self.size = dict()

        # number of disjoint trees/sets
        self.components = 0

    def find(self, x) -> Tuple[bool, Any]:
        if x not in self.pi:
            return (False, None)
        else:
            # find the representative root of the set that x belongs to

            # assume x itself is the root
            root = x

            # as long as x is not the root keep going up the parent chain
            while root != self.pi[root]:
                root = self.pi[root]

            # now we have found the root, let's do path compression
            # make every node on the path point directly to the root
            while x != root:
                next_x = self.pi[x]
                self.pi[x] = root
                x = next_x

            return (True, root)

    def same_set(self, x, y) -> bool:
        return self.find(x) == self.find(y)

    def union(self, x, y) -> bool:
        found_x, root_x = self.find(x)
        found_y, root_y = self.find(y)

        if not found_x or not found_y:
            return False

        if root_x == root_y:
            return True

        # make root_x the smaller tree
        if self.size[root_x] > self.size[root_y]:
            root_x, root_y = root_y, root_x

        # now root_x is the smaller tree
        # merge root_x into root_y
        self.pi[root_x] = root_y
        self.size[root_y] += self.size[root_x]
        del self.size[root_x]
        self.components -= 1

    def total(self, x) -> int:
        return self.size[self.find(x)[1]]

    def members(self, x) -> set:
        found, root = self.find(x)
        if not found:
            return set()
        else:
            # find all nodes that have root as their representative
            # and return them as a set
            return {k for k in self.pi.keys() if self.find(k)[1] == root}

    def add(self, x):
        if x not in self.pi:
            self.pi[x] = x
            self.size[x] = 1
            self.components += 1

    def isolate(self, x) -> bool:
        found, root = self.find(x)
        if not found:
            return False
        elif root == x and self.size[root] == 1:
            return True
        else:
            members = {k for k in self.pi.keys() if self.find(k)[1] == root and k != x}
            new_root = random.choice(members)
            self.size[new_root] = len(members)
            for k in members:
                self.pi[k] = new_root

            del self.pi[x]
            del self.size[x]
            self.components -= 1

            self.add(x)

    def delete(self, x) -> bool:
        if self.isolate(x):
            del self.pi[x]
            del self.size[x]
            self.components -= 1
            return True
        else:
            return False


class Solution:

    def pathExistenceQueries(
        self, n: int, nums: List[int], maxDiff: int, queries: List[List[int]]
    ) -> List[bool]:
        ds = DisJointSet()
        i = 0

        def collapse(start):
            nonlocal ds, maxDiff, nums
            i = start + 1
            ds.add(start)
            while i < n:
                if abs(nums[i] - nums[start]) <= maxDiff:
                    ds.add(i)
                    ds.union(i, start)
                else:
                    return i
                i += 1
            return i

        i = 0
        while True:
            i = collapse(i)

            if i >= n:
                break

            if abs(nums[i - 1] - nums[i]) <= maxDiff:
                ds.add(i)
                ds.union(i, i - 1)

        ret = list()
        for x, y in queries:
            ret.append(ds.same_set(x, y))

        return ret


import unittest


class Test(unittest.TestCase):

    def test_case0(self):
        s = Solution()
        n = 2
        maxDiff = 1
        nums = [1, 3]
        queries = [[0, 0], [0, 1]]
        ret = s.pathExistenceQueries(n, nums, maxDiff, queries)
        print()
        import pprint

        pprint.pprint(ret)

    def test_case1(self):
        s = Solution()
        n = 4
        maxDiff = 2
        nums = [2, 5, 6, 8]
        queries = [[0, 1], [0, 2], [1, 3], [2, 3]]
        ret = s.pathExistenceQueries(n, nums, maxDiff, queries)
        print()
        import pprint

        pprint.pprint(ret)


if __name__ == "__main__":
    unittest.main()
