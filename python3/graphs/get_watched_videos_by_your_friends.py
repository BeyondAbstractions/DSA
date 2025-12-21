# link: https://leetcode.com/problems/get-watched-videos-by-your-friends/description/?envType=problem-list-v2&envId=graph

from typing import List
from collections import deque, defaultdict, Counter
from functools import cmp_to_key


class Solution:
    def watchedVideosByFriends(
        self,
        watchedVideos: List[List[str]],
        friends: List[List[int]],
        id: int,
        level: int,
    ) -> List[str]:

        cq = deque()
        nq = deque()
        cq.append(id)

        k = 0

        g = defaultdict(dict)

        visited = dict()
        visited[id] = None

        counter = Counter()

        for s, f in enumerate(friends):
            for d in f:
                g[s][d] = None
                g[d][s] = None

        while 1:

            if not cq and not nq:
                break

            if not cq and nq:
                k += 1
                cq, nq = nq, cq

            cnode = cq.popleft()

            if k == level:
                counter.update(watchedVideos[cnode])

            for d in g[cnode]:
                if d not in visited:
                    visited[d] = None
                    nq.append(d)

        def counter_comparator(a, b):
            nonlocal counter
            if counter[a] < counter[b]:
                return -1
            elif counter[a] > counter[b]:
                return 1
            else:
                if a < b:
                    return -1
                elif a > b:
                    return 1
                else:
                    return 0

        return list(sorted(counter.keys(), key=cmp_to_key(counter_comparator)))


# import unittest


# class Test(unittest.TestCase):

#     def test_case_0(self):
#         watchedVideos = [["A", "B"], ["C"], ["B", "C"], ["D"]]
#         friends = [[1, 2], [0, 3], [0, 3], [1, 2]]
#         id = 0
#         level = 1
#         s = Solution()
#         ret = s.watchedVideosByFriends(
#             watchedVideos=watchedVideos, friends=friends, id=id, level=level
#         )
#         self.assertEqual(ret, ["B", "C"])

#     def test_case_1(self):
#         watchedVideos = [["A", "B"], ["C"], ["B", "C"], ["D"]]
#         friends = [[1, 2], [0, 3], [0, 3], [1, 2]]
#         id = 0
#         level = 2
#         s = Solution()
#         ret = s.watchedVideosByFriends(
#             watchedVideos=watchedVideos, friends=friends, id=id, level=level
#         )
#         self.assertEqual(ret, ["D"])


# if __name__ == "__main__":
#     unittest.main()
