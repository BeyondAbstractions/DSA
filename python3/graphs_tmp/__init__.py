import abc, collections, graphviz


class AbstractGraph(abc.ABC):

    def __init__(self, g: collections.OrderedDict):
        self.g = g

    def vertices(self):
        return self.g.keys()

    @abc.abstractmethod
    def edges(self):
        raise NotImplementedError()


class UndirectedAdjMatrix(AbstractGraph):

    def edges(self):
        for i, src in enumerate(self.vertices()):
            vertices = iter(self.vertices())
            for _ in range(i):
                _ = next(vertices)
            for dest in vertices:
                if self.g[src][dest]:
                    yield (src, dest)


class DirectedAdjMatrix(AbstractGraph):

    def edges(self):
        for i, src in enumerate(self.vertices()):
            vertices = iter(self.vertices())
            for _ in range(i):
                _ = next(vertices)
            for dest in vertices:
                if self.g[src][dest]:
                    yield (src, dest)


class UndirectedAdjList(AbstractGraph):

    def edges(self):
        edges = set()
        for src in self.vertices():
            for dest in self.g[src]:
                if (src, dest) not in edges:
                    edges.add((src, dest))
                    edges.add((dest, src))
                    yield (src, dest)


class DirectedAdjList(AbstractGraph):

    def edges(self):
        for src in self.vertices():
            for dest in self.g[src]:
                yield (src, dest)


class DecoratedGraph(AbstractGraph):

    def __init__(self, g: AbstractGraph):
        self.g = g

    def vertices(self):
        return self.g.vertices()

    def edges(self):
        return self.g.edges()


class GraphVizGraph(DecoratedGraph):

    @abc.abstractmethod
    def get_graphviz(self):
        raise NotImplementedError()

    def graphviz(self):
        svg = self.get_graphviz()
        for v in self.vertices():
            svg.node(name=f"{v}")
        for src, dest in self.edges():
            svg.edge(tail_name=f"{src}", head_name=f"{dest}")
        return svg


class UnDirectedGraph(GraphVizGraph):

    def get_graphviz(self):
        g = graphviz.Graph()
        return g


class DirectedGraph(GraphVizGraph):

    def get_graphviz(self):
        g = graphviz.Digraph()
        return g
