# link: https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/description/?envType=problem-list-v2&envId=graph

from typing import List

from collections import defaultdict
from copy import deepcopy


class Stack(object):

    def __init__(self):
        self.data = list()
        self.items = defaultdict(int)

    def push(self, data):
        self.data.append(data)
        self.items[data] += 1

    def pop(self):
        data = self.data.pop()
        self.items[data] -= 1
        if self.items[data] <= 0:
            del self.items[data]
        return data

    def instack(self, data):
        return data in self.data

    def top(self):
        return self.data[-1]

    def isEmpty(self):
        return len(self.data) == 0


class Solution:
    def countPaths_timeout(self, n: int, roads: List[List[int]]) -> int:
        g = defaultdict(list)
        for s, d, t in roads:
            g[s].append((d, t))
            g[d].append((s, t))

        st = Stack()
        st.push(0)

        wt_st = dict()
        wt_st[0] = 0

        it_map = dict()
        it_map[0] = iter(g[0])

        current_wt = 0
        min_wt = None
        count = 0

        while not st.isEmpty():

            top = st.top()

            if top == n - 1:
                if min_wt == None:
                    min_wt = current_wt
                    count = 1
                else:
                    if current_wt < min_wt:
                        min_wt = current_wt
                        count = 1
                    elif current_wt == min_wt:
                        count += 1
                    else:
                        pass

                current_wt -= wt_st[st.top()]
                del it_map[st.top()]
                del wt_st[st.top()]
                st.pop()
                continue

            try:
                d, td = next(it_map[top])
                proposed_wt = current_wt + td
                if not st.instack(d):
                    if min_wt != None:
                        if proposed_wt >= min_wt and d != n - 1:
                            continue

                    current_wt = proposed_wt
                    it_map[d] = iter(g[d])
                    wt_st[d] = td
                    st.push(d)

            except StopIteration:
                current_wt -= wt_st[st.top()]
                del it_map[st.top()]
                del wt_st[st.top()]
                st.pop()

        assert min_wt != None
        return count % (10**9 + 7)

    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        g = defaultdict(dict)

        for s, d, t in roads:
            # s = min(s, d)
            # d = max(s, d)
            g[s][d] = t
            g[d][s] = t

        min_wt = deepcopy(g)

        min_g = deepcopy(g)

        # use apsp floyd warshal
        # |V| times, each vertex V in set(V) can break any (S,D) in set(E)
        for x in min_wt:

            # for each edge
            for s in min_wt:

                # do relaxation if possible via x
                for d in g[s]:

                    if s == d:
                        continue

                    wt_sd = min_wt[s][d]
                    wt_sx = min_wt[s][x] if x in min_wt[s] else None
                    wt_xd = min_wt[x][d] if d in min_wt[x] else None

                    if wt_sx is None or wt_xd is None:
                        min_wt[s][d] = wt_sd
                        min_g[d][s] = None
                        continue

                    proposed_wt = wt_sx + wt_xd

                    if proposed_wt < wt_sd:
                        min_wt[s][d] = proposed_wt
                        min_g[d].clear()
                        min_g[d][x] = None
                        min_g[x][s] = None
                    elif proposed_wt == wt_sd:
                        min_wt[s][d] = wt_sd
                        min_g[d][x] = None
                        min_g[x][s] = None
                    elif wt_sd < proposed_wt:
                        min_wt[s][d] = wt_sd
                        min_g[d][s] = None
                    else:
                        assert False

        count = 0
        path = dict()

        def dfs(s):
            nonlocal count, path, min_g
            path[s] = None

            if s == 0:
                count += 1
                del path[s]
                return

            for d in min_g[s]:
                if d not in path:
                    dfs(d)

            del path[s]

        dfs(n - 1)

        return count % (10**9 + 7)


import unittest


class Test(unittest.TestCase):

    def test_case_0(self):
        n = 7
        roads = [
            [0, 6, 7],
            [0, 1, 2],
            [1, 2, 3],
            [1, 3, 3],
            [6, 3, 3],
            [3, 5, 1],
            [6, 5, 1],
            [2, 5, 1],
            [0, 4, 5],
            [4, 6, 2],
        ]
        s = Solution()
        ret = s.countPaths(n=n, roads=roads)
        self.assertEqual(ret, 4)

    def test_case_1(self):
        pass


if __name__ == "__main__":
    unittest.main()
