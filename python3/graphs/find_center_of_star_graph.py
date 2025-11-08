# link: https://leetcode.com/problems/find-center-of-star-graph/?envType=problem-list-v2&envId=graph

from typing import List

class Solution:
    def findCenter(self, edges: List[List[int]]) -> int:
        degree = dict()
        for (s,d) in edges:
            if s not in degree:
                degree[s] = {'out': 1, 'in': 0}
            else:
                degree[s]['out'] += 1

            if d not in degree:
                degree[d] = {'out': 0, 'in': 1}
            else:
                degree[d]['in'] += 1

        n = len(degree)
        for node in degree:
            in_degree = degree[node]['in']
            out_degree = degree[node]['out']
            if in_degree == n-1:
                return node
            elif out_degree == n-1:
                return node
            elif (in_degree + out_degree) == n-1:
                return node
        
        assert False, "No center found"

            

        

