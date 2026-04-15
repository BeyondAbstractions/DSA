import typing
import collections
import pprint


class Algo(object):

    def bfs(self, g: typing.Dict[str, typing.Dict[str, None]], s: str) -> None:

        white = {node: None for node in g}
        grey = collections.defaultdict(lambda: None)
        black = collections.defaultdict(lambda: None)
        distance = collections.defaultdict(int)
        parent = collections.defaultdict(lambda: None)

        q = collections.deque()

        del white[s]
        q.append(s)
        grey[s]

        while q:
            current = q.popleft()
            for d in g[current]:
                if d not in grey and d not in black:
                    parent[d] = current
                    distance[d] = distance[current] + 1
                    del white[d]
                    grey[d]
                    q.append(d)

            del grey[current]
            black[current]


import unittest


class Test(unittest.TestCase):

    def test_0(self):
        g = {"a": dict()}
        s = "a"
        algo = Algo()
        algo.bfs(g=g, s=s)


if __name__ == "__main__":
    unittest.main()
