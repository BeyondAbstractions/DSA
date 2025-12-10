# link: https://leetcode.com/problems/number-of-provinces/?envType=problem-list-v2&envId=graph

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

    def size(self, x) -> int:
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
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        ds = DisJointSet()
        for i in range(len(isConnected)):
            ds.add(i)

            row = isConnected[i]
            for j in range(len(row)):
                if row[j] == 1:
                    ds.add(j)
                    ds.union(i, j)

        return ds.components
