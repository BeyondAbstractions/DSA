# link: https://leetcode.com/problems/find-the-town-judge/?envType=problem-list-v2&envId=graph

from typing import List

class Solution:
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        degree = {i:{'out': 0, 'in': 0} for i in range(n+1)}
        for (s,d) in trust:
            degree[s]['out'] += 1
            degree[d]['in'] += 1
        for i in range(1,n+1):
            if degree[i]['out'] == 0 and degree[i]['in'] == n-1:
                return i
        return -1