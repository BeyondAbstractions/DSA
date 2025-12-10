# link: https://leetcode.com/problems/find-if-path-exists-in-graph/description/?envType=problem-list-v2&envId=graph

from typing import List
from collections import deque


class Solution:
    def validPath_bfs(
        self, n: int, edges: List[List[int]], source: int, destination: int
    ) -> bool:
        G = {i: list() for i in range(n)}
        for a, b in edges:
            G[a].append(b)
            G[b].append(a)

        q = deque()
        q.append(source)
        visited = set()

        while q:
            current = q.popleft()
            visited.add(current)

            if current == destination:
                return True

            for d in G[current]:
                if d not in visited:
                    q.append(d)

                if d == destination:
                    return True
        return False

    def validPath_dfs(
        self, n: int, edges: List[List[int]], source: int, destination: int
    ) -> bool:
        G = {i: list() for i in range(n)}
        for a, b in edges:
            G[a].append(b)
            G[b].append(a)

        stack = deque()
        stack.append((source, iter(G[source])))
        visited = set()

        while stack:
            current, it = stack[-1]
            visited.add(current)

            if current == destination:
                return True

            try:
                d = next(it)
                if d not in visited:
                    stack.append((d, iter(G[d])))
            except StopIteration:
                stack.pop()

        return False

    def validPath(
        self, n: int, edges: List[List[int]], source: int, destination: int
    ) -> bool:
        return self.validPath_dfs(
            n=n, edges=edges, source=source, destination=destination
        )
