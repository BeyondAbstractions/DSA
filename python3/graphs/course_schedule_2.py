# link: https://leetcode.com/problems/course-schedule-ii/?envType=problem-list-v2&envId=graph

from typing import List
from collections import deque


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        G = {i: list() for i in range(numCourses)}
        degree = {i: {"in": 0, "out": 0} for i in range(numCourses)}
        in_0 = {i: None for i in range(numCourses)}

        for d, s in prerequisites:
            G[s].append(d)
            degree[s]["out"] += 1
            degree[d]["in"] += 1
            if d in in_0:
                del in_0[d]

        topo = list()

        if in_0:
            q = deque()
            for s in in_0:
                q.append(s)
            while q:
                current = q.popleft()
                topo.append(current)
                for d in G[current]:
                    degree[d]["in"] -= 1
                    if degree[d]["in"] == 0:
                        q.append(d)

        return topo if len(topo) == numCourses else list()
