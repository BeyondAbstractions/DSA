# link: https://leetcode.com/problems/all-paths-from-source-to-target/description/?envType=problem-list-v2&envId=graph

from typing import List


class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        ret = list()

        def dfs(node, path):
            nonlocal ret
            if node == len(graph) - 1:
                ret.append(list(path + [node]))
                path.pop()
                return

            for neighbor in graph[node]:
                dfs(neighbor, path + [node])
            if path:
                path.pop()

        dfs(0, list())

        return ret


import unittest


class Test(unittest.TestCase):

    def test_case0(self):
        print()
        s = Solution()
        g = [[1, 2], [3], [3], []]
        ret = s.allPathsSourceTarget(g)
        import pprint

        pprint.pprint(ret)


if __name__ == "__main__":
    unittest.main()
